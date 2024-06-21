import time
import requests
import http.client
from threading import Thread
from balancer import loadBalancer
from socketserver import ThreadingMixIn
from http.server import SimpleHTTPRequestHandler, HTTPServer

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

class MyServer(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("host",'haas.website.com' )
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>load Balancer</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % hostName, "utf-8"))
        self.wfile.write(bytes("<form action='/path' method='post'>", "utf-8"))
        self.wfile.write(bytes("<label for='name'>Name:</label>", "utf-8"))
        self.wfile.write(bytes("<input type='text' id='name' name='name'><br><br>", "utf-8"))
        self.wfile.write(bytes("<input type='submit' value='Submit'>", "utf-8"))
        self.wfile.write(bytes("</form>", "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))
        
    def do_POST(self):
        retry_limit = 3 
        attempts = 0
        while attempts < retry_limit:
            try:
                content_length = int(self.headers["Content-Length"])
                post_data = self.rfile.read(content_length)
                server_detail = balancer.get_next_server()
                host_name, port_number = server_detail
                
                if server_detail is None:
                    self.send_error(503, "No available servers")
                                    
                if not schedule.server_status(host_name, port_number):
                    attempts += 1
                    continue
                
                connection = http.client.HTTPConnection(host_name, port=port_number)
                connection.request("POST", "/", body=post_data, headers=dict(self.headers))
                response = connection.getresponse()
                
                if response.status == 500:
                    attempts += 1
                    continue
                                
                self.send_response(response.status)
                self.send_header("Content-type", 
                             response.getheader("Content-Type","text/html"))
                self.end_headers()
                self.wfile.write(response.read())        
                connection.close()
                break
            
            except Exception as e:
                self.send_error(500, "Internal server Error {}".format(e))
                
        if attempts == retry_limit:
            self.send_error(500, "Internal server Error {}".format(e))
            
            
class schedule:
    def server_status(name, port):
        try:
            x = requests.get(f'http://{name}:{port}', timeout=5)
            health_code = x.status_code
            return health_code == 200   
        except:
            return False
        
    def schedule_health_check(balancer, interval=30):
        while True:
            new_server_list = [(host, port) for host, port in balancer.server_pool if schedule.server_status(host, port)]
            balancer.update_servers(new_server_list)
            time.sleep(interval)
            

if __name__ == "__main__":
    hostName = "localhost"
    serverPort = 8080
    server_list = [("localhost", 8000), ("localhost", 8888)]
    balancer = loadBalancer(server_list)
    health_check_thread = Thread(target=schedule.schedule_health_check,
                                 args=(balancer,))
    health_check_thread.start()
    webServer = ThreadedHTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))
    # Prevent issues with socket reuse
    webServer.allow_reuse_address = True

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")