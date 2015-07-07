// ===========================================================================
// eXeLearning
// Copyright 2014, Mercedes Cotelo Lois <mclois@gmail.com>
//
// This program is free software; you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation; either version 2 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program; if not, write to the Free Software
// Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
//===========================================================================

Ext.define('eXe.view.forms.StyleDesignerCreate', {
    extend: 'Ext.form.Panel',
    alias: 'widget.styledesignercreate',
	url: location.pathname + '/styleDesigner',
    id: 'styledesignercreateform',
    bodyPadding: 10,
    items: [
        {
        	xtype: 'textfield',
        	fieldLabel: _('Style name'),
        	name: 'style_name',
        	allowBlank: false,
            width: '100%'
        },
        {
        	xtype: 'textfield',
        	fieldLabel: _('Author'),
        	name: 'style_author',
        	allowBlank: false,
            width: '100%'
        },
        {
        	xtype: 'textfield',
        	fieldLabel: _('Author URL'),
        	name: 'style_author_url',
        	vtype: 'url',
            width: '100%'
        },
        {
        	xtype: 'textarea',
        	fieldLabel: _('Description'),
        	name: 'style_description',
            width: '100%'
        }
    ],
    buttons: [
        {
            text: _('Continue'),
            handler: function() {
                var form = this.up('form').getForm(); // get the form panel
                if (form.isValid()) { // make sure the form contains valid data before submitting
                    form.submit({
                        success: function(response) {
                           console.log(response);
                           Ext.Msg.alert('Success', response);
                        },
                        failure: function(response) {
                            console.log(response);
                            Ext.Msg.alert('Failed', response);
                        }
                    });
                }
                else { // display error alert if the data is invalid
                    Ext.Msg.alert('Invalid Data', 'Please correct form errors.')
                }
            }
        }
    ]
});
