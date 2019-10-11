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
from PyQt5.QtWidgets import QFrame, QWidget, QVBoxLayout, QLabel
from PyQt5 import Qt
from PyQt5.QtCore import Qt as Qtc
from PyQt5.QtCore import QSize
from gnuradio import gr
import pmt

class LabeledDialControl(QFrame):
    def __init__(self, lbl = '', parent=None, minimum=0, maximum=100, defaultvalue=0,backgroundColor='default', changedCallback=None, minsize=100, isFloat = False, scaleFactor = 1, showvalue=False):
        QFrame.__init__(self, parent)
        self.numberControl = DialControl(minimum, maximum, defaultvalue,backgroundColor, self.valChanged, changedCallback, minsize)
        
        layout =  QVBoxLayout()

        self.showvalue = showvalue
        self.isFloat = isFloat
        self.scaleFactor = scaleFactor
        self.lbl = lbl
        self.lblcontrol = QLabel(lbl, self)
        self.lblcontrol.setAlignment(Qtc.AlignCenter)

        if self.showvalue:        
            textstr = self.buildTextStr(defaultvalue*self.scaleFactor)
            self.lblcontrol.setText(textstr)

        if len(lbl) > 0:
            self.hasLabel = True
            layout.addWidget(self.lblcontrol)
        else:
            self.hasLabel = False

        layout.addWidget(self.numberControl)
        
        layout.setAlignment(Qtc.AlignCenter)
        self.setLayout(layout)
        self.show()
        
    def buildTextStr(self, newValue):
        textstr=""
        if len(self.lbl) > 0:
            textstr = self.lbl + " - "
            
        if self.isFloat:
            textstr += "%.2f" % (newValue)
        else:
            textstr += str(newValue)

        return textstr
    
    def valChanged(self, newValue):
        if not self.showvalue:
            return 
        
        if len(self.lbl) > 0:
            if int(self.scaleFactor) != 1:
                newValue = newValue * self.scaleFactor
                
            textstr = self.buildTextStr(newValue)
            self.lblcontrol.setText(textstr)
        
class DialControl(Qt.QDial):
    def __init__(self, minimum=0, maximum=100, defaultvalue=0,backgroundColor='default', lablelCallback=None, changedCallback=None, minsize=100):
        Qt.QDial.__init__(self)
        
        if (backgroundColor != "default"):
            self.setStyleSheet("background-color: " + backgroundColor + ";")
            
        self.minsize = minsize
        self.changedCallback = changedCallback
        self.lablelCallback = lablelCallback
        super().setMinimum(minimum)
        super().setMaximum(maximum)
        super().setValue(defaultvalue)
        super().valueChanged.connect(self.sliderMoved)
        
    def minimumSizeHint(self):
            return QSize(self.minsize,self.minsize)
        
    def sliderMoved(self):
        if self.changedCallback is not None:
            self.changedCallback(self.value())
            
        if self.lablelCallback is not None:
            self.lablelCallback(self.value())

class GrDialControl(gr.sync_block, LabeledDialControl):
    def __init__(self, lbl, parent, minimum, maximum, defaultvalue,backgroundColor='default', varCallback=None, isFloat=False, scaleFactor = 1, minsize=100, showvalue=False):
        gr.sync_block.__init__(self, name = "GrDialControl", in_sig = None, out_sig = None)
        LabeledDialControl.__init__(self,lbl, parent, minimum, maximum, defaultvalue,backgroundColor, self.valueChanged, minsize, isFloat, scaleFactor, showvalue)
        
        self.varCallback = varCallback
        self.scaleFactor = scaleFactor
        self.isFloat = isFloat
        self.message_port_register_out(pmt.intern("value"))

    def valueChanged(self, newValue):
        if int(self.scaleFactor) != 1:
            newValue = newValue * self.scaleFactor
            
        if (self.varCallback is not None):
            self.varCallback(newValue)

        if (self.isFloat):
            self.message_port_pub(pmt.intern("value"),pmt.cons( pmt.intern("value"), pmt.from_float(newValue) ))
        else:
            self.message_port_pub(pmt.intern("value"),pmt.cons( pmt.intern("value"), pmt.from_long(newValue) ))
