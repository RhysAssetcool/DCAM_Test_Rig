import socket
import json

class Net:
    def __init__(self, sock: socket.socket = None):
        self.sock = sock or socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._recv_buffer = b''  # Buffer for partial/incomplete messages

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
        """Send a Python object as JSON, delimited by newline."""
        data = json.dumps(obj).encode('utf-8') + b'\n'
        self.sock.sendall(data)

    def recv_json(self, bufsize=4096):
        """Receive a newline-delimited JSON object and decode to Python object."""
        while b'\n' not in self._recv_buffer:
            chunk = self.sock.recv(bufsize)
            if not chunk:
                return None
            self._recv_buffer += chunk
        line, self._recv_buffer = self._recv_buffer.split(b'\n', 1)
        return json.loads(line.decode('utf-8'))

    def close(self):
        self.sock.close()