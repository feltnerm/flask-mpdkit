flask-mpdkit
============

A Flask extension that simplifies the use of MPD. If you import the MPDKit class and use that as your global mpd connection handler, then MPDKit will automatically deal with bringing the connection up or down, give you a nice syntax/sematics for communicating with the MPD socket, error pretty gracefully (if it even does), and work with previous Flask versions.

This is my first Flask extension.
The code was based on the [Flask-Mongokit](https://github.com/jarus/flask-mongokit) project, but (obviously) adapted to use [python-mpd2](https://github.com/Mic92/python-mpd2).
