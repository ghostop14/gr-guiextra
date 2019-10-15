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

from PyQt5.QtWidgets import QFrame, QWidget, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtGui import QPainter, QPixmap,  QBrush, QColor, QPen, QFontMetricsF
from PyQt5 import Qt
from PyQt5 import QtCore
from PyQt5.QtCore import Qt as Qtc
from PyQt5.QtCore import QSize, QPoint, QRect
from PyQt5.QtGui import QPixmap,QPainter, QPainterPath

from gnuradio import gr
import pmt

class LabeledToggleSwitch(QFrame):
    # Positions: 1 = above, 2=below, 3=left, 4=right
    def __init__(self, lbl='', onColor='green', offColor='red', initialState=False, maxSize=50, position=1, parent=None, callback=None, alignment=1, valignment=1):
        QFrame.__init__(self, parent)
        self.numberControl = ToggleSwitch(onColor, offColor, initialState, maxSize, parent, callback)
        
        if position < 3:
            layout =  QVBoxLayout()
        else:
            layout = QHBoxLayout()
            
        self.lbl = lbl
        self.lblcontrol = QLabel(lbl, self)
        
        if position == 3: # left of switch
            self.lblcontrol.setAlignment(Qtc.AlignRight)
        elif position == 4: # right of switch
            self.lblcontrol.setAlignment(Qtc.AlignLeft)
        else:
            # Above or below
            self.lblcontrol.setAlignment(Qtc.AlignCenter)

        # add top or left
        if len(lbl) > 0:
            if position == 1 or position == 3:
                layout.addWidget(self.lblcontrol)

        layout.addWidget(self.numberControl)
        
        # Add bottom or right
        if len(lbl) > 0:
            if position == 2 or position == 4:
                layout.addWidget(self.lblcontrol)
                
        if alignment == 1:        
            halign = Qtc.AlignCenter
        elif alignment == 2:
            halign = Qtc.AlignLeft
        else:
            halign = Qtc.AlignRight

        if valignment == 1:
            valign = Qtc.AlignVCenter
        elif valignment == 2:
            valign = Qtc.AlignTop
        else:
            valign = Qtc.AlignBottom
            
        layout.setAlignment(halign | valign)
        # layout.setAlignment(Qtc.AlignCenter | Qtc.AlignVCenter)
        self.setLayout(layout)
        
        textfont = self.lblcontrol.font()
        metrics = QFontMetricsF(textfont)
        
        maxWidth = max( (maxSize+4),(maxSize*2 + metrics.width(lbl)) )
        maxHeight = max( (maxSize/2+4),(maxSize/2 + metrics.height()+2) )
        #print('Min size: ' + str(maxWidth) + " x " + str(maxHeight))
        
        self.setMinimumSize(int(maxWidth), int(maxHeight))

        self.show()
        
    def setState(self,onOff):
        self.numberControl.setState(onOff)
        
class ToggleSwitch(QFrame):
    def __init__(self, onColor='green', offColor='red', initialState=False, maxSize=50, parent=None, callback=None):
        QFrame.__init__(self, parent)

        #super().setPixmap(QtGui.QPixmap(":/icons/led-red-on.png"))
        #super().setScaledContents(True)

        self.maxSize = maxSize
        self.curState = initialState  
        self.onColor = QColor(onColor)
        self.offColor = QColor(offColor)
        self.callback = callback
        self.setMinimumSize(maxSize, maxSize/2)      
        self.setMaximumSize(maxSize, maxSize/2)  

    def setState(self,onOff):
        self.curState = onOff
        if self.callback is not None:
            self.callback(onOff)
            
        super().update()
        
    def paintEvent(self, event):
        super().paintEvent(event)
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        size = self.size()
        brush = QBrush()

        rect = QtCore.QRect(0, 0, size.width(), size.height())
        #painter.fillRect(rect, brush)

        switchWidth = size.width()/2 - 2            
        switchHeight = size.height()/2 - 2
        ## rect.moveCenter(QPoint(size.width()/2,size.height()/2))
        center_x = size.width()/2
        center_y = size.height()/2
        centerpoint = QPoint(center_x,center_y)
        
        if (self.curState):
            brush.setColor(self.onColor)
            painter.setPen(QPen(self.onColor,0))
        else:
            brush.setColor(self.offColor)
            painter.setPen(QPen(self.offColor,0))
            
        brush.setStyle(Qtc.SolidPattern)
        painter.setBrush(brush)
        
        # Draw the switch background
        centerRect = QRect(size.width()/4,0,size.width()/2-4,size.height())
        painter.drawRect(centerRect)
        painter.drawEllipse(0,0,size.height(),size.height())
        painter.drawEllipse(size.width()/2,0,size.height(),size.height())

        # Draw the switch itself
        brush.setColor(QColor('white'))
        painter.setBrush(brush)
        painter.setPen(QPen(QColor('white'),0))
        actualSwitchWidth = min(switchWidth/2,switchHeight)
        if self.curState:
            painter.drawEllipse(2,2,size.height() - 4,size.height() - 4)
        else:
            painter.drawEllipse(center_x+2,2,size.height() - 4,size.height() - 4)
        
    def mousePressEvent(self,event):
        if (event.x() <= self.size().width()/2):
            self.setState(True)
        else:
            self.setState(False)
            
        super().update()

class GrToggleSwitch(gr.sync_block, LabeledToggleSwitch):
    def __init__(self, callback, lbl, pressedReleasedDict, initialState=False, onColor='green', offColor='silver', position=3 , maxSize=50, alignment=1, valignment=1, parent=None):
        gr.sync_block.__init__(self, name = "ToggleSwitch", in_sig = None, out_sig = None)
        LabeledToggleSwitch.__init__(self, lbl, onColor, offColor, initialState, maxSize, position, parent, self.notifyUpdate, alignment, valignment)
        
        self.pressReleasedDict = pressedReleasedDict
        self.callback = callback
        self.message_port_register_out(pmt.intern("state"))
        
    def notifyUpdate(self,newVal):
        if self.callback is not None:
            if (newVal):
                self.callback(self.pressReleasedDict['Pressed'])
            else:
                self.callback(self.pressReleasedDict['Released'])
            
        if (newVal):
            if type(self.pressReleasedDict['Pressed']) == bool:
                self.message_port_pub(pmt.intern("state"),pmt.cons( pmt.intern("state"), pmt.from_bool(self.pressReleasedDict['Pressed']) ))
            elif type(self.pressReleasedDict['Pressed']) == int:
                self.message_port_pub(pmt.intern("state"),pmt.cons( pmt.intern("state"), pmt.from_long(self.pressReleasedDict['Pressed']) ))
            else:
                self.message_port_pub(pmt.intern("state"),pmt.cons( pmt.intern("state"), pmt.intern(self.pressReleasedDict['Pressed']) ))
        else:
            if type(self.pressReleasedDict['Released']) == bool:
                self.message_port_pub(pmt.intern("state"),pmt.cons( pmt.intern("state"), pmt.from_bool(self.pressReleasedDict['Released']) ))
            elif type(self.pressReleasedDict['Released']) == int:
                self.message_port_pub(pmt.intern("state"),pmt.cons( pmt.intern("state"), pmt.from_long(self.pressReleasedDict['Released']) ))
            else:
                self.message_port_pub(pmt.intern("state"),pmt.cons( pmt.intern("state"), pmt.intern(self.pressReleasedDict['Released']) ))
            