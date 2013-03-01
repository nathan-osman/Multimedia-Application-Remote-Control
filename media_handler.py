from BaseHTTPServer import BaseHTTPRequestHandler
from json import dumps
from re import match

from media_player import MediaPlayer

class MediaHandler(BaseHTTPRequestHandler):
    '''Provides an HTTP interface for controlling a media player.'''
    
    @classmethod
    def initialize(cls):
        '''Initializes the players, list of valid API methods, static files, and HTML template.'''
        cls._players = {
            'amarok': MediaPlayer(MediaPlayer.AMAROK),
        }
        cls._methods = {
            'play':  cls.play,
            'pause': cls.pause,
            'stop':  cls.stop,
            'prev':  cls.prev,
            'next':  cls.next,
        }
        cls._static_files = {
            'css/style.css':    'text/css',
            'img/sprites.png':  'image/png',
            'js/jquery.min.js': 'application/javascript',
            'js/marc.js':       'application/javascript',
        }
        cls._template = open('html/template.html', 'r').read()
    
    def _send_reply(self, content, status_code=200, mime_type='text/html'):
        '''Convenience method for sending a response to the client.'''
        self.send_response(status_code)
        self.send_header('Content-length', str(len(content)))
        self.send_header('Content-type', mime_type)
        self.end_headers()
        self.wfile.write(content)
    
    def do_GET(self):
        '''Processes an HTTP GET request.'''
        if self.path == '/':
            self._send_reply(self._template)
        elif self.path[1:] in self._static_files:
            self._send_reply(open(self.path[1:], 'r').read(),
                             mime_type=self._static_files[self.path[1:]])
        else:
            self._send_reply('The page "%s" does not exist on this server.' % self.path,
                             status_code=404, mime_type='text/plain')
    
    def do_POST(self):
        '''Processes an HTTP POST request.'''
        m = match(r'^/api/(\w+)/(\w+)$', self.path)
        if m and m.group(1) in self._players and m.group(2) in self._methods:
            response = getattr(self, m.group(2))(self._players[m.group(1)])
        else:
            response = {'error': 'the API method "%s" does not exist' % self.path,}
        self._send_reply(dumps(response), mime_type='application/json')
    
    # These methods are simple and need no explanation.
    def play(self, player):  player.play()
    def pause(self, player): player.pause()
    def stop(self, player):  player.stop()
    def prev(self, player):  player.prev()
    def next(self, player):  player.next()

# Set up all method mappings and initialize the players.
MediaHandler.initialize()