import socket
import struct
from functools import partial
import cv2
import pickle


class DataReceiver:
    """
    ToDo
    """
    def __init__(self):
        self.receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host_ip = socket.gethostbyname(socket.gethostname())
        self.port = 9999
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

    def thread(self):
        self.socket_binding()
        self.socket_listening()
        print(f"LISTENING AT: {self.socket_address}")
        self.client_socket, self.address = self.socket_connected()
        print(f"GOT CONNECTION FROM:{self.address}")
        self.show_client()

    def show_client(self):
        """
        Affichage du feed video après la connexion au serveur.
        :param args:
        :return:
        """
        if self.client_socket:
            try:
                while True:
                    data = b''
                    payload_size = struct.calcsize('Q')
                    while len(data) < payload_size:
                        packet = self.client_socket.recv(4 * 1024)
                        if not packet:
                            break
                        data += packet
                    packed_msg_size = data[:payload_size]
                    data = data[payload_size:]
                    msg_size = struct.unpack("Q", packed_msg_size)[0]

                    while len(data) < msg_size:
                        data += self.client_socket.recv(4 * 1024)
                    frame_data = data[:msg_size]
                    data = data[msg_size:]
                    frame = pickle.loads(frame_data)
                    cv2.imshow("Receiving...", frame)
                    key = cv2.waitKey(1)
                    if key == ord('q'):
                        self.client_socket.send(bytes(1))
                        self.client_socket.close()
                        break
            except:
                print("SERVER ERROR")
                self.client_socket.close()
