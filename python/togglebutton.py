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
from PyQt5 import Qt
from gnuradio import gr
import pmt

class ToggleButton(gr.sync_block, Qt.QPushButton):
    def __init__(self, callback, lbl, pressedReleasedDict, initPressed):
        gr.sync_block.__init__(self, name = "ToggleButton", in_sig = None, out_sig = None)
        Qt.QPushButton.__init__(self,lbl)
        self.setCheckable(True)
        self.lbl = lbl
        self.callback = callback
        self.pressReleasedDict = pressedReleasedDict
        
        self.relBackColor = 'default'
        self.relFontColor = 'default'
        self.pressBackColor = 'default'
        self.pressFontColor = 'default'
        
        self.message_port_register_out(pmt.intern("state"))

        if initPressed:
            self.setChecked(True)
            self.state = 1
            self.callback(self.pressReleasedDict['Pressed'])
            # Note: You can't send the pmt message here in the constructor, it won't work.
        else:
            self.state = 0
        
        self.clicked[bool].connect(self.onToggleClicked)
        
    def setColors(self,relBackColor, relFontColor, pressBackColor, pressFontColor):
        self.relBackColor = relBackColor
        self.relFontColor = relFontColor
        self.pressBackColor = pressBackColor
        self.pressFontColor = pressFontColor
        
        self.setColor()

    def setColor(self):
        if self.state:
            styleStr = ""
            if (self.pressBackColor != 'default'):
                styleStr = "background-color: " + self.pressBackColor + "; "
                
            if (self.pressFontColor):
                styleStr += "color: " + self.pressFontColor + "; "
                
            self.setStyleSheet(styleStr)
        else:
            styleStr = ""
            if (self.relBackColor != 'default'):
                styleStr = "background-color: " + self.relBackColor + "; "
                
            if (self.relFontColor):
                styleStr += "color: " + self.relFontColor + "; "
                
            self.setStyleSheet(styleStr)
                
    def onToggleClicked(self, pressed):
        if pressed:
            self.state = 1
            self.callback(self.pressReleasedDict['Pressed'])
        else:
            self.state = 0
            self.callback(self.pressReleasedDict['Released'])
        
        self.setColor()
        
        self.message_port_pub(pmt.intern("state"),pmt.cons( pmt.intern("state"), pmt.from_long(self.state) ))
        