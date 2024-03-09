Overview
--------

This project aims to create a GUI for controlling the RCV3 reflow controller from Beta-Layouts.
Currently we support:
- Starting and stopping the reflow process
- Viewing the reflow process and time-temperature graph


Dependencies
------------

- PyQT5
- PySerial
- matplotlib


Running it
----------

Simply execute `python3 reflow.py` to open the GUI.
The program expects the reflow controller to be available through the serial port `/dev/ttyUSB0`.
This can currently only be changed by editing the source code.
