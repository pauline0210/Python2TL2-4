import socket


class DataReceiver:
    """
    ToDo
    """
    def __init__(self, port=9999):
        self.receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host_ip = socket.gethostbyname(socket.gethostname())
        self.port = port
        self.client_socket, self.address = None, None

    @property
    def socket_address(self):
        return self.host_ip, self.port

    def socket_binding(self):
        self.receiver_socket.bind(self.socket_address)

    def socket_listening(self):
        self.receiver_socket.listen()
        print("LISTENING AT:", self.socket_address)

    def socket_connected(self):
        return self.receiver_socket.accept()

    def stop_receiving(self):
        self.receiver_socket.close()
        self.receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
