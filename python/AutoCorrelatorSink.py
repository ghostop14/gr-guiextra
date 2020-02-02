#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2019 ghostop14.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

from gnuradio import gr
from gnuradio import qtgui
from gnuradio import blocks, fft, filter
import math

import sip
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget

class Normalize(gr.hier_block2):
    def __init__(self, vecsize=1024):
        gr.hier_block2.__init__(
            self, "Normalize",
            gr.io_signature(1, 1, gr.sizeof_float*vecsize),
            gr.io_signature(1, 1, gr.sizeof_float*vecsize),
        )

        ##################################################
        # Parameters
        ##################################################
        self.vecsize = vecsize

        ##################################################
        # Blocks
        ##################################################
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_float, vecsize)
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_float, vecsize)
        self.blocks_max_xx_0 = blocks.max_ff(vecsize)
        self.blocks_divide_xx_0 = blocks.divide_ff(vecsize)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_divide_xx_0, 0), (self, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.blocks_divide_xx_0, 1))
        self.connect((self, 0), (self.blocks_max_xx_0, 0))
        self.connect((self.blocks_repeat_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.blocks_max_xx_0, 0), (self.blocks_repeat_0, 0))
        self.connect((self, 0), (self.blocks_divide_xx_0, 0))


    def get_vecsize(self):
        return self.vecsize

    def set_vecsize(self, vecsize):
        self.vecsize = vecsize

class AutoCorrelator(gr.hier_block2):
    """
    docstring for block AutoCorrelator
    """
    def __init__(self, sample_rate,  fac_size,fac_decimation,  useDB):
        gr.hier_block2.__init__(self,"AutoCorrelator",
            gr.io_signature(1, 1, gr.sizeof_gr_complex),  # Input signature
            gr.io_signature(1, 1, gr.sizeof_float*fac_size)) # Output signature

        self.fac_size = fac_size
        self.fac_decimation = fac_decimation
        self.sample_rate = sample_rate
            
        streamToVec = blocks.stream_to_vector(gr.sizeof_gr_complex, self.fac_size)
        # Make sure N is at least 1
        decimation =  int(self.sample_rate/self.fac_size/self.fac_decimation)
        self.one_in_n = blocks.keep_one_in_n(gr.sizeof_gr_complex * self.fac_size, max(1,decimation))

        # FFT Note: No windowing.
        fac = fft.fft_vcc(self.fac_size, True, ())

        complex2Mag = blocks.complex_to_mag(self.fac_size)
        self.avg = filter.single_pole_iir_filter_ff_make(1.0, self.fac_size)

        fac_fac   = fft.fft_vfc(self.fac_size, True, ())
        fac_c2mag = blocks.complex_to_mag_make(fac_size)

        # There's a note in Baz's block about needing to add 3 dB to each bin but the DC bin, however it was never implemented
        n = 20
        k =  -20*math.log10(self.fac_size)
        log = blocks.nlog10_ff_make(n, self.fac_size, k )

        if useDB:
            self.connect(self, streamToVec, self.one_in_n, fac, complex2Mag,  fac_fac, fac_c2mag, self.avg, log,  self)
        else:
            self.connect(self, streamToVec, self.one_in_n, fac, complex2Mag,  fac_fac, fac_c2mag, self.avg, self)

class AutoCorrelatorSink(gr.hier_block2):
    """
    docstring for block AutoCorrelatorSink
    """
    def __init__(self, sample_rate, fac_size, fac_decimation, title,  autoScale, grid, yMin, yMax,  useDB):
        gr.hier_block2.__init__(self,
            "AutoCorrelatorSink",
            gr.io_signature(1, 1, gr.sizeof_gr_complex),  # Input signature
            gr.io_signature(0, 0, 0)) # Output signature

        self.fac_size = fac_size
        self.fac_decimation = fac_decimation
        self.sample_rate = sample_rate
        
        autoCorr = AutoCorrelator(sample_rate, fac_size, fac_decimation,  useDB)
        vecToStream = blocks.vector_to_stream(gr.sizeof_float, self.fac_size)

        self.timeSink = qtgui.time_sink_f(self.fac_size/2, sample_rate, title, 1)
        self.timeSink.enable_grid(grid)
        self.timeSink.set_y_axis(yMin, yMax)
        self.timeSink.enable_autoscale(autoScale)
        self.timeSink.disable_legend()
        self.timeSink.set_update_time(0.1)

        if useDB:
            self.connect(self, autoCorr,  vecToStream,  self.timeSink)
        else:
            norm = Normalize(self.fac_size)
            self.connect(self, autoCorr,  norm,  vecToStream,  self.timeSink)

        #pyQt  = self.timeSink.pyqwidget()
        #self.pyWin = sip.wrapinstance(pyQt, QtGui.QWidget)
        # self.pyWin.show()

    def getWidget(self):
        return sip.wrapinstance(self.timeSink.pyqwidget(), QWidget)
