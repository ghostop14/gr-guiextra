#!/usr/bin/env python
#
# Copyright 2019
# ghostop14
#
# This file is part of GNU Radio
#
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt as Qtc
from PyQt5.QtCore import QSize

import os
import sys

from gnuradio import gr
import pmt

class GrGraphicItem(gr.sync_block, QLabel):
    def __init__(self,imageFile,scaleImage=True,fixedSize=False,setWidth=0,setHeight=0):
        gr.sync_block.__init__(self, name = "GrGraphicsItem", in_sig = None, out_sig = None)
        QLabel.__init__(self)
        
        if not os.path.isfile(imageFile):
            print("[GrGraphicsItem] ERROR: Unable to find file " + imageFile)
            sys.exit(1)
            
        try:
            self.pixmap = QPixmap(imageFile)
        except OSError as e:
            print("[GrGraphicsItem] ERROR: " + e.strerror)
            sys.exit(1)
        
        self.imageFile = imageFile
        self.scaleImage = scaleImage
        self.fixedSize = fixedSize
        self.setWidth = setWidth
        self.setHeight = setHeight
        super().setPixmap(self.pixmap)
        
        self.overlays = {}
        
        self.message_port_register_in(pmt.intern("filename"))
        self.set_msg_handler(pmt.intern("filename"), self.msgHandler) 
          
        self.message_port_register_in(pmt.intern("overlay"))
        self.set_msg_handler(pmt.intern("overlay"), self.overlayHandler)   

    def overlayHandler(self, msg):
        try:    
            overlayitem = pmt.to_python(pmt.car(msg))
            if overlayitem is None:
                print("[GrGraphicsItem] ERROR: overlay message contains None in the 'car' portion of the message.  Please pass in a dictionary or list of dictionaries in this portion of the message.  Each dictionary should have the following keys: filename,x,y.  Use x=y=-1 to remove an overlay item.")
                return 
            
            if type(overlayitem) is dict:
                itemlist = []
                itemlist.append(overlayitem)
            elif type(overlayitem) is list:
                itemlist = overlayitem
            else:
                print("[GrGraphicsItem] ERROR: Overlay message type is not correct.  Please pass in a dictionary or list of dictionaries in this portion of the message.  Each dictionary should have the following keys: filename,x,y.  Use x=y=-1 to remove an overlay item.")
                return 

            # Check each dict item to make sure it's valid.
            for curitem in itemlist:
                if type(curitem) == dict:
                    if 'filename' not in curitem:
                        print("[GrGraphicsItem] ERROR: Dictionary item did not contain the 'filename' key.")
                        print("Received " + str(curitem))
                        continue
                        
                    if 'x' not in curitem:
                        print("[GrGraphicsItem] ERROR: The dictionary for filename " + curitem['filename'] + " did not contain an 'x' key.")
                        print("Received " + str(curitem))
                        continue
                        
                    if 'y' not in curitem:
                        print("[GrGraphicsItem] ERROR: The dictionary for filename " + curitem['filename'] + " did not contain an 'y' key.")
                        print("Received " + str(curitem))
                        continue
                        
                    if not os.path.isfile(curitem['filename']):
                        print("[GrGraphicsItem] ERROR: Unable to find overlay file " + curitem['filename'])
                        print("Received " + str(curitem))
                        continue
                    
                    # Now either add/update our list or remove the item.
                    if curitem['x'] == -1 and curitem['y'] == -1:
                        try:
                            del self.overlays[curitem['filename']]  # remove item
                        except:
                            pass
                    else:
                        self.overlays[curitem['filename']] = curitem
                
                self.updateGraphic()
        except Exception as e:
            print("[GrGraphicsItem] Error with overlay message conversion: %s" % str(e))
        
    def updateGraphic(self):
        if (len(self.overlays.keys()) == 0):
            try:
                super().setPixmap(self.pixmap)
            except Exception as e:
                print("[GrGraphicsItem] Error updating graphic: %s" % str(e))
                return
        else:
            # Need to deal with overlays
            tmpPxmap = self.pixmap.copy(self.pixmap.rect())
            painter = QPainter(tmpPxmap)
            for curkey in self.overlays.keys():
                curOverlay = self.overlays[curkey]
                try:
                    newOverlay = QPixmap(curkey)
                    if 'scalefactor' in curOverlay:
                        scale = curOverlay['scalefactor']
                        w = newOverlay.width()
                        h = newOverlay.height()
                        newOverlay = newOverlay.scaled(int(w*scale),int(h*scale),Qtc.KeepAspectRatio)
                    painter.drawPixmap(curOverlay['x'],curOverlay['y'], newOverlay)
                except Exception as e:
                    print("[GrGraphicsItem] Error adding overlay: %s" % str(e))
                    return

            painter.end()
                    
            super().setPixmap(tmpPxmap)
            
    def msgHandler(self, msg):
        try:    
            newVal = pmt.to_python(pmt.cdr(msg))
            imageFile=newVal
            if type(newVal) == str:
                if not os.path.isfile(imageFile):
                    print("[GrGraphicsItem] ERROR: Unable to find file " + imageFile)
                    return
                
                try:
                    self.pixmap = QPixmap(imageFile)
                    self.imageFile = imageFile
                except OSError as e:
                    print("[GrGraphicsItem] ERROR: " + e.strerror)
                    return
                
                self.updateGraphic()
            else:
                print("[GrGraphicsItem] Error: Value received was not an int or a bool: %s" % str(e))
                
        except Exception as e:
            print("[GrGraphicsItem] Error with message conversion: %s" % str(e))

    def minimumSizeHint(self):
        return QSize(self.pixmap.width(),self.pixmap.height())

    def resizeEvent(self, event):
        if self.scaleImage:
            w = super().width()
            h = super().height()
            
            self.pixmap = self.pixmap.scaled(w,h,Qtc.KeepAspectRatio)
        elif self.fixedSize and self.setWidth > 0 and self.setHeight > 0:
            self.pixmap = self.pixmap.scaled(self.setWidth,self.setHeight,Qtc.KeepAspectRatio)

        self.updateGraphic()