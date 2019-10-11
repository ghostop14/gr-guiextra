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

class MsgCheckBox(gr.sync_block, Qt.QCheckBox):
    def __init__(self, callback, lbl, pressedReleasedDict, initPressed):
        gr.sync_block.__init__(self, name = "MsgCheckBox", in_sig = None, out_sig = None)
        Qt.QCheckBox.__init__(self)
        self.lbl = lbl
        self.setText(lbl)
        self.callback = callback
        self.pressReleasedDict = pressedReleasedDict
        
        self.message_port_register_out(pmt.intern("state"))

        if initPressed:
            self.setChecked(True)
            self.state = 1
            self.callback(self.pressReleasedDict['Pressed'])
            # Note: You can't send the pmt message here in the constructor, it won't work.
        else:
            self.state = 0
        
        self.stateChanged.connect(self.onToggleClicked)
        
    def onToggleClicked(self):
        if self.isChecked():
            self.state = 1
            self.callback(self.pressReleasedDict['Pressed'])
        else:
            self.state = 0
            self.callback(self.pressReleasedDict['Released'])
        
        self.message_port_pub(pmt.intern("state"),pmt.cons( pmt.intern("state"), pmt.from_long(self.state) ))
        