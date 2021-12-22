import cv2
import pickle
import socket
import struct
import imutils


class DataSender:
    """
    TODO: Documentation sur la classe Client
    C'est le ficher data_sender.py mais en classe le fonctionnement est pareil
    """

    def __init__(self, ip):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host_ip = ip
        self.port = 9999
        self.vid = cv2.VideoCapture(0)

    @property
    def socket_address(self):
        return self.host_ip, self.port

    def connect_to_receiver(self):
        self.client_socket.connect(self.socket_address)

    def send_data(self):
        if self.client_socket:
            print("SENDING VIDEO FEED")
            try:
                while self.vid.isOpened():
                    img, frame = self.vid.read()
                    frame = imutils.resize(frame, width=320)
                    a = pickle.dumps(frame)
                    message = struct.pack("Q", len(a)) + a
                    self.client_socket.sendall(message)
                    cv2.imshow("Sending...", frame)
                    key = cv2.waitKey(1)
                    if key == ord('q'):
                        self.client_socket.close()
                        break
                self.vid = None
            except:
                print("CLIENT ERROR")
                self.client_socket.close()
                self.vid = None

    def thread(self):
        self.connect_to_receiver()
        self.send_data()
