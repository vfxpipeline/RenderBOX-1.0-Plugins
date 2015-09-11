"""
Name: RenderBox Launcher for Maya
Author :  Rajiv Sharma
Developer Website : www.technicaldirector.in
Developer Email   : rajiv@technicaldirector.in
Date Started : 23 August 2015
Date Modified :
Description: This file will launch maya render to renderbox

Download Application from : www.technicaldirector.in/renderbox
Free Video Tutorials : www.youtube.com/vfxpipeline

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
__author__ = 'Rajiv Sharma'
__version__ = '1.0'

import maya.utils
import os
import subprocess
from time import strftime
import pymel.core as pm
import maya.cmds as cmds

 
class RenderboxLauncherClass(object):
    def __init__(self, *args):
        # first delete window if it already exists
        if (cmds.window('MainWindow', exists=True)):
            cmds.deleteUI('MainWindow')
        path = os.path.dirname(__file__)
        ui_file = path + '/ui/launcher.ui'
        self.ui = cmds.loadUI(f=ui_file)
        ## Create dock layout and tell it where it can go
        dockLayout = cmds.paneLayout(configuration='single', parent=self.ui)
        cmds.dockControl(allowedArea='all', area='right', floating=True, content=dockLayout, label='RenderBOX 1.0 Launcher')
        ## parent our window underneath the dock layout
        cmds.control(self.ui, e=True, parent=dockLayout)
        cmds.button( "send_PB", edit=True, command=self.sendJob )
    
    def getValues(self):
        """
        In this function we will get all values
        """
        renderer = cmds.getAttr('defaultRenderGlobals.currentRenderer')
        if not renderer == 'mentalRay' :
          cmds.confirmDialog( title='Renderer Not Supported', message='Render box only support mentalRay', button=['Exit'], cancelButton='Exit' )
          return 0
        app = pm.about(application =True)
        version = pm.about(version=True)
        appname = app+version
        apppath = os.environ["MAYA_LOCATION"]
        renderableLayerList = []
        date_time = strftime("%a, %d %b %Y %H:%M:%S")
        scene_file_path = str(pm.system.sceneName())
        scene_file_name = str(os.path.basename(scene_file_path))
        renderLayerList = cmds.ls(type='renderLayer')
        for renderLayerName in renderLayerList:
            renderableLayer = cmds.getAttr('%s.renderable' % renderLayerName)
            if renderableLayer:
                renderableLayerList.append(renderLayerName)
        # Get the name of the first and last image for the current layer
        first_frame = str(cmds.getAttr('defaultRenderGlobals.startFrame'))
        last_frame = str(cmds.getAttr('defaultRenderGlobals.endFrame'))
        newList = str(renderableLayerList).replace("u'", "").replace("'", "").replace("[", "").replace("]","")
        custom_path = ''
        custom_checkbox = pm.checkBox('custom_CB', query=True, value=True)
        if custom_checkbox:
            first_frame = pm.textField('start_frame_LE', query=True, text=True)
            try:
              val = int(first_frame)
            except ValueError:
              cmds.confirmDialog( title='invalid number', message='first frame is not valid', button=['Exit'], cancelButton='Exit' )
              return 0
            last_frame = pm.textField('end_frame_LE', query=True, text=True)
            try:
              val = int(last_frame)
            except ValueError:
              cmds.confirmDialog( title='invalid number', message='last frame is not valid', button=['Exit'], cancelButton='Exit' )
              return 0
            custom_path = pm.textField('output_path_LE', query=True, text=True)
        job_description = pm.textField('description_LE', query=True, text=True)
        priority = pm.optionMenu('priority_CB', query=True, value=True)
        #force_start = pm.checkBox('force_start_TB', query=True, value=True)
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
                  ' -starttime "%s" ' % (appname, apppath, priority, job_description, scene_file_name, scene_file_path, custom_path, newList , first_frame, last_frame, date_time)
        
        if custom_path:
          if os.path.exists(custom_path):
            return command
          else:
            cmds.confirmDialog( title='Path not exists', message='Output path provided by you is not exists', button=['Exit'], cancelButton='Exit' )
            return 0
        else:
          return command
    
    def sendJob(self, *args):
        """
        This function will launch job to renderbox
        """
        file_location = cmds.file(q=True, location=True)
        if file_location == 'unknown':
          cmds.confirmDialog( title='File Not Saved', message='maya file is not saved\nplease save file to send render', button=['Exit'], cancelButton='Done' )
          return
        modify_file = cmds.file(q=True, modified=True)
        if modify_file:
          pm.system.saveFile()
        app_path = '"C:\\Program Files\\RenderBOX\\bin\\metaDataOperation.exe"'
        value = self.getValues()
        if value:
          command = app_path + value
          subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
          cmds.confirmDialog( title='Render Submitted', message='your file sent to RenderBox ', button=['Done'], cancelButton='Done' )
        else:
          return


if __name__ == '__main__':
    RenderboxLauncher = RenderboxLauncherClass()

