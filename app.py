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

Builder.load_file("kivy_graphics.kv")


class Main(App, Widget):
    """
    Classe principale de l'application. C'est ici que l'interface se construit et que la réception des données sera
    faite.
    """

    def __init__(self, **kwargs):
        """
        Initialisation des attributs qui serviront plus tard pour la réception des données.
        :param kwargs: héritage de la classe App
        """
        super().__init__(**kwargs)
        self.receiver = DataReceiver()
        # METTRE LA BONNE IP ICI
        self.sender = DataSender('130.104.210.148')
        self.client_socket, self.address = None, None
        self.image = self.ids.img

    def build(self):
        """
        Construction de l'interface graphique kivy.
        :return:
        """
        # opencv2 stuffs
        Clock.schedule_interval(self.show_client, 1 / 64)
        return self

    def stop_app(self, *args):
        self.sender.stop_send_data()
        self.receiver.stop_receiving()
        self.image = self.ids.img

    def data_receiver(self, *args):
        self.receiver.socket_binding()
        self.receiver.socket_listening()
        print(f"LISTENING AT: {self.receiver.socket_address}")
        self.client_socket, self.address = self.receiver.socket_connected()
        print(f"GOT CONNECTION FROM:{self.address}")

    def show_client(self, *args):
        """
        Affichage du feed video après la connexion au serveur.
        :param args:
        :return:
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
            print("ERROR")
            self.client_socket.close()
            self.client_socket = None

    def translate_frame(self, frame, *args):
        """
        Cette méthode converti la frame vidéo en quelque chose de compréhensible par kivy afin de pourvoir l'afficher.
        :param frame: les données d'image reçue du client
        :param args:
        :return:
        """
        # display the current video frame in the kivy Image widget
        # create a Texture the correct size and format for the frame
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        # copy the frame data into the texture
        texture.blit_buffer(cv2.flip(frame, 0).tobytes(), colorfmt='bgr', bufferfmt='ubyte')
        # actually put the texture in the kivy Image widget
        self.image.texture = texture

    def call(self):
        threading.Thread(target=self.sender.thread).start()
