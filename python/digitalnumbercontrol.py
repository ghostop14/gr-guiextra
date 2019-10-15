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

from PyQt5.QtWidgets import QFrame,  QVBoxLayout, QWidget,  QLabel
from PyQt5.QtGui import QPainter, QPixmap,  QFont,  QFontMetrics, QBrush, QColor
from PyQt5.QtCore import Qt, QSize
from PyQt5 import QtCore
from PyQt5.QtCore import Qt as Qtc
from PyQt5.QtCore import pyqtSignal

from gnuradio import gr
import pmt

# -------------- Support Classes ---------------------------------
#
#

class LabeledDigitalNumberControl(QFrame):
    def __init__(self, lbl = '', minFreqHz = 0, maxFreqHz=6000000000, parent=None,  ThousandsSeparator=',', backgroundColor='black', fontColor='white', clickCallback=None):
        QFrame.__init__(self, parent)
        self.numberControl = DigitalNumberControl(minFreqHz, maxFreqHz, self, ThousandsSeparator, backgroundColor, fontColor, clickCallback)
        
        layout =  QVBoxLayout()

        self.lbl = QLabel(lbl, self)
        if len(lbl) > 0:
            self.hasLabel = True
            layout.addWidget(self.lbl)
        else:
            self.hasLabel = False

        layout.addWidget(self.numberControl)
        layout.setAlignment(Qtc.AlignCenter | Qtc.AlignVCenter)
        self.setLayout(layout)
        self.show()
        
    def minimumSizeHint(self):
        if (self.hasLabel):
            return QSize(self.numberControl.minimumWidth()+10, 100)
        else:
            return QSize(self.numberControl.minimumWidth()+10, 50)

    def setReadOnly(self,bReadOnly):
        self.numberControl.setReadOnly(bReadOnly)
        
    def setFrequency(self, newFreq):
        self.numberControl.setFrequency(newFreq)
        
    def getFrequency(self):
        return self.numberControl.getFrequency()
        
