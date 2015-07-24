# -- coding: utf-8 --
# ===========================================================================
# eXe
# Copyright 2015, Mercedes Cotelo Lois <mclois@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
# ===========================================================================
"""
StyleDesigner provides the functions to create and save the Styles edited with the Styles Designer tool
"""

import logging
import re
import os
import shutil
import json
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from xml.dom import minidom
from twisted.web.resource import Resource
from exe.webui.renderable import Renderable
from exe.engine import version
from exe.engine.style import Style

log = logging.getLogger(__name__)


class StyleDesignerError(Exception):
    def __init__(self, message=''):
        if message == '':
            self.message = _('Error saving style. ')
        else:
            self.message = message
    
    pass

class CreateStyleError(StyleDesignerError):
    def __init__(self, message=''):
        if message == '':
            self.message = _('Error creating style. ')
        else:
            self.message = message
    
    pass

class CreateStyleExistsError(CreateStyleError):
    def __init__(self, absolute_style_dir, message=''):
        self.absolute_style_dir = absolute_style_dir
        if message == '':
            self.message = _('Error creating style, local style already exists. ')
        else:
            self.message = message

    def __str__(self):
        return repr(self.message)

    pass

class StyleDesigner(Renderable, Resource):
    """
    StyleDesigner provides the functions to create and save the Styles edited with the Styles Designer tool
    """
    name = 'styleDesigner'

    def __init__(self, parent):
        """ 
        Initialize
        """ 
        parent.putChild(self.name, self)
        Renderable.__init__(self, parent)
        Resource.__init__(self)

    def render(self, request=None):
        """
        Saves the style and returns a JSON string with the result
        """
        action = request.args['action'][0]
        log.debug("StyleDesigner, action: %s" % (action))
        response = {}
            
        try :
            if action == 'createStyle':
                # Get the style dir name from the style full name, replacing ' ' with '_',
                # cleaning non alphanumeric chars and converting to lower case
                style_dirname = request.args['style_name'][0].replace(' ', '_')
                clean_non_alphanum = re.compile('\W+')
                style_dirname = clean_non_alphanum.sub(' ', style_dirname).strip()
                style_dirname = style_dirname.lower()
            
                style = self.createStyle(style_dirname, request.args)
                response['style_dirname'] = style.get_dirname()
                response['success'] = True
                response['responseText'] = _('Style %s successfully created!') % (style.get_name())
                
            if action == 'saveStyle':
                style_dirname = request.args['style_dirname'][0]
                style = self.saveStyle(style_dirname, request.args)
                response['style_dirname'] = style.get_dirname()
                response['success'] = True
                response['responseText'] = _('Style %s successfully s!') % (style.get_name())
        
        except Exception, e:
            response['success'] = False
            response['responseText'] = str(e)
        
        return json.dumps(response)
    
    def createStyle(self, style_dirname, style_data):
        """
        Creates a new style with the name and data given
        """
        # Check that the target dir does not already exists and create
        styleDir = self.config.stylesDir / style_dirname
        if os.path.isdir(styleDir):
            raise CreateStyleExistsError(styleDir, _('Style %s directory already exists') % (style_dirname))
        else:
            try:
                os.mkdir(styleDir)
                
                # Copy ALL files from the base style
                baseStyleDir = self.config.stylesDir / 'base'
                base_files = os.listdir(baseStyleDir)
                for file_name in base_files:
                    full_file_name = os.path.join(baseStyleDir, file_name)
                    if (os.path.isfile(full_file_name)):
                        shutil.copy(full_file_name, styleDir)
                
                
                # Overwrite content.css, nav.css and config.xml files with the data
                # from the style designer
                contentcss = style_data['contentcss'][0]
                contentcss_file = open(styleDir / 'content.css', 'w')
                contentcss_file.write(contentcss)
                contentcss_file.close()
                
                navcss = style_data['navcss'][0]
                navcss_file = open(styleDir / 'nav.css', 'w')
                navcss_file.write(navcss)
                navcss_file.close()
                
                theme = ET.Element('theme')
                ET.SubElement(theme, 'name').text = style_data['style_name'][0]
                ET.SubElement(theme, 'version').text = '1.0'
                ET.SubElement(theme, 'compatibility').text = version.version
                ET.SubElement(theme, 'author').text = 'eXeLearning.net'
                ET.SubElement(theme, 'author-url').text = 'http://exelearning.net'
                ET.SubElement(theme, 'license').text = 'Creative Commons by-sa'
                ET.SubElement(theme, 'license-url').text = 'http://creativecommons.org/licenses/by-sa/3.0/'
                ET.SubElement(theme, 'description').text = ''
                
                configxml = ET.tostring(theme, 'utf-8')
                configxml_parsed = minidom.parseString(configxml)
                configxml_pretty = configxml_parsed.toprettyxml(indent = "    ")
                configxml_file = open(styleDir / 'config.xml', 'w')
                configxml_file.write(configxml_pretty)
                configxml_file.close()
                
                # New style dir has been created, add style to eXe Styles store
                style = Style(styleDir)
                if style.isValid():
                    if not self.config.styleStore.addStyle(style):
                        styleDir.rmtree()
                        raise CreateStyleExistsError(styleDir, _('The style name already exists'))
                
                return style
                
            except Exception, e:
                if os.path.isdir(styleDir):
                    styleDir.rmtree()
                raise CreateStyleError(str(e))
    
    def saveStyle(self, style_dirname, style_data):
        """
        Updates the style with data given
        """
        styleDir = self.config.stylesDir / style_dirname
        
        # Check that the target dir already exists and update files
        if not os.path.isdir(styleDir):
            raise StyleDesignerError(_('Error saving style, style directory does not exist'))
        else:
            try:
                # Overwrite content.css, nav.css and config.xml files with the data
                # from the style designer
                contentcss = style_data['contentcss'][0]
                contentcss_file = open(styleDir / 'content.css', 'w')
                contentcss_file.write(contentcss)
                contentcss_file.close()
                
                navcss = style_data['navcss'][0]
                navcss_file = open(styleDir / 'nav.css', 'w')
                navcss_file.write(navcss)
                navcss_file.close()
                
                theme = ET.Element('theme')
                ET.SubElement(theme, 'name').text = style_data['style_name'][0]
                ET.SubElement(theme, 'version').text = '1.0'
                ET.SubElement(theme, 'compatibility').text = version.version
                ET.SubElement(theme, 'author').text = 'eXeLearning.net'
                ET.SubElement(theme, 'author-url').text = 'http://exelearning.net'
                ET.SubElement(theme, 'license').text = 'Creative Commons by-sa'
                ET.SubElement(theme, 'license-url').text = 'http://creativecommons.org/licenses/by-sa/3.0/'
                ET.SubElement(theme, 'description').text = ''
                
                configxml = ET.tostring(theme, 'utf-8')
                configxml_parsed = minidom.parseString(configxml)
                configxml_pretty = configxml_parsed.toprettyxml(indent = "    ")
                configxml_file = open(styleDir / 'config.xml', 'w')
                configxml_file.write(configxml_pretty)
                configxml_file.close()
                
                style = Style(styleDir)
                return style
                
            except Exception, e:
                raise StyleDesignerError(str(e))
            
        
        