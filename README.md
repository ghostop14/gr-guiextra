# gr-guiextra
Modern and enhanced GUI widgets for GNU Radio 3.8+

## Overview

This OOT module set provides modernized and new GUI control capabilities for GNU Radio 3.8+.  The following blocks are currently implemented in this set:

**Fast Auto-correlator** - This is a QT GUI ported version of the old WX-based Fast Auto-correlator.  This conversion makes this block GR 3.8/3.9-available.

**Compass** - Provides an on-screen compass with 3 different choices for the needle (full, half, and -pi to pi with DoA uncertainty)

**Dial** - Think of this as your volume dial control.  Supports both variables and messages.

**Digital Number Control (Frequency Control)** - Very similar to SDR-based stand-alone applications, clicking the numbers can adjust frequency, or it can be set in read-only mode for display only.  Supports both controlling a variable and input / output messages.

**LED Indicator** - Just as it sounds.  On-screen LED.  You can choose the on/off colors and supports both variables and messages to control state.

**Linear Gauge (Progress Bar)** - Linear progress bar / linear gauge, either horizontal or vertical.  Colors can be chosen for the background and the bar, and it is controllable via variable or message.

**Dial Gauge** - Circular guage.  Colors can be chosen for the background and the bar, and it is controllable via variable or message.

**Toggle Button** - Push to hold down.  Push again to release.  Both variables and messages available.

**Toggle Button** - Modern toggle switch.  Both variables and messages available.

**Message-based Checkbox** - Like a standard checkbox, but both variables and messages available.

**Message Pushbutton** - Produce a message when the button is pushed.  (This is different than the toggle in that this bounces back to release like a traditional button when pressed and a message is only produced on press).

**Graphics Item** - Drop a graphic anywhere in your GNU Radio app screen.  You can also control the file based on input messages to change the graphic on the fly.  This can be tied to the toggle switch, button, etc. to control the image displayed based on other factors for a more dynamic display.  This control also supports the concept of overlays where additional images can be dynamically add/update/deleted from the main graphic which also allows for dynamic animation via message.  Overlay messages should be in the car portion of the message and can be a dictionary with the following keys: filename (full path), x, y, and an optional scalefactor.  A list of dictionaries can also be sent.  Overlays are keyed by filename so passing updates to x/y for an overlay will update it.  Setting any overlay file to x/y -1,-1 will remove it.

**App Background** - While stylesheets can be used to change an app, that can be cumbersome if all you want is to change the background color or display a background graphic.  This drop-in control lets you do either or both.

**Azimuth-Elevation Plot** - Similar to the Az/El plot in satellite trackers, this widget produces a similar screen that can be fed from gpredict-doppler's rotor block that outputs an az_el message.  This UI block is looking for a dictionary in the car part of a message with 'az' and 'el' float entries.

**Distance "Radar"** - Similar to the old-school signal trackers, this widget produces a radar-like screen and draws a "contact" circle at a distance of your choosing controlled by an inbound message.

## Building
gr-guiextra is available in the pybombs repository.  However to build gr-guiextra from source, simply follow the standard module build process.  Close GNURadio if you have it open; then use the following build steps:

    cd
    git clone https://github.com/ghostop14/gr-guiextra.git
    cd ~/gr-guiextra
    git checkout maint-3.8  # for version 3.8
    mkdir build
    cd build
    cmake ../
    make
    sudo make install
    sudo ldconfig

**Do not overlook the "sudo ldconfig" step!**

