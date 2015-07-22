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
import os
from exe.webui.renderable import Renderable
from twisted.web.resource import Resource
import json


log = logging.getLogger(__name__)


class StyleDesignerError(Exception):
    def __init__(self, message=''):
        if message == '':
            self.message = u'Error creating style, local style already exists. '
        else:
            self.message = message
    
    pass

class CreateStyleError(StyleDesignerError):
    def __init__(self, message=''):
        if message == '':
            self.message = u'Error creating style, local style already exists. '
        else:
            self.message = message
    
    pass

class CreateStyleExistsError(CreateStyleError):
    def __init__(self, absolute_style_dir, message=''):
        self.absolute_style_dir = absolute_style_dir
        if message == '':
            self.message = u'Error creating style, local style already exists. '
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
        
        if action == 'createStyle':
            self.createStyle(request.args['style_name'][0], request.args)

        return json.dumps({'success': True, 'data': [], 'responseText': 'OK'})
    
    def createStyle(self, style_name, style_data):
        """
        Creates a new style with the name and data given
        """
        styleDir = self.config.stylesDir / style_name
        
        if os.path.isdir(styleDir):
            raise CreateStyleExistsError(styleDir, u'Style directory already exists')
        else:
            try:
                os.mkdir(styleDir)
            except Exception, e:
                raise CreateStyleError(str(e))
            
        
        