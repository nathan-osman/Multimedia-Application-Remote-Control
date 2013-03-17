import dbus

class MediaPlayer:
    '''Represents a D-Bus connection to a running instance of a supported media player.'''
    
    # Exception class thrown when a D-Bus error occurs.
    class Error(Exception):
        '''Represents a D-Bus error encountered while executing a command.'''
        
        def __init__(self, dbus_exception, player):
            '''Initializes the error with the specified player and error message.'''
            Exception.__init__(self, dbus_exception.get_dbus_message())
            self._player = player
        
        def get_player(self):
            '''Returns the name of the player that generated the error.'''
            return self._player['name']
    
    # Maintain a connection to the session bus throughout the lifetime of the module.
    _bus = dbus.SessionBus()
    
    # Information about each of the supported media players.
    _players = {
        'amarok': {
            'name': 'Amarok',
            'bus':  'org.kde.amarok',
        },
        'rhythmbox': {
            'name': 'Rhythmbox',
            'bus':  'org.gnome.Rhythmbox',
        },
    }
    
    @classmethod
    def players(self):
        '''Returns a list of all media players available.'''
        return self._players.keys()
    
    def __init__(self, player):
        '''Creates a new D-Bus connection to a running instance of the specified media player.'''
        try:
            self._player = self._players[player]
            self._proxy = self._bus.get_object(self._player['bus'], '/Player')
            self._iface = dbus.Interface(self._proxy, 'org.freedesktop.MediaPlayer')
        except KeyError:
            raise Exception('media player "%s" is not supported' % player)
        except dbus.exceptions.DBusException, e:
            raise self.Error(e, self._player)
    
    def _action(self, action, *args):
        '''Performs the requested action on the player.'''
        try:
            self._iface.__getattr__(action)(*args)
        except dbus.exceptions.DBusException, e:
            raise self.Error(e, self._player)
    
    def _track_changed(self, sender):
        print 'Track CHANGED!'
    
    def play(self):
        '''Begins playing the current song.'''
        self._action('Play')
    
    def pause(self):
        '''Pauses playback of the current song.'''
        self._action('Pause')
    
    def stop(self):
        '''Immediately stops playback.'''
        self._action('Stop')
    
    def prev(self):
        '''Plays the preceding song in the current playlist.'''
        self._action('Prev')
    
    def next(self):
        '''Plays the next song in the current playlist.'''
        self._action('Next')
