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
from PyQt5.QtWidgets import QFrame, QWidget, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtGui import QPainter, QPixmap,  QBrush, QColor, QPen
from PyQt5 import Qt
from PyQt5 import QtCore
from PyQt5.QtCore import Qt as Qtc
from PyQt5.QtCore import QSize, QPoint, QRect
from PyQt5.QtGui import QPixmap,QPainter, QPainterPath,QLinearGradient, QRadialGradient, QConicalGradient

from gnuradio import gr
import pmt

class LabeledLEDIndicator(QFrame):
    # Positions: 1 = above, 2=below, 3=left, 4=right
    def __init__(self, lbl='', onColor='green', offColor='red', initialState=False, maxSize=80, position=1, parent=None):
        QFrame.__init__(self, parent)
        self.numberControl = LEDIndicator(onColor, offColor, initialState, maxSize, parent)
        
        if position < 3:
            layout =  QVBoxLayout()
        else:
            layout = QHBoxLayout()
            
        self.lbl = lbl
        self.lblcontrol = QLabel(lbl, self)
        self.lblcontrol.setAlignment(Qtc.AlignCenter)

        # add top or left
        if len(lbl) > 0:
            if position == 1 or position == 3:
                layout.addWidget(self.lblcontrol)
        else:
            self.hasLabel = False

        layout.addWidget(self.numberControl)
        
        # Add bottom or right
        if len(lbl) > 0:
            if position == 2 or position == 4:
                layout.addWidget(self.lblcontrol)
                
        layout.setAlignment(Qtc.AlignCenter | Qtc.AlignVCenter)
        self.setLayout(layout)
        
        if (len(lbl) > 0):
            self.setMaximumSize(maxSize+30, maxSize+35)
        else:
            self.setMaximumSize(maxSize, maxSize)  

        self.show()
        
    def setState(self,onOff):
        self.numberControl.setState(onOff)
        
class LEDIndicator(QFrame):
    def __init__(self, onColor='green', offColor='red', initialState=False, maxSize=80, parent=None):
        QFrame.__init__(self, parent)

        #super().setPixmap(QtGui.QPixmap(":/icons/led-red-on.png"))
        #super().setScaledContents(True)

        self.maxSize = maxSize
        self.curState = initialState  
        self.onColor = QColor(onColor)
        self.offColor = QColor(offColor)

        self.setMinimumSize(maxSize, maxSize)      
        self.setMaximumSize(maxSize, maxSize)  

    def setState(self,onOff):
        self.curState = onOff
        super().update()
        
    def paintEvent(self, event):
        super().paintEvent(event)
        
        painter = QPainter(self)
        
        #self.painter.setPen(self.backgroundColor)
        size = self.size()
        brush = QBrush()

        #rect = QtCore.QRect(2, 2, size.width()-4, size.height()-4)
        rect = QtCore.QRect(0, 0, size.width(), size.height())
        #painter.fillRect(rect, brush)
        smallestDim = size.width()
        if smallestDim > size.height():
            smallestDim = size.height();
            
        smallestDim = smallestDim/2
        smallestDim -= 2
        ## rect.moveCenter(QPoint(size.width()/2,size.height()/2))
        center_x = size.width()/2
        center_y = size.height()/2
        centerpoint = QPoint(center_x,center_y)
        
        # Draw the border
        #circle_path = QPainterPath()
        radius = smallestDim
        #circle_path.addEllipse(centerpoint,radius,radius)
        painter.setPen(QPen(QColor('lightgray'),0))
        brush.setStyle(Qtc.SolidPattern)

        radial = QRadialGradient(center_x,center_y/2, radius)
        #radial = QConicalGradient(centerpoint, 50)  # Last number is the angle
        radial.setColorAt(0, Qtc.white)
        radial.setColorAt(0.8, Qtc.darkGray)
        painter.setBrush(QBrush(radial))
        painter.drawEllipse(centerpoint,radius,radius)
        #painter.setBrush(QColor('gray'))
        # painter.drawPath(circle_path)
        
        # Draw the colored center        
        radial = QRadialGradient(center_x,center_y/2, radius)
        #radial = QRadialGradient(center_x*2/3,center_y*2/3, radius)
        #radial = QConicalGradient(centerpoint, 0)  # Last number is the angle
        radial.setColorAt(0, Qtc.white)
        
        if (self.curState):
            radial.setColorAt(.7, self.onColor)
            brush.setColor(self.onColor)
            painter.setPen(QPen(self.onColor,0))
        else:
            radial.setColorAt(.7, self.offColor)
            brush.setColor(self.offColor)
            painter.setPen(QPen(self.offColor,0))
            
        brush.setStyle(Qtc.SolidPattern)
        #painter.setBrush(brush)
        painter.setBrush(QBrush(radial))
        #radius = radius - 9
        if (smallestDim <= 30):
            radius = radius - 3
        elif (smallestDim <= 60):
            radius = radius - 4
        elif (smallestDim <=100):
              radius = radius - 5
        elif (smallestDim <= 200):
            radius = radius - 6
        elif (smallestDim <= 300):
            radius = radius - 7
        else:
            radius = radius - 9
        painter.drawEllipse(centerpoint,radius,radius)

class GrLEDIndicator(gr.sync_block, LabeledLEDIndicator):
    def __init__(self, lbl='', onColor='green', offColor='red', initialState=False, maxSize=80, position=1, parent=None):
        gr.sync_block.__init__(self, name = "LEDIndicator", in_sig = None, out_sig = None)
        LabeledLEDIndicator.__init__(self, lbl, onColor, offColor, initialState, maxSize, position, parent)
        self.lbl = lbl
        
        self.message_port_register_in(pmt.intern("state"))
        self.set_msg_handler(pmt.intern("state"), self.msgHandler)   


    def msgHandler(self, msg):
        try:    
            newVal = pmt.to_python(pmt.cdr(msg))

            if type(newVal) == bool or type(newVal) == int:
                if type(newVal) == bool:
                    super().setState(newVal)
                else:
                    if newVal == 1:
                        super().setState(True)
                    else:
                        super().setState(False)
            else:
                print("[LEDIndicator] Error: Value received was not an int or a bool: %s" % str(e))
                
        except Exception as e:
            print("[LEDIndicator] Error with message conversion: %s" % str(e))

    def setState(self,onOff):
        super().setState(onOff)
        