class DigitalNumberControl(QFrame):
    # Notifies to avoid thread conflicts on paints
    updateInt = pyqtSignal(int)
    updateFloat = pyqtSignal(float)
    
    def __init__(self, minFreqHz = 0, maxFreqHz=6000000000, parent=None,  ThousandsSeparator=',', backgroundColor='black', fontColor='white', clickCallback=None):
        QFrame.__init__(self, parent)
        
        self.updateInt.connect(self.onUpdateInt)
        self.updateFloat.connect(self.onUpdateFloat)
        
        self.minFreq = int(minFreqHz)
        self.maxFreq = int(maxFreqHz)
        self.numDigitsInFreq = len(str(maxFreqHz))
 
        self.ThousandsSeparator = ThousandsSeparator
        self.clickCallback = clickCallback
        
        # See https://doc.qt.io/archives/qt-4.8/qframe.html for a description
        #self.setLineWidth(2)
        #self.setMidLineWidth(0)
        #self.setFrameStyle(QFrame.Sunken)
        #self.setContentsMargins(2,2,2,2)

        #self.setStyleSheet("border: 2;border-style: inset;")
        
        self.readOnly = False
                    
        # self.setColors(Qt.black, Qt.white)
        self.setColors(QColor(backgroundColor), QColor(fontColor))
        self.numberFont = QFont("Arial", 12, QFont.Normal)

        self.curFreq = minFreqHz
        
        self.debugClick = False
        
        # Determine what our width minimum is
        teststr = ""
        for i in range(0,self.numDigitsInFreq):
            teststr += "0"
            
        fm = QFontMetrics(self.numberFont)
        if len(self.ThousandsSeparator) > 0:
            # The -1 makes sure we don't count an extra for 123,456,789.  Answer should be 2 not 3.
            numgroups = int(float(self.numDigitsInFreq-1) / 3.0)
            if (numgroups > 0):
                for i in range(0,numgroups):
                    teststr += self.ThousandsSeparator
                    
            textstr = teststr
        else:
            textstr = teststr

        width=fm.horizontalAdvance(textstr)
        
        self.minwidth = width
        # print("min width: " + str(width))
        if (self.minwidth < 410):
            self.minwidth = 410
            
        self.setMaximumHeight(70)
        self.setMinimumWidth(self.minwidth)
        # Show the control
        self.show()
        
    def minimumSizeHint(self):
        return QSize(self.minwidth, 50)

    def setReadOnly(self,bReadOnly):
        self.readOnly = bReadOnly
        
    def mousePressEvent(self, event):
        super(DigitalNumberControl, self).mousePressEvent(event)
        self.offset = event.pos()
        
        if self.readOnly:
            return
        
        fm = QFontMetrics(self.numberFont)
        
        if len(self.ThousandsSeparator) > 0:
            if self.ThousandsSeparator != ".":
                textstr = format(self.getFrequency(), self.ThousandsSeparator)
            else:
                textstr = format(self.getFrequency(), ",")
                textstr = textstr.replace(",",".")
        else:
            textstr = str(self.getFrequency())

        width=fm.horizontalAdvance(textstr)
        
        # So we know:
        # - the width of the text
        # - The mouse click position relative to 0 (pos relative to string start will be size().width() - 2 - pos.x

        clickpos = self.size().width() - 2 - self.offset.x()

        foundNumber = False
        clickedThousands = False
        for i in range(1, len(textstr)+1):
            #width = fm.horizontaladvance(textstr[-i:])
            #widthchar = fm.horizontaladvance(textstr[-i:-i+1])
            width = fm.width(textstr[-i:])
            charstr = textstr[-i:]
            widthchar = fm.width(charstr[0])
            if clickpos >= (width-widthchar) and clickpos <=width:
                clickedChar = i-1
                
                clickedNumIndex = clickedChar
                
                foundNumber = True

                if len(self.ThousandsSeparator) > 0:
                    if charstr[0] != self.ThousandsSeparator:
                        numSeps = charstr.count(self.ThousandsSeparator)
                        clickedNumIndex -= numSeps
                        if self.debugClick:
                            print("clicked number: " + str(clickedNumIndex))
                    else:
                        clickedThousands = True
                        if self.debugClick:
                            print("clicked thousands separator")
                else:
                        if self.debugClick:
                            print("clicked number: " + str(clickedChar))
                
                # Remember y=0 is at the top so this is reversed
                clickedUp = False
                if (self.offset.y() > self.size().height()/2):
                    if self.debugClick:
                        print('clicked down')
                else:
                    if self.debugClick:
                        print('clicked up')
                    clickedUp = True
                    
                if not clickedThousands:
                    curFreq = self.getFrequency()
                    increment = pow(10, clickedNumIndex)
                    if (clickedUp):
                        curFreq += increment
                    else:
                        curFreq -= increment
                        
                    self.setFrequency(curFreq)
                    if (self.clickCallback is not None):
                        # print("calling click callback")
                        self.clickCallback(self.getFrequency())
                
                break
            
        if (not foundNumber) and (not clickedThousands):
            # See if we clicked in the high area, if so, increment there.
            clickedUp = False
            if (self.offset.y() > self.size().height()/2):
                if self.debugClick:
                    print('clicked down in the high area')
            else:
                if self.debugClick:
                    print('clicked up in the high area')
                clickedUp = True
                
            textstr = str(self.getFrequency())
            numNumbers = len(textstr)
            increment = pow(10, numNumbers)
            curFreq = self.getFrequency()
            if (clickedUp):
                curFreq += increment
            else:
                curFreq -= increment
                
            self.setFrequency(curFreq)
            if (self.clickCallback is not None):
                # print("calling click callback")
                self.clickCallback(self.getFrequency())
            
    def setColors(self, background, fontColor):
        self.backgroundColor = background
        self.fontColor = fontColor
        
    def reverseString(self, astring): 
        astring = astring[::-1] 
        return astring 
        
    def onUpdateInt(self,newFreq): 
        if (newFreq >= self.minFreq) and (newFreq <= self.maxFreq): 
            self.curFreq = int(newFreq)
            
        #print("Setting frequency: " + str(newFreq))
        self.update()
                                 
    def onUpdateFloat(self,newFreq): 
        if (newFreq >= self.minFreq) and (newFreq <= self.maxFreq): 
            self.curFreq = int(newFreq)
            
        #print("Setting frequency: " + str(newFreq))
        self.update()
        
    def setFrequency(self, newFreq):
        if (type(newFreq) == int):
            self.updateInt.emit(newFreq)
        else:
            self.updateFloat.emit(newFreq)
        
    def getFrequency(self):
        return self.curFreq

    def resizeEvent(self, event):
        self.pxMap = QPixmap(self.size())
        self.pxMap.fill(self.backgroundColor)
        
        self.update()
        
    def paintEvent(self, event):
        super().paintEvent(event)
        
        painter = QPainter(self)
        
        #self.painter.setPen(self.backgroundColor)
        size = self.size()
        brush = QBrush()
        brush.setColor(self.backgroundColor)
        brush.setStyle(Qt.SolidPattern)
        rect = QtCore.QRect(2, 2, size.width()-4, size.height()-4)
        #rect = QtCore.QRect(0, 0, size.width(), size.height())
        painter.fillRect(rect, brush)

        self.numberFont.setPixelSize(0.9 * size.height())
        painter.setFont(self.numberFont)
        painter.setPen(self.fontColor)
        rect = event.rect()
        
        if len(self.ThousandsSeparator) > 0:
            if self.ThousandsSeparator != ".":
                textstr = format(self.getFrequency(), self.ThousandsSeparator)
            else:
                textstr = format(self.getFrequency(), ",")
                textstr = textstr.replace(",",".")
        else:
            textstr = str(self.getFrequency())
        rect = QtCore.QRect(0, 0, size.width()-4, size.height())
        #painter.drawText(event.rect(), Qt.AlignRight + Qt.AlignVCenter,  textstr)
        painter.drawText(rect, Qt.AlignRight + Qt.AlignVCenter,  textstr)
        
