# -*- coding: utf-8 -*-

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

import os
from time import strftime
import subprocess
from ctypes import *

import bpy


class RENDER_BOX(bpy.types.Panel):
	bl_label = "RenderBox"
	bl_category = 'RenderBox'
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "render"
	bl_options = {'DEFAULT_CLOSED'}

	def draw(self, context):
		layout = self.layout
		sce = context.scene
		settings = sce.renderbox_setting
		col = layout.column(align=True)
		row = col.row(align=True)
		row.scale_y = 1.2
		layout.separator()
		layout.label(text="RenderBox 1.0 Launcher")
		layout.separator()
		row.prop(sce, 'frame_start')
		row.prop(sce, 'frame_end')

		layout.separator()
		col = layout.column()
		col.prop(settings, 'force')
		col.prop(settings, 'jobdescription')
		col.prop(settings, 'outputpath')

		layout.separator()
		layout.label(text="submit render to RenderBox")
		row = layout.row()
		row.scale_y = 1.5
		row.operator('renderbox.submit', icon='RENDER_STILL')


		layout.separator()
		layout.label(text="www.technicaldirector.in/renderbox")


class RENDERBOX_Submit(bpy.types.Operator):
	"""Submit job to RenderBox"""

	bl_idname = "renderbox.submit"
	bl_label = "renderbox Submit Job "

	def execute(self, context):
		user32 = windll.user32
		scene = context.scene
		appname = 'blender%s.%s' %(bpy.app.version[0], bpy.app.version[1])
		apppath = os.getcwd()
		priority = 'Low'
		job_description =  bpy.data.scenes['Scene'].renderbox_setting.jobdescription
		custom_path =  bpy.data.scenes['Scene'].renderbox_setting.outputpath
		
			
		scene_file_name =  bpy.path.basename(bpy.data.filepath)
		scene_file_name =  os.path.splitext(scene_file_name)[0]
		scene_file_path =  bpy.data.filepath

		if not scene_file_path:
			message = user32.MessageBoxW(None, "blender file is not saved\nplease save file to send render", "File Not Saved", 1)
			return {'FINISHED'}

		# save file before proceed render
		bpy.ops.wm.save_mainfile()

		first_frame = scene.frame_start
		last_frame = scene.frame_end
		renderlayers = ""
		date_time = strftime("%a, %d %b %Y %H:%M:%S")
		command = ' -w ' \
		          ' -app "%s" ' \
				  ' -apppath "%s" ' \
		          ' -priority "%s" ' \
		          ' -description "%s" ' \
		          ' -filename "%s" ' \
		          ' -filepath "%s" ' \
		          ' -custompath "%s" ' \
		          ' -renderlayers "%s" ' \
		          ' -startframe "%s" ' \
		          ' -endframe "%s" ' \
		          ' -starttime "%s" ' % (appname, apppath, priority, job_description, scene_file_name, scene_file_path, custom_path, renderlayers , first_frame, last_frame, date_time)
		meta_path = '"C:\\Program Files\\RenderBOX\\bin\\metaDataOperation.exe"'
		if custom_path:
			if not os.path.exists(custom_path):
				message = user32.MessageBoxW(None, "The output path does not exists", "No Directory", 1)
			else:
				subprocess.Popen(meta_path + command)
				message = user32.MessageBoxW(None, "your file sent to RenderBox", "Render Submitted", 1)
		else:
			subprocess.Popen(meta_path + command)
			message = user32.MessageBoxW(None, "your file sent to RenderBox", "Render Submitted", 1)
		
		return {'FINISHED'}


def register():
	bpy.utils.register_module(__name__)


def unregister():
	bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
	register()
