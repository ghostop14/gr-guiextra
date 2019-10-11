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
from PyQt5 import QtWidgets
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from gnuradio import gr
import pmt

class DistanceRadar(gr.sync_block, FigureCanvas):
    def __init__(self, lbl, ticklabels, backgroundColor, fontColor, ringColor, Parent=None, width=4, height=4, dpi=100):
        gr.sync_block.__init__(self, name = "MsgPushButton", in_sig = None, out_sig = None)
        
        self.lbl = lbl
        
        self.message_port_register_in(pmt.intern("radius"))
        self.set_msg_handler(pmt.intern("radius"), self.msgHandler)   

        self.fontColor = fontColor
        self.backgroundColor = backgroundColor
        self.ringColor = ringColor
        
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig.patch.set_facecolor(self.backgroundColor)
        # "axisbg was deprecated, use facecolor instead"
        # self.axes = self.fig.add_subplot(111, polar=True, axisbg=self.backgroundColor)
        self.axes = self.fig.add_subplot(111, polar=True, facecolor=self.backgroundColor)
        # Angle: np.linspace(0, 2*np.pi, 100)
        # Radius: np.ones(100)*5
        # ax.plot(np.linspace(0, 2*np.pi, 100), np.ones(100)*5, color='r', linestyle='-')
        # Each of these use 100 points.  linespace creates the angles 0-2 PI with 100 points
        # np.ones creates a 100 point array filled with 1's then multiplies that by the scalar 5

        # Create an "invisible" line at 100 to set the max for the plot
        self.axes.plot(np.linspace(0, 2*np.pi, 100), np.ones(100)*100, color=self.fontColor, linestyle='')

        # Plot line: Initialize out to 100 and blank
        radius = 100
        self.blackline = self.axes.plot(np.linspace(0, 2*np.pi, 100), np.ones(100)*radius, color=self.fontColor, linestyle='-')
        self.redline = None

        # Plot a filled circle
        # http://nullege.com/codes/search/matplotlib.pyplot.Circle
        # Params are: Cartesian coord of center, radius, etc...
        # circle = plt.Circle((0.0, 0.0), radius, transform=self.axes.transData._b, color="red", alpha=0.4)
        # self.filledcircle = self.axes.add_artist(circle)
        self.filledcircle = None
        # Create bullseye
        circle = plt.Circle((0.0, 0.0), 20, transform=self.axes.transData._b, color=self.fontColor, alpha=0.4)
        self.bullseye = self.axes.add_artist(circle)

        # Rotate zero up
        self.axes.set_theta_zero_location("N")

        self.axes.set_yticklabels(ticklabels, color=self.fontColor)
        self.axes.set_xticklabels([], color=self.fontColor)
        # plt.show()
        # -----------------------------------------------------------
        FigureCanvas.__init__(self, self.fig)
        self.setParent(Parent)


        self.title  = self.fig.suptitle(self.lbl, fontsize=8, fontweight='bold', color=self.fontColor)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def msgHandler(self, msg):
        try:    
            newVal = pmt.to_python(pmt.cdr(msg))

            if type(newVal) == float or type(newVal) == int:
                self.updateData(newVal)
            else:
                print("[DistanceRadar] Error: Value received was not an int or a float: %s" % str(e))
                
        except Exception as e:
            print("[DistanceRadar] Error with message conversion: %s" % str(e))
        
    def updateData(self, radius):
        if self.redline is not None:
            self.redline.pop(0).remove()
        self.redline = self.axes.plot(np.linspace(0, 2*np.pi, 100), np.ones(100)*radius, color='r', linestyle='-')

        if self.filledcircle:
            self.filledcircle.remove()
            
        self.bullseye.remove()
        circle = plt.Circle((0.0, 0.0), radius, transform=self.axes.transData._b, color=self.ringColor, alpha=0.4)
        self.filledcircle = self.axes.add_artist(circle)
        # Create bullseye
        circle = plt.Circle((0.0, 0.0), 20, transform=self.axes.transData._b, color=self.fontColor, alpha=0.4)
        self.bullseye = self.axes.add_artist(circle)
        
        self.draw()
        
