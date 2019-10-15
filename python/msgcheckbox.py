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
from PyQt5.QtWidgets import QFrame, QVBoxLayout
from PyQt5.QtCore import Qt as Qtc

from gnuradio import gr
import pmt

class CheckBoxEx(Qt.QCheckBox):
    def __init__(self, lbl, callback=None):
        Qt.QCheckBox.__init__(self)
        self.setText(lbl)
        self.callback = callback

        self.stateChanged.connect(self.onToggleClicked)
        
    def onToggleClicked(self):
        if self.callback is not None:
            self.callback(super().isChecked())

class MsgCheckBox(gr.sync_block, QFrame):
    def __init__(self, callback, lbl, pressedReleasedDict, initPressed, alignment, valignment,outputmsgname='value'):
        gr.sync_block.__init__(self, name = "MsgCheckBox", in_sig = None, out_sig = None)
        QFrame.__init__(self)
                        
        self.outputmsgname = outputmsgname
        self.chkBox = CheckBoxEx(lbl, self.onToggleClicked)
        
        layout =  QVBoxLayout()
        
        layout.addWidget(self.chkBox)

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
        self.setLayout(layout)
        
        self.callback = callback
        self.pressReleasedDict = pressedReleasedDict
        
        self.message_port_register_out(pmt.intern("state"))

        if initPressed:
            self.chkctl.setChecked(True)
        
        self.show()
        
    def onToggleClicked(self, checked):
        if self.chkBox.isChecked():
            self.callback(self.pressReleasedDict['Pressed'])
            
            if type(self.pressReleasedDict['Pressed']) == bool:
                self.message_port_pub(pmt.intern("state"),pmt.cons( pmt.intern(self.outputmsgname), pmt.from_bool(self.pressReleasedDict['Pressed']) ))
            elif type(self.pressReleasedDict['Pressed']) == int:
                self.message_port_pub(pmt.intern("state"),pmt.cons( pmt.intern(self.outputmsgname), pmt.from_long(self.pressReleasedDict['Pressed']) ))
            elif type(self.pressReleasedDict['Pressed']) == float:
                self.message_port_pub(pmt.intern("state"),pmt.cons( pmt.intern(self.outputmsgname), pmt.from_float(self.pressReleasedDict['Pressed']) ))
            else:
                self.message_port_pub(pmt.intern("state"),pmt.cons( pmt.intern(self.outputmsgname), pmt.intern(self.pressReleasedDict['Pressed']) ))
        else:
            self.callback(self.pressReleasedDict['Released'])

            if type(self.pressReleasedDict['Released']) == bool:
                self.message_port_pub(pmt.intern("state"),pmt.cons( pmt.intern(self.outputmsgname), pmt.from_bool(self.pressReleasedDict['Released']) ))
            elif type(self.pressReleasedDict['Released']) == int:
                self.message_port_pub(pmt.intern("state"),pmt.cons( pmt.intern(self.outputmsgname), pmt.from_long(self.pressReleasedDict['Released']) ))
            elif type(self.pressReleasedDict['Released']) == float:
                self.message_port_pub(pmt.intern("state"),pmt.cons( pmt.intern(self.outputmsgname), pmt.from_float(self.pressReleasedDict['Released']) ))
            else:
                self.message_port_pub(pmt.intern("state"),pmt.cons( pmt.intern(self.outputmsgname), pmt.intern(self.pressReleasedDict['Released']) ))
