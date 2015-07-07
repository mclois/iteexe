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
from exe.webui.renderable import Renderable
from twisted.web.resource import Resource
from exe import globals as G
import json
from xml.sax.saxutils import escape

log = logging.getLogger(__name__)

class StyleDesigner(Renderable, Resource):
    """
    StyleDesigner provides the functions to create and save the Styles edited with the Styles Designer tool
    """
    name = 'styleDesigner'

    def __init__(self, parent):
        """ 
        Initialize
        """ 
        Renderable.__init__(self, parent)
        if parent:
            self.parent.putChild(self.name, self)
        Resource.__init__(self)
        self.client = None

    def render(self, request=None):
        """
        Saves the style and returns a JSON string with the result
        """
        log.debug("Render")

        return json.dumps({'success': True, 'data': [], 'responseText': 'OK'})

