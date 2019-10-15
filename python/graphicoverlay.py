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
import sys
import threading
import time

from gnuradio import gr
import pmt

# This thread just gets us out of the sync_block's init function so the messaging system and scheduler are active.
class offloadThread(threading.Thread):
  def __init__(self, callback, overlayList,listDelay,repeat):
    threading.Thread.__init__(self)
    self.callback = callback
    self.overlayList = overlayList
    self.listDelay = listDelay
    self.threadRunning = False
    self.stopThread = False
    self.repeat = repeat
    
  def run(self):
    self.stopThread = False
    self.threadRunning = True
    
    # Wait for main __init__ to finish
    time.sleep(0.5) 
    
    if (type(self.overlayList) == list and self.listDelay > 0.0):
        while self.repeat and not self.stopThread:
            for curItem in self.overlayList:
                self.callback(curItem)
    
                if self.stopThread:
                    break
                            
                time.sleep(self.listDelay)
    
                if self.stopThread:
                    break
    else:
        self.callback(self.overlayList)
        
    self.threadRunning = False

class GrGraphicOverlay(gr.sync_block):
    def __init__(self,overlayList, listDelay, repeat):
        gr.sync_block.__init__(self, name = "GrGraphicsOverlay", in_sig = None, out_sig = None)

        self.overlayList = overlayList
        self.listDelay = listDelay
        if type(self.overlayList) is not dict and type(self.overlayList) is not list:
            print("[GrGraphicsOverlay] Error: the specified input is not valid.  Please specify either a dictionary item with the following keys: 'filename','x','y'[,'scalefactor'] or a list of dictionary items.")
            sys.exit(1)
            
        self.message_port_register_out(pmt.intern("overlay"))

        self.thread = offloadThread(self.overlayCallback,self.overlayList, listDelay, repeat)
        self.thread.start()

    def overlayCallback(self,msgData):
        # Need to let init finish before this can be called so need to thread it out.
        meta = pmt.to_pmt(msgData)
        pdu = pmt.cons(meta,pmt.PMT_NIL)
        self.message_port_pub(pmt.intern('overlay'), pdu)

    def stop(self):
        self.thread.stopThread = True
        
        while self.thread.threadRunning:
            time.sleep(0.1)

        return True
    