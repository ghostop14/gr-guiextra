#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Test Distance Radar
# GNU Radio version: 3.8.0.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import guiextra
from gnuradio import qtgui

class test_distanceradar(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Test Distance Radar")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Test Distance Radar")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "test_distanceradar")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000

        ##################################################
        # Blocks
        ##################################################
        self.variable_qtgui_msg_push_button_0_0_0 = _variable_qtgui_msg_push_button_0_0_0_toggle_button = guiextra.MsgPushButton('75%', 'radius', 75)
        self.variable_qtgui_msg_push_button_0_0_0 = _variable_qtgui_msg_push_button_0_0_0_toggle_button

        self.top_grid_layout.addWidget(_variable_qtgui_msg_push_button_0_0_0_toggle_button, 2, 0, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.variable_qtgui_msg_push_button_0_0 = _variable_qtgui_msg_push_button_0_0_toggle_button = guiextra.MsgPushButton('50%', 'radius', 50)
        self.variable_qtgui_msg_push_button_0_0 = _variable_qtgui_msg_push_button_0_0_toggle_button

        self.top_grid_layout.addWidget(_variable_qtgui_msg_push_button_0_0_toggle_button, 1, 0, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.variable_qtgui_msg_push_button_0 = _variable_qtgui_msg_push_button_0_toggle_button = guiextra.MsgPushButton('25%', 'radius', 25)
        self.variable_qtgui_msg_push_button_0 = _variable_qtgui_msg_push_button_0_toggle_button

        self.top_grid_layout.addWidget(_variable_qtgui_msg_push_button_0_toggle_button, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.variable_qtgui_distanceradar_0 = _distance_radar_variable_qtgui_distanceradar_0 = guiextra.DistanceRadar('', ['20', '40', '60', '80', '100'], "black", "white", "red", self)
        self.variable_qtgui_distanceradar_0 = _distance_radar_variable_qtgui_distanceradar_0

        self.top_grid_layout.addWidget(_distance_radar_variable_qtgui_distanceradar_0)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_null_source_0 = blocks.null_source(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.variable_qtgui_msg_push_button_0, 'pressed'), (self.variable_qtgui_distanceradar_0, 'radius'))
        self.msg_connect((self.variable_qtgui_msg_push_button_0_0, 'pressed'), (self.variable_qtgui_distanceradar_0, 'radius'))
        self.msg_connect((self.variable_qtgui_msg_push_button_0_0_0, 'pressed'), (self.variable_qtgui_distanceradar_0, 'radius'))
        self.connect((self.blocks_null_source_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_null_sink_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "test_distanceradar")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)



def main(top_block_cls=test_distanceradar, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()
    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
