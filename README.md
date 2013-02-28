##  Multimedia Application Remote Control (MARC)

These Python scripts provide a web-based interface for controlling common Linux media players. Using the web interface, you can control the player (play, pause, etc.) and browse your media library.

### Supported Music Players

 - Amarok

### Requirements

You will need the following installed on your system in order to run PAD:

 - one of the supported media players
 - Python 2.x (tested on Python 2.7.3)
 - [dbus-python](http://dbus.freedesktop.org/releases/dbus-python/) (often found in package managers under the name `python-dbus`)

### Starting MARC

Simply open a terminal and run the following command:

    python marc.py

Then point your browser to [http://localhost:8000](http://localhost:8000) and enjoy!