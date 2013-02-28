import dbus

class Amarok:
    '''Represents a D-Bus connection to a running instance of Amarok.'''
    
    def __init__(self):
        '''Creates a new D-Bus connection to a running instance of Amarok.'''
        self._bus = dbus.SessionBus()
        self._proxy = self._bus.get_object('org.kde.amarok', '/Player')
        self._iface = dbus.Interface(self._proxy, 'org.freedesktop.MediaPlayer')
    
    def __getattr__(self, name):
        '''Returns metadata about the currently playing song.'''
        return self._iface.GetMetadata()[name]
    
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