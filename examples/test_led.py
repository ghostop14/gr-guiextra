#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Test LED Indicator
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

from PyQt5 import Qt
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import guiextra
from gnuradio import qtgui

class test_led(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Test LED Indicator")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Test LED Indicator")
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

        self.settings = Qt.QSettings("GNU Radio", "test_led")

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
        self.variable_qtgui_toggle_button_msg_0 = variable_qtgui_toggle_button_msg_0 = True
        self.samp_rate = samp_rate = 32000
        self.ledstate = ledstate = True

        ##################################################
        # Blocks
        ##################################################
        _ledstate_check_box = Qt.QCheckBox('Variable-based LED State')
        self._ledstate_choices = {True: True, False: False}
        self._ledstate_choices_inv = dict((v,k) for k,v in self._ledstate_choices.items())
        self._ledstate_callback = lambda i: Qt.QMetaObject.invokeMethod(_ledstate_check_box, "setChecked", Qt.Q_ARG("bool", self._ledstate_choices_inv[i]))
        self._ledstate_callback(self.ledstate)
        _ledstate_check_box.stateChanged.connect(lambda i: self.set_ledstate(self._ledstate_choices[bool(i)]))
        self.top_grid_layout.addWidget(_ledstate_check_box, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._variable_qtgui_toggle_button_msg_0_choices = {'Pressed': True, 'Released': False}
        _variable_qtgui_toggle_button_msg_0_toggle_button = guiextra.ToggleButton(self.set_variable_qtgui_toggle_button_msg_0, 'Msg Based State', self._variable_qtgui_toggle_button_msg_0_choices, True)
        _variable_qtgui_toggle_button_msg_0_toggle_button.setColors("default","default","default","default")
        self.variable_qtgui_toggle_button_msg_0 = _variable_qtgui_toggle_button_msg_0_toggle_button

        self.top_grid_layout.addWidget(_variable_qtgui_toggle_button_msg_0_toggle_button, 0, 1, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.guiextra_ledindicator_0 = self._guiextra_ledindicator_0_win = guiextra.GrLEDIndicator("State", "green", "red", ledstate, 40, 1, self)
        self._guiextra_ledindicator_0_win = self._guiextra_ledindicator_0_win
        self.top_grid_layout.addWidget(self._guiextra_ledindicator_0_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_null_source_0 = blocks.null_source(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.variable_qtgui_toggle_button_msg_0, 'state'), (self.guiextra_ledindicator_0, 'state'))
        self.connect((self.blocks_null_source_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_null_sink_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "test_led")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_variable_qtgui_toggle_button_msg_0(self):
        return self.variable_qtgui_toggle_button_msg_0

    def set_variable_qtgui_toggle_button_msg_0(self, variable_qtgui_toggle_button_msg_0):
        self.variable_qtgui_toggle_button_msg_0 = variable_qtgui_toggle_button_msg_0

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)

    def get_ledstate(self):
        return self.ledstate

    def set_ledstate(self, ledstate):
        self.ledstate = ledstate
        self._ledstate_callback(self.ledstate)
        self.guiextra_ledindicator_0.setState(self.ledstate)



def main(top_block_cls=test_led, options=None):

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
