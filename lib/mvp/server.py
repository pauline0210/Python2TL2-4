
import cv2
import imutils
import pickle
import socket
import struct
import threading
from .server_instance import ServerInstance


class Server:
    """
    TODO: La doc de la classe Server
    C'est le ficher serveur.py mais en classe le fonctionnement est pareil
    La différence c'est que j'ai créé un autre fichier server_instance.py qui prend en charge dès qu'un client
    se connecte. Mais le fonctionnement est tout pareil que avant c'est juste plus propre.
    """
    def __init__(self, ip, port=9999):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host_ip = ip
        self.port = port

    @property
    def socket_address(self):
        return self.host_ip, self.port

    def socket_binding(self):
        self.server_socket.bind(self.socket_address)

    def server_listening(self):
        self.server_socket.listen()
        print("LISTENING AT:", self.socket_address)

    def server_client_connected(self):
        client = ServerInstance(self.server_socket.accept())
        client.show_client()
        print("TOTAL CLIENTS ", threading.active_count() - 1)
