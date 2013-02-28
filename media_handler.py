from BaseHTTPServer import BaseHTTPRequestHandler
from json import dumps
from re import match

from media_player import MediaPlayer

class MediaHandler(BaseHTTPRequestHandler):
    '''Provides an HTTP interface for controlling a media player.'''
    
    # Initializes connections to all supported players. Also sets up the list of
    # accepted API methods and their appropriate methods in this class.
    @classmethod
    def initialize(cls):
        cls._players = {
            'amarok': MediaPlayer(MediaPlayer.AMAROK),
        }
        cls._methods = {
            'play':  cls.play,
            'pause': cls.pause,
        }
    
    def _send_reply(self, status_code, content, mime_type='text/html'):
        '''Convenience method for sending a response to the client.'''
        self.send_response(status_code)
        self.send_header('Content-length', str(len(content)))
        self.send_header('Content-type', mime_type)
        self.end_headers()
        self.wfile.write(content)
    
    def do_GET(self):
        '''Processes an HTTP GET request.'''
        m = match(r'^/api/(\w+)/(\w+)$', self.path)
        if m and m.group(1) in self._players and m.group(2) in self._methods:
            getattr(self, m.group(2))(self._players[m.group(1)])
        elif self.path == '/':
            self._send_reply(200, '<a href="/api/amarok/play">Play</a> | <a href="/api/amarok/pause">Pause</a>')
        else:
            self._send_reply(404, 'The path "%s" does not exist on this server.' % self.path)
    
    # These methods are simple and need no explanation.
    def play(self, player):  player.play()
    def pause(self, player): player.pause()

# Set up all method mappings and initialize the players.
MediaHandler.initialize()

#==================================================================
# This will eventually get removed, but it's handy for development.
if __name__ == "__main__":
    from BaseHTTPServer import HTTPServer
    s = HTTPServer(('', 8000,), MediaHandler)
    s.serve_forever()