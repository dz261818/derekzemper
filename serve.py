import http.server
import os
import socketserver
import mimetypes

PORT = int(os.environ.get('PORT', 8080))
DIR = '/Users/derekzemper/Desktop/derek-zemper-portfolio'

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split('?')[0].split('#')[0]
        if path == '/' or path == '':
            path = '/index.html'
        local = os.path.join(DIR, path.lstrip('/'))
        try:
            with open(local, 'rb') as f:
                data = f.read()
            ct, _ = mimetypes.guess_type(local)
            self.send_response(200)
            self.send_header('Content-Type', ct or 'application/octet-stream')
            self.send_header('Content-Length', str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
        except PermissionError:
            self.send_response(403)
            self.end_headers()

    def log_message(self, fmt, *args):
        print(fmt % args)

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

with ReusableTCPServer(('', PORT), Handler) as httpd:
    print(f'Serving {DIR} on port {PORT}')
    httpd.serve_forever()
