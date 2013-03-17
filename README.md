##  Multimedia Application Remote Control (MARC)

These Python scripts provide a web-based interface for controlling common Linux media players. Using the web interface, you can control the player (play, pause, etc.) and browse your media library.

### Supported Music Players

 - Amarok

### Requirements

You will need the following installed on your system in order to run PAD:

 - one of the supported media players
 - Python 2.7.x (tested on Python 2.7.3)
 - [dbus-python](http://dbus.freedesktop.org/releases/dbus-python/) (often found in package managers under the name `python-dbus`)

### Starting MARC

Simply open a terminal and run the following command:

    python marc.py

Then point your browser to [http://localhost:8000](http://localhost:8000) and enjoy!

### JSON API

MARC provides a JSON API that is used by the web interface to control the music players. The functions exposed are as follows:

 - <code>/players</code> - a list of all media players available
 - <code>/&lt;player&gt;/&lt;action&gt;</code> - sends one of the following actions to the specified player:
   - <code>play</code> - begins playing the current song in the playlist
   - <code>pause</code> - ceases playback
   - <code>stop</code> - ceases playback and resets the play position in the current song
   - <code>previous</code> - begins playing the previous song in the playlist
   - <code>next</code> - begins playing the next song in the playlist

The JSON data returned always consists of information relating to the currently playing song (if any). For example:

    {
        'song': {
            'title': 'Song Title',
            'artist': 'Song Artist',
            'album': 'Song Album',
            'art': '/img/a782bb990f9001244de88c9a32b9c14.jpg',
            'position': 20.4,
            'length': 213.6
        }
    }

