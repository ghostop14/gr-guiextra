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
import math

from gnuradio import gr
import pmt

class AzElPlot(gr.sync_block, FigureCanvas):
    def __init__(self, lbl, backgroundColor, dotColor, Parent=None, width=4, height=4, dpi=90):
        gr.sync_block.__init__(self, name = "MsgPushButton", in_sig = None, out_sig = None)
        
        self.lbl = lbl
        
        self.message_port_register_in(pmt.intern("azel"))
        self.set_msg_handler(pmt.intern("azel"), self.msgHandler)   

        self.dotColor = dotColor
        self.backgroundColor = backgroundColor
        self.scaleColor = 'black'
        if (self.backgroundColor == 'black'):
            self.scaleColor = 'white'
            
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig.patch.set_facecolor(self.backgroundColor)
        # "axisbg was deprecated, use facecolor instead"
        # self.axes = self.fig.add_subplot(111, polar=True, axisbg=self.backgroundColor)
        self.axes = self.fig.add_subplot(111, polar=True, facecolor=self.backgroundColor)
        # Angle: np.linspace(0, 2*np.pi, 90)
        # Radius: np.ones(100)*5
        # ax.plot(np.linspace(0, 2*np.pi, 90), np.ones(90)*5, color='r', linestyle='-')
        # Each of these use 90 points.  linespace creates the angles 0-2 PI with 90 points
        # np.ones creates a 90 point array filled with 1's then multiplies that by the scalar 5

        # Create an "invisible" line at 90 to set the max for the plot
        self.axes.plot(np.linspace(0, 2*np.pi, 90), np.ones(90)*90, color=self.scaleColor, linestyle='')

        # Plot line: Initialize out to 90 and blank
        radius = 90
        self.blackline = self.axes.plot(np.linspace(0, 2*np.pi, 90), np.ones(90)*radius, color=self.scaleColor, linestyle='-')
        self.reddot = None

        # Rotate zero up
        self.axes.set_theta_zero_location("N")

        # Set limits:
        self.axes.set_rlim(0,90)
        
        # self.axes.set_yticklabels(ticklabels, color=self.dotColor)
        self.axes.set_yticklabels([], color=self.scaleColor)
        self.axes.set_xticklabels([], color=self.scaleColor)
        # plt.show()
        # -----------------------------------------------------------
        FigureCanvas.__init__(self, self.fig)
        self.setParent(Parent)


        self.title  = self.fig.suptitle(self.lbl, fontsize=8, fontweight='bold', color='black')

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def msgHandler(self, msg):
        try:    
            newVal = pmt.to_python(pmt.car(msg))

            if type(newVal) == dict:
                if 'az' in newVal and 'el' in newVal:
                    # print("Received az/el: " + str(newVal['az']) + " " + str(newVal['el']))
                    self.updateData(newVal['az'],newVal['el'])
                else:
                    print("[AzElPlot] Error: az and el keys were not found in the dictionary.")
            else:
                print("[AzElPlot] Error: Value received was not a dictionary.  Expecting a dictionary in the car message component with az and el keys.")
                
        except Exception as e:
            print("[AzElPlot] Error with message conversion: %s" % str(e))
        
    def updateData(self, azimuth, elevation):
        if self.reddot is not None:
            self.reddot.pop(0).remove()
            
        # Plot is angle, radius where angle is in radians
        
        if (elevation > 0):
            # Need to reverse elevation.  90 degrees is center (directly overhead), and 90 degrees is horizon.
            if (elevation > 90.0):
                elevation = 90.0
                
            convertedElevation = 90.0 - elevation
            # Note: +azimuth for the plot is measured counter-clockwise, so need to reverse it.
            self.reddot = self.axes.plot(-azimuth * math.pi/180.0,convertedElevation,self.dotColor)
            # self.reddot = self.axes.plot(-azimuth * math.pi/180.0,convertedElevation,'ro')

        self.draw()
        
