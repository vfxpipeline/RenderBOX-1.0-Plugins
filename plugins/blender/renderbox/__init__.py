"""
Copyright (c) 2015, RAJIV SHARMA(www.TechnicalDirector.in) . All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.

    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.

    * Neither the name of RAJIV SHARMA(www.TechnicalDirector.in) nor the names of any
      other contributors to this software may be used to endorse or
      promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

bl_info = {
    "name": "RenderBox",
    "author": "Rajiv Sharma",
    "version": (1,0,0),
    "blender": (2, 75, 0 ),
    "location": "Properties > Render > RenderBox",
    "description": "RenderBox",
    "warning": "Copyright (c) 2015, RAJIV SHARMA(www.TechnicalDirector.in)",
    "wiki_url": "http://technicaldirector.in/renderbox",
    "tracker_url": "http://sourceforge.net/p/mx-renderbox/tickets",
    "category": "RenderBox"
    }


if "bpy" in locals():
    import imp
    imp.reload(renderboxLauncher)
else:
    from . import renderboxLauncher

import bpy
from bpy.props import (IntProperty, BoolProperty, StringProperty, PointerProperty)


#create menu for RenderBOX
class RenderBoxMenu(bpy.types.Menu):
    bl_label = "RenderBox_Menu"
    bl_idname = "renderbox_menu"

    def draw(self, context):
        layout = self.layout

class RENDERBOX_Settings(bpy.types.PropertyGroup):
    """custom renderbox options in render settings
    """
    force = BoolProperty(name='Force Start',
        description='this option will clode all running renders and put this file on rendering', default=0)

    jobdescription = StringProperty(name='Job description',
        description='add a quick note to the render to remember easily ', maxlen=512, default='')
    
    outputpath = StringProperty(name='Output Path', description='custom output path for render',maxlen=512, default='')


def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.renderbox_setting = PointerProperty(
        type=RENDERBOX_Settings,
        name='RenderBOX_set',
        description='RenderBOX Render Settings'
    )


def unregister():
    del bpy.types.Scene.renderbox_setting
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
