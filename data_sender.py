import cv2
import pickle
import socket
import struct
import imutils


class DataSender:
    """
    Cette classe est utilisé afin de pouvoir se connecter avec un socket prêt à recevoir le feed de la webcam.
    """
    def __init__(self, ip=None):
        """
        :param ip: l'adresse ip de la machine sur laquelle on veut se connecter.
        Doit être de type str et valide, exemple: '123.123.123.123'

        Le constructeur a 4 attributs
        :receiver_socket: un objet socket est créé avec le protocole TCP_IP
        :host_ip: l'adresse ip de la machine à laquelle on veut se connecter, par défaut None
        :port: le port qui sera ouvert sur host_ip
        :vid: le feed vidéo de la webcam
        """
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host_ip = ip
        self.port = 9999
        self.vid = cv2.VideoCapture(0)

    @property
    def socket_address(self):
        """
        Permet d'avoir à self.host_ip et à self.port dans un tuple
        :PRE: /
        :POST: retourne un tuple de self.host_ip et self.port
        """
        return self.host_ip, self.port

    def connect_to_receiver(self):
        """
        Cherche à connecter le socket de l'objet avec un socket récepteur à l'adresse et au port passé en paramètre
        :PRE: /
        :POST: Se connecte au socket
        :raises TimeoutError: si il ne trouve pas le socket correspondant
        :raises ConnectionRefusedError: si le socket a refusé la connexion
        """
        self.client_socket.connect(self.socket_address)

    def send_data(self):
        """
        Envoie le feed vidéo de la webcam au socket connecté
        :PRE: /
        :POST: compresse le feed vidéo de la webcam et l'envoie au socket récepteur
        """
        if self.client_socket:
            print("Send video...")
            while self.vid.isOpened():
                try:
                    img, frame = self.vid.read()
                    frame = imutils.resize(frame, width=320)
                    a = pickle.dumps(frame)
                    message = struct.pack("Q", len(a)) + a
                    self.client_socket.sendall(message)
                except Exception:
                    self.stop_send_data()
                    break

    def stop_send_data(self):
        """
        Met self.receiver_socket en état fermé et éteint la webcam
        :PRE: /
        :POST: self.vid devient None et self.receiver_socket est fermé et un autre socket est recréé pour
        d'autres connexion
        """
        self.vid = None
        self.client_socket.close()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def thread(self):
        """
        Cette méthode lance la procédure pour le socket client
        :PRE: /
        :POST: self.client_socket se connecte et envoie le feed vidéo de la webcam
        """
        self.connect_to_receiver()
        self.send_data()
