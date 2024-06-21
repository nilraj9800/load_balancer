from http.server import SimpleHTTPRequestHandler, HTTPServer


import socket
socket.getaddrinfo('localhost', 8080)


host_name = "localhost"
serve_port = 8000

class BackendServer(SimpleHTTPRequestHandler):
    
    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        content_length = int(self.headers['Content-Length'])
        
        post_data = self.rfile.read(content_length)
        post_data = post_data.decode('utf-8')
        name = post_data.split("=")[1]
        
        self.wfile.write(bytes("<html><head><title>Backend Server</title></head>", "utf-8"))
        self.wfile.write(bytes("<p> Resonse 200 </p>", "utf-8"))
        self.wfile.write(bytes(f"<p> Hello {name} from backend Server1</p>", "utf-8"))
        
if __name__ == "__main__":        
    Backend_server = HTTPServer((host_name, serve_port), BackendServer)
    print("Server started http://%s:%s" % (host_name, serve_port))

    try:
        Backend_server.serve_forever()
    except KeyboardInterrupt:
        pass

    Backend_server.server_close()
    print("Server stopped.")