# ################################################################################

# GNU Radio Class
class MsgDigitalNumberControl(gr.sync_block, LabeledDigitalNumberControl):
    def __init__(self, lbl = '', minFreqHz = 0, maxFreqHz=6000000000, parent=None,  ThousandsSeparator=',', backgroundColor='black', fontColor='white',varCallback=None):
        gr.sync_block.__init__(self, name = "MsgDigitalNumberControl", in_sig = None, out_sig = None)
        LabeledDigitalNumberControl.__init__(self,lbl,minFreqHz,maxFreqHz,parent,ThousandsSeparator,backgroundColor, fontColor, self.clickCallback)

        self.varCallback = varCallback
                
        self.message_port_register_in(pmt.intern("valuein"))
        self.set_msg_handler(pmt.intern("valuein"), self.msgHandler)   
        self.message_port_register_out(pmt.intern("valueout"))

    def msgHandler(self, msg):
        try:    
            newVal = pmt.to_python(pmt.cdr(msg))

            if type(newVal) == float or type(newVal) == int:
                self.callVarCallback(newVal)

                self.setValue(newVal)
            else:
                print("[Digital Number Control] Error: Value received was not an int or a float: %s" % str(e))
                
        except Exception as e:
            print("[Digital Number Control] Error with message conversion: %s" % str(e))
        
    def callVarCallback(self,newValue):
        if (self.varCallback is not None):
            # print('Calling var callback with ' + str(newValue))
            
            if type(self.varCallback) is float:
                self.varCallback = float(newValue)
            else:
                self.varCallback(float(newValue))
        
    def clickCallback(self,newValue):
        # print("click callback called")
        self.callVarCallback(newValue)

        self.message_port_pub(pmt.intern("valueout"),pmt.cons( pmt.intern("value"), pmt.from_float(float(newValue)) ))
        
    def setValue(self,newVal):
        self.setFrequency(newVal)
        
        self.message_port_pub(pmt.intern("valueout"),pmt.cons( pmt.intern("value"), pmt.from_float(float(self.getFrequency())) ))
        
    def getValue(self):
        self.getFrequency()

    def setReadOnly(self,bReadOnly):
        super().setReadOnly(bReadOnly)
        
