from BaseHTTPServer import BaseHTTPRequestHandler
from hashlib import md5
from json import dumps
from re import match
from urllib import url2pathname
from urlparse import urlparse

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
            'info':  cls.info,
            'play':  cls.play,
            'pause': cls.pause,
            'stop':  cls.stop,
            'prev':  cls.prev,
            'next':  cls.next,
        }
        cls._static_files = {
            'css/style.css':    'text/css',
            'html/player.html': 'text/html',
            'img/icons.png':    'image/png',
            'img/sprites.png':  'image/png',
            'js/jquery.min.js': 'application/javascript',
            'js/marc.js':       'application/javascript',
        }
        cls._art = {}
    
    def _send_reply(self, content, status_code=200, mime_type='text/html'):
        '''Convenience method for sending a response to the client.'''
        self.send_response(status_code)
        self.send_header('Content-length', str(len(content)))
        self.send_header('Content-type', mime_type)
        self.end_headers()
        self.wfile.write(content)
    
    def _send_redirect(self, url):
        '''Convenience method for sending a redirect to the client.'''
        self.send_response(301)
        self.send_header('Location', url)
        self.end_headers()
    
    def do_GET(self):
        '''Processes an HTTP GET request.'''
        m = match(r'^/art/([0-9a-f]{32})$', self.path)
        if m and m.group(1) in self._art:
            self._send_reply(open(self._art[m.group(1)], 'r').read(), mime_type='image/png')
        elif self.path == '/':
            self._send_redirect('/html/player.html')
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
    
    def info(self, player):
        '''Returns information about the current song being played.'''
        i = player.info()
        # Create an MD5 hash of the current album art.
        h = md5(i['arturl']).hexdigest()
        self._art[h] = url2pathname(urlparse(str(i['arturl'])).path)
        return {
            'album':  str(i['album']),
            'artist': str(i['artist']),
            'art':    h,
            'title':  str(i['title']),
        }
    
    # These methods are simple and need no explanation.
    def play(self, player):  player.play()
    def pause(self, player): player.pause()
    def stop(self, player):  player.stop()
    def prev(self, player):  player.prev()
    def next(self, player):  player.next()

# Set up all method mappings and initialize the players.
MediaHandler.initialize()