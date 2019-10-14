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
from PyQt5.QtGui import QPainter, QPixmap,  QBrush, QColor, QPen, QFont, QFontMetricsF
from PyQt5 import Qt
from PyQt5 import QtCore
from PyQt5.QtCore import Qt as Qtc
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QSize, QPoint, QRect
from PyQt5.QtGui import QPalette
from threading import Lock

from gnuradio import gr
import pmt

class LabeledDialGauge(QFrame):
    # Positions: 1 = above, 2=below, 3=left, 4=right
    def __init__(self, lbl='', barColor='blue', backgroundColor='white', fontColor='black', minValue=0, maxValue=100, maxSize=80, position=1, 
                 isFloat=False,showValue=False,fixedOrMin=True, parent=None):
        QFrame.__init__(self, parent)
        self.numberControl = DialGauge(barColor, backgroundColor, fontColor, minValue, maxValue, maxSize, isFloat,showValue,fixedOrMin, parent)
        
        if position < 3:
            layout =  QVBoxLayout()
        else:
            layout = QHBoxLayout()
            
        self.lbl = lbl
        self.showvalue = showValue
        self.isFloat = isFloat
        
        self.lblcontrol = QLabel(lbl, self)
        self.lblcontrol.setAlignment(Qtc.AlignCenter)

        # For whatever reason, the progressbar doesn't show the number in the bar if it's vertical, only if it's horizontal
        if len(lbl) > 0:        
            self.lblcontrol.setText(lbl)
            
        if (fontColor != 'default'):
            self.lblcontrol.setStyleSheet("QLabel { color : " + fontColor + "; }");
            
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
        
        #if (len(lbl) > 0):
        #    self.setMaximumSize(maxSize+30, maxSize+35)
        #else:
        #    self.setMaximumSize(maxSize, maxSize)  

        self.show()
        
    def setValue(self,newValue):
        self.numberControl.setValue(newValue)
        
class DialGauge(QFrame):
    def __init__(self, barColor='blue', backgroundColor='white', fontColor='black', minValue=0, maxValue=100, maxSize=80, 
                 isFloat=False,showValue=False,fixedOrMin=True, parent=None):
        QFrame.__init__(self, parent)

        self.maxSize = maxSize
        super().setMinimumSize(maxSize,maxSize)
        if fixedOrMin:
            super().setMaximumSize(maxSize,maxSize)
        
        self.backgroundColor = backgroundColor
        self.barColor = barColor
        self.fontColor = fontColor
        self.isFloat = isFloat
        self.showValue = showValue
        
        self.value = minValue
        
        self.minValue = minValue
        self.maxValue = maxValue
        
        self.textfont = QFont(self.font())
        #font.setPixelSize(10)
        self.textfont.setPixelSize(16)
        self.metrics = QFontMetricsF(self.textfont)
            
        self.startAngle = 0.0
        self.endAngle = 360.0
        self.degScaler = 16.0 # The span angle must be specified in 1/16 of a degree units
        self.penWidth = max(int(0.1 * maxSize),6)
        self.halfPenWidth = int(self.penWidth / 2)
        
    def getValue(self):
        if (isFloat):
            return float(self.value)
        else:
            return int(self.value)
                                 
    def setValue(self,newValue):
        if newValue > self.maxValue:
            newValue = self.maxValue
        elif newValue < self.minValue:
            newValue = self.minValue
            
        self.value = float(newValue)

        super().update()
            
    def paintEvent(self, event):
        super().paintEvent(event)

        #self.painter.setPen(self.backgroundColor)
        size = self.size()
        
        percentRange = float(self.value - self.minValue) / float(self.maxValue - self.minValue)
        endAngle = self.startAngle + round(percentRange * float(self.endAngle - self.startAngle),0)

        # Now convert angles to 1/16 scale
        startAngle = int(round(self.startAngle * self.degScaler,0))
        endAngle = int(round(endAngle * self.degScaler,0))
                
        rect = QtCore.QRect(self.halfPenWidth, self.halfPenWidth, size.width()-self.penWidth, size.height()-self.penWidth)
        brush = QBrush(QColor(self.backgroundColor))

        # Set up the painting canvass
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)

        if self.showValue:
            painter.setFont(self.textfont)
            # painter.setPen(QPen(Qtc.black))
            painter.setPen(QPen(QColor(self.fontColor)))

            if (self.isFloat):
                printText = "%.2f" % self.value
            else:
                printText = str(int(self.value))

            painter.drawText(size.width()/2-self.metrics.width(printText)/2,size.height()/2, printText)

        painter.save()
        # painter.translate(self.width()/2, self.height()/2)
        painter.translate(self.width(), 0)
        # painter.scale(self.width()/120.0, self.width()/120.0)
        painter.rotate(90.0)
        
        # First draw complete circle
        painter.setPen(QPen(QColor(self.backgroundColor),self.penWidth))
        painter.drawArc(rect,startAngle, self.endAngle*self.degScaler)
        # First draw complete circle
        painter.setPen(QPen(QColor(self.barColor),self.penWidth))
        painter.drawArc(rect,startAngle, -endAngle)
        painter.setPen(QPen(QColor('darkgray'),2))
        painter.drawEllipse(1, 1, rect.width()+self.penWidth-2,rect.width()+self.penWidth-2)
        painter.drawEllipse(1+self.penWidth, 1+self.penWidth, rect.width()-self.penWidth-2,rect.width()-self.penWidth-2)
        painter.restore()

        painter.end()
        
class GrDialGauge(gr.sync_block, LabeledDialGauge):
    def __init__(self, lbl='', barColor='blue', backgroundColor='white', fontColor='black', minValue=0, maxValue=100, maxSize=80, 
                 position=1, isFloat=False,showValue=False, fixedOrMin=True, parent=None):
        gr.sync_block.__init__(self, name = "DialGauge", in_sig = None, out_sig = None)
        LabeledDialGauge.__init__(self, lbl, barColor, backgroundColor, fontColor, minValue, maxValue, maxSize, position, isFloat,showValue,fixedOrMin, parent)
        self.lbl = lbl
        
        self.message_port_register_in(pmt.intern("value"))
        self.set_msg_handler(pmt.intern("value"), self.msgHandler)   


    def msgHandler(self, msg):
        try:    
            newVal = pmt.to_python(pmt.cdr(msg))

            if type(newVal) == float or type(newVal) == int:
                    super().setValue(newVal)
            else:
                print("[DialGauge] Error: Value received was not an int or a float: %s" % str(e))
                
        except Exception as e:
            print("[DialGauge] Error with message conversion: %s" % str(e))

        
    def setValue(self,newValue):
        super().setValue(newValue)
        
