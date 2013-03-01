import dbus

class MediaPlayer:
    '''Represents a D-Bus connection to a running instance of a supported media player.'''
    
    # Definitions for common media players.
    AMAROK = 'org.kde.amarok'
    
    def __init__(self, bus_name):
        '''Creates a new D-Bus connection to a running instance of the specified media player.'''
        self._bus = dbus.SessionBus()
        self._proxy = self._bus.get_object(bus_name, '/Player')
        self._iface = dbus.Interface(self._proxy, 'org.freedesktop.MediaPlayer')
    
    def info(self):
        '''Returns information about the currently playing song.'''
        return self._iface.GetMetadata()
    
    def play(self):
        '''Begins playing the current song.'''
        self._iface.Play()
    
    def pause(self):
        '''Pauses playback of the current song.'''
        self._iface.Pause()
    
    def stop(self):
        '''Immediately stops playback.'''
        self._iface.Stop()
    
    def prev(self):
        '''Plays the preceding song in the current playlist.'''
        self._iface.Prev()
    
    def next(self):
        '''Plays the next song in the current playlist.'''
        self._iface.Next()