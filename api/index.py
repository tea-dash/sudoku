from http.server import BaseHTTPRequestHandler
from .server import app

# Vercel serverless function handler
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # Create a Flask response for the path
        with app.test_client() as client:
            response = client.get(self.path)
            self.wfile.write(response.data)
        
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        # Create a Flask response for the path
        with app.test_client() as client:
            response = client.post(
                self.path, 
                data=post_data,
                content_type='application/json'
            )
            self.wfile.write(response.data) 