from threading import Lock
from itertools import cycle


class loadBalancer:
    def __init__(self, server_pool):
        self.server_pool = server_pool
        self.lock = Lock()
        self.cycle = cycle(self.server_pool)

    def get_next_server(self):
        with self.lock:
            try:    
                return next(self.cycle)
            except StopIteration:
                return None
    
    def update_servers(self, new_server_list):
        with self.lock:
            self.server_pool = new_server_list
            self.cycle = cycle(self.server_pool)
    