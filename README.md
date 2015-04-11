Ps Controller
======

What is it?
------
The Ps Controller is a local python web server to control the PS201 adjustable power supply. See http://github.com/mannsi/PS201. 

Release date
------
Currently there is no decided release date

Installation
------
The easiest way to install is to run `sudo python3 setup.py install`. Note that this will try to download and install python dependencies so a network connection is probably needed (see the setup.py file for dependencies).

Running
------
Precondition: Your user needs to belong to the user group 'dialout' to be able to access the usb port of the PS201.

1. Connect the PS201 via usb to your computer
2. From terminal run `ps_controller`. This runs a local web server that exposes the PS201. By default the server uses port 8080. To use port XXX run `ps_controller --port XXX` instead.
3. From your favorite browser, go the the path 'localhost:8080'. This should open a web UI for the PS201

API
------
See the http://github.com/mannsi/PsController/wiki for details on the local web server API.

License
------
All code is fully open source licensed under GNU GPL v3. Feel free to copy and modify our software, any feedback is welcome.
