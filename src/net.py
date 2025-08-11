import socket
import json

class Net:
    def __init__(self, sock: socket.socket = None):
        self.sock = sock or socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host, port):
        """Connect as client."""
        self.sock.connect((host, port))

    def bind_and_listen(self, host, port):
        """Bind and listen as server."""
        self.sock.bind((host, port))
        self.sock.listen()

    def accept(self):
        """Accept a connection (server-side). Returns a new Net instance."""
        conn, addr = self.sock.accept()
        return Net(conn), addr

    def send_json(self, obj):
        """Send a Python object as JSON."""
        data = json.dumps(obj).encode('utf-8')
        self.sock.sendall(data)

    def recv_json(self, bufsize=4096):
        """Receive JSON and decode to Python object."""
        data = self.sock.recv(bufsize)
        if not data:
            return None
        return json.loads(data.decode('utf-8'))

    def close(self):
        self.sock.close()
