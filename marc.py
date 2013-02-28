from BaseHTTPServer import HTTPServer

from media_handler import MediaHandler

# Create an instance of the server and launch it.
s = HTTPServer(('', 8000,), MediaHandler)
s.serve_forever()