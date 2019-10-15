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
from PyQt5.QtWidgets import QFrame, QWidget, QHBoxLayout, QVBoxLayout, QLabel,QProgressBar
from PyQt5.QtGui import QPainter, QPixmap,  QBrush, QColor, QPen
from PyQt5 import Qt
from PyQt5 import QtCore
from PyQt5.QtCore import Qt as Qtc
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QSize, QPoint, QRect
from PyQt5.QtGui import QPalette
from threading import Lock

import sys

from gnuradio import gr
import pmt

class LabeledLevelGauge(QFrame):
    # Positions: 1 = above, 2=below, 3=left, 4=right
    def __init__(self, lbl='', barColor='blue', backgroundColor='white', fontColor='black', minValue=0, maxValue=100, maxSize=80, position=1, isVertical=True, isFloat=False,scaleFactor=1,showValue=False,parent=None):
        QFrame.__init__(self, parent)
        self.numberControl = LevelGauge(barColor, backgroundColor, minValue, maxValue, maxSize, isVertical, isFloat,scaleFactor,showValue,parent)
        
        #if (isVertical):
        #    self.numberControl.setAlignment(Qtc.AlignCenter)
        
        if position < 3:
            layout =  QVBoxLayout()
        else:
            layout = QHBoxLayout()
            
        self.lbl = lbl
        self.showvalue = showValue
        self.isFloat = isFloat
        self.isVertical = isVertical
        self.scaleFactor = scaleFactor
        
        self.lblcontrol = QLabel(lbl, self)
        self.lblcontrol.setAlignment(Qtc.AlignCenter)

        # For whatever reason, the progressbar doesn't show the number in the bar if it's vertical, only if it's horizontal
        if self.showvalue and (isFloat or self.isVertical):        
            textstr = self.buildTextStr(minValue/self.scaleFactor)
            self.lblcontrol.setText(textstr)
            
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
        if (not self.showvalue):
            return 
        
        if self.isFloat or self.isVertical:
            if len(self.lbl) > 0:
                textstr = self.buildTextStr(newValue)
                self.lblcontrol.setText(textstr)
            
    def setValue(self,newValue):
        self.valChanged(newValue)
        
        if int(self.scaleFactor) != 1:
            newValue = int(newValue * self.scaleFactor)
            
        self.numberControl.setValue(newValue)
        
class LevelGauge(QProgressBar):

    # Notifies to avoid thread conflicts on paints
    updateInt = pyqtSignal(int)
    updateFloat = pyqtSignal(float)
            
    def __init__(self, barColor='blue', backgroundColor='white', minValue=0, maxValue=100, maxSize=80, isVertical=True, isFloat=False,scaleFactor=1,showValue=False,parent=None):
        super().__init__(parent)

        
        #super().setPixmap(QtGui.QPixmap(":/icons/led-red-on.png"))
        #super().setScaledContents(True)

        self.updateInt.connect(self.onUpdateInt)
        self.updateFloat.connect(self.onUpdateFloat)
        
        self.lock = Lock()
        
        self.maxSize = maxSize

        p = super().palette()
        
        if (backgroundColor != 'default'):
            p.setColor(QPalette.Base, QColor(backgroundColor));
            
        if (barColor != 'default'):
            p.setColor(QPalette.Highlight, QColor(barColor));
            
        if backgroundColor != 'default' or barColor != 'default':
            super().setPalette(p)
          
        if (not isFloat) and showValue:
            # print("Showing value")
            super().setFormat("%v")  # This shows the number in the bar itself.
            super().setTextVisible(True)
        else:
            super().setTextVisible(False)
            # super().setFormat("")  # This shows the number in the bar itself.
        
        super().setMinimum(minValue)
        super().setMaximum(maxValue)
        
        if isVertical:
            super().setOrientation(Qtc.Vertical)
        else:
            super().setOrientation(Qtc.Horizontal)
            
    def onUpdateInt(self,newValue): 
        if newValue > super().maximum():
            newValue = super().maximum()
        elif newValue < super().minimum():
            newValue = super().minimum()
            
        self.lock.acquire()
        super().setValue(newValue)
        self.lock.release()
                                 
    def onUpdateFloat(self,newValue): 
        if newValue > super().maximum():
            newValue = super().maximum()
        elif newValue < super().minimum():
            newValue = super().minimum()
            
        self.lock.acquire()
        super().setValue(newValue)
        self.lock.release()
                                 
    def setValue(self,newValue):
        if (type(newValue) == int):
            self.updateInt.emit(newValue)
        else:
            self.updateFloat.emit(newValue)
            

class GrLevelGauge(gr.sync_block, LabeledLevelGauge):
    def __init__(self, lbl='', barColor='blue', backgroundColor='white', fontColor='black', minValue=0, maxValue=100, maxSize=80, isVertical=True, position=1, isFloat=False,scaleFactor=1,showValue=False, parent=None):
        gr.sync_block.__init__(self, name = "LevelGauge", in_sig = None, out_sig = None)
        LabeledLevelGauge.__init__(self, lbl, barColor, backgroundColor, fontColor, minValue, maxValue, maxSize, position, isVertical, isFloat,scaleFactor,showValue,parent)
        self.lbl = lbl
        
        if (minValue > maxValue):
            print("[LevelGauge] ERROR: min value is greater than max value.")
            sys.exit(1)
            
        self.message_port_register_in(pmt.intern("value"))
        self.set_msg_handler(pmt.intern("value"), self.msgHandler)   


    def msgHandler(self, msg):
        try:    
            newVal = pmt.to_python(pmt.cdr(msg))

            if type(newVal) == float or type(newVal) == int:
                    super().setValue(newVal)
            else:
                print("[LevelGauge] Error: Value received was not an int or a float: %s" % str(e))
                
        except Exception as e:
            print("[LevelGauge] Error with message conversion: %s" % str(e))

        
    def setValue(self,newValue):
        super().setValue(newValue)
        
