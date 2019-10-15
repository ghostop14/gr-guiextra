# gr-guiextra
Modern and enhanced GUI widgets for GNU Radio 3.8+

## Overview

This OOT module set provides modernized and new GUI control capabilities for GNU Radio 3.8+.  The following blocks are currently implemented in this set:

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

**Graphics Item** - Drop a graphic anywhere in your GNU Radio app screen.  You can also control the file based on input messages to change the graphic on the fly.  This can be tied to the toggle switch, button, etc. to control the image displayed based on other factors for a more dynamic display.

**App Background** - While stylesheets can be used to change an app, that can be cumbersome if all you want is to change the background color or display a background graphic.  This drop-in control lets you do either or both.

**Distance "Radar"** - Similar to the old-school signal trackers, this widget produces a radar-like screen and draws a "contact" circle at a distance of your choosing controlled by an inbound message.

## Building
gr-lfast is available in the pybombs repository.  However to build gr-lfast from source, simply follow the standard module build process.  Git clone it to a directory, close GNURadio if you have it open, then use the following build steps:

cd <clone directory>

mkdir build

cd build

cmake ..

make

[sudo] make install

sudo ldconfig

If each step was successful (do not overlook the "sudo ldconfig" step).





