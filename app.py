import socket
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from functools import partial
import threading
import cv2
import struct
import pickle
from data_sender import DataSender
from data_receiver import DataReceiver
from kivy.properties import ObjectProperty

Builder.load_file("kivy_graphics.kv")


class Main(App, Widget):
    """
    Classe principale de l'application. C'est ici que l'interface se construit et que la réception des données sera
    faite.
    """
    inputted_ip = ObjectProperty(None)

    def __init__(self, **kwargs):
        """
        Initialisation des attributs qui serviront plus tard pour la réception des données.
        :param kwargs: héritage de la classe App
        :self.receiver: initialisé à None, sera un objet DataReceiver par après
        :self.sender: initialisé à None, sera un objet DataSender par après
        :self.selected_ip: initialisé à None, l'adresse ip choisie par l'utilisateur
        :self.client_socket: initialisé à None, le socket qui s'est connecté
        :self.address: initialisé à None, l'adresse du socket qui s'est connecté
        :self.image: l'endroit où sera affiché la webcam
        """
        super().__init__(**kwargs)
        self.receiver = None
        self.sender = None
        self.selected_ip = None
        self.client_socket, self.address = None, None
        self.image = self.ids.img

    def build(self):
        """
        Construction de l'interface graphique kivy.
        :return: l'affichage graphique selon le fichier .kv chargé au préalable
        """
        self.inputted_ip.text = socket.gethostbyname(socket.gethostname())
        # opencv2 stuffs
        Clock.schedule_interval(self.show_client, 0)
        return self

    def stop_app(self, *args):
        """
        Arrête l'envoie des données et la réception des données
        :PRE: /
        :POST: arrête les sockets self.receiver et self.sender, réinitialise le socket entrant à None
        """
        self.receiver.stop_receiving()
        self.sender.stop_send_data()
        self.client_socket, self.address = None, None

        def reset_webcam(*args):
            self.image.texture = None

        Clock.schedule_once(reset_webcam)

    def data_receiver(self, *args):
        """
        Cette méthode lance la procédure pour le socket récepteur
        :PRE: /
        :POST: self.receiver_socket est paramétré, écoute et accepte toute connexion entrante
        """
        self.receiver.socket_binding()
        self.receiver.socket_listening()
        print(f"LISTENING AT: {self.receiver.socket_address}")
        self.client_socket, self.address = self.receiver.socket_connected()
        print(f"GOT CONNECTION FROM:{self.address}")

    def show_client(self, *args):
        """
        Affichage du feed video après la connexion au serveur.
        :param args: permet l'appel par kivy
        :PRE: /
        :POST: Affiche la webcam du socket client dans kivy
        """
        try:
            if self.client_socket:
                data = b""
                payload_size = struct.calcsize("Q")
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
                Clock.schedule_once(partial(self.translate_frame, frame))
            else:
                pass
        except:
            print("ERROR APP")
            self.client_socket.close()
            self.client_socket = None

    def translate_frame(self, frame, *args):
        """
        Cette méthode converti la frame vidéo en quelque chose de compréhensible par kivy afin de pourvoir l'afficher.
        :param frame: les données d'image reçue du client
        """
        # display the current video frame in the kivy Image widget
        # create a Texture the correct size and format for the frame
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        # copy the frame data into the texture
        texture.blit_buffer(cv2.flip(frame, 0).tobytes(), colorfmt='bgr', bufferfmt='ubyte')
        # actually put the texture in the kivy Image widget
        self.image.texture = texture

    def set_ip(self):
        """
        Méthode appelé pour enregistrer l'ip introduite dans kivy
        :PRE: /
        :POST: change self.selected_ip par l'ip soumise
        """
        self.selected_ip = self.inputted_ip.text
        print(self.selected_ip)

    def call(self):
        """
        Lance la réception et l'appel vidéo
        :PRE: /
        :POST: lance deux threads: un qui attend une connexion et l'autre qui lance un appel
        """
        self.sender = DataSender(self.selected_ip)
        self.receiver = DataReceiver()
        threading.Thread(target=self.sender.thread).start()
        threading.Thread(target=self.data_receiver).start()
        # Clock.schedule_interval(self.load_vid, 1/64)
