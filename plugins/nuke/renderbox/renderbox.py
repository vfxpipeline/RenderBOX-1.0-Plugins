"""
Name: Renderbox Lanucher for Nuke
Author :  Rajiv Sharma
Developer Website : www.technicaldirector.in
Developer Email   : rajiv@technicaldirector.in
Date Started : 01 Sept 2015
Date Modified :
Description: This file will send nuke file to renderbox

Download Application from : www.technicaldirector.in/renderbox
Source Code Website : www.github.com/vfxpipeline/renderbox
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

import os
import subprocess
from PySide import QtGui
from time import strftime
from nukescripts import panels

from ui_win.launcher import Ui_MainWindow


class RenderboxLauncherClass(Ui_MainWindow, QtGui.QMainWindow):

    def __init__(self):
        super(RenderboxLauncherClass, self).__init__()
        self.setupUi(self)
        self.updateWriteNodesList()
        self.send_PB.clicked.connect(self.sendJob)

    def getInfo(self):
        nuke_version = nuke.NUKE_VERSION_STRING
        appname = 'nuke%s' % nuke_version
        apppath = nuke.EXE_PATH
        scene_file_path = nuke.root()['name'].value()
        scene_file_name = os.path.basename(scene_file_path)
        if self.groupBox.isChecked():
            first_frame = self.start_frame_LE.text()
            last_frame = self.end_frame_LE.text()
        else:
            first_frame = nuke.Root()['first_frame'].value()
            last_frame = nuke.Root()['last_frame'].value()
        date_time = strftime("%a, %d %b %Y %H:%M:%S")
        write_node = self.writeNode_CB.currentText()  # use write node as render layers
        selected_write_node = nuke.toNode(write_node)
        custom_path = self.output_path_LE.text()
        if custom_path:
          selected_write_node["file"].setValue(custom_path)
        output_path =  selected_write_node["file"].value()
        output_path = os.path.dirname(output_path)
        job_description = self.description_LE.text()
        priority = self.priority_CB.currentText()
        
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
                  ' -starttime "%s" ' % (appname, apppath, priority, job_description, scene_file_name, scene_file_path, output_path, write_node, first_frame, last_frame, date_time)

        if custom_path:
          if os.path.exists(custom_path):
            return command
          else:
            QtGui.QMessageBox.warning(self, "Path not exists", "Output path provided by you is not exists" )
            return 0
        else:
          return command

    def updateWriteNodesList(self):
        """
        this function will update the list of write nodes in nuke script
        """
        writeNodes = []
        for node in nuke.allNodes():
            if node.Class() == 'Write':
                node_name = node['name'].getValue()
                writeNodes.append(node_name)
        self.writeNode_CB.addItems(writeNodes)

    def sendJob(self):
        """
        This function will launch job to renderbox
        """
        file_location = nuke.root()['name'].value()
        if file_location == '':
            QtGui.QMessageBox.warning(self, "File Not Saved", "nuke file is not saved\nplease save file to send render" )
            return
 
        if not self.writeNode_CB.currentText():
            QtGui.QMessageBox.warning(self, "No Write Node Found", "you did not add write node\nplease add write node to send render" )
            return

        # save nuke file before execute render
        nuke.scriptSave()
        app_path = '"C:\\Program Files\\RenderBOX\\bin\\metaDataOperation.exe" '
        value = self.getInfo()
        if value:
          command = app_path + value
          subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
          QtGui.QMessageBox.about(self, 'Render Submitted', 'your file sent to RenderBox ')
        else:
          return

def show_ui():
    global execGui
    execGui= RenderboxLauncherClass()
    execGui.show()