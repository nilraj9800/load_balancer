from http.server import SimpleHTTPRequestHandler, HTTPServer

host_name = "localhost"
serve_port = 8000

class BackendServer(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_POST(self):
        self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
        
if __name__ == "__main__":        
    Backend_server = HTTPServer((host_name, serve_port), BackendServer)
    print("Server started http://%s:%s" % (host_name, serve_port))

    try:
        Backend_server.serve_forever()
    except KeyboardInterrupt:
        pass

    Backend_server.server_close()
    print("Server stopped.")