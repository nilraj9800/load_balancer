from http.server import SimpleHTTPRequestHandler, HTTPServer

import socket
socket.getaddrinfo('localhost', 8888)


host_name1 = "localhost"
serve_port1 = 8888

class BackendServer2(SimpleHTTPRequestHandler):
    
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
        self.wfile.write(bytes(f"<p> Hello {name} from backend Server2</p>", "utf-8"))
        
if __name__ == "__main__":        
    Backend_server1 = HTTPServer((host_name1, serve_port1), BackendServer2)
    print("Server started http://%s:%s" % (host_name1, serve_port1))

    try:
        Backend_server1.serve_forever()
    except KeyboardInterrupt:
        pass

    Backend_server1.server_close()
    print("Server stopped.")