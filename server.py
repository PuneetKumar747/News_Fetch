import http.server
import socketserver
import os

PORT = 10000  # Change this if needed
DIRECTORY = "."  # Serve files from the current directory

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        """Serve only JSON files"""
        if self.path.endswith(".json"):
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
        self.send_response(403)
        self.end_headers()
        self.wfile.write(b"Forbidden: Only JSON files are accessible")

os.chdir(DIRECTORY)  # Change working directory
with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"Serving JSON files on port {PORT}")
    httpd.serve_forever()
