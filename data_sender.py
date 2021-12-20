
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
    def __init__(self, ip, film=0, port=9999):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host_ip = ip
        self.port = port
        self.vid = cv2.VideoCapture('town.mp4')

    @property
    def socket_address(self):
        return self.host_ip, self.port

    def connect_to_receiver(self):
        self.client_socket.connect(self.socket_address)

    def send_data(self):
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
                    print("VIDEO TERMINATED")
                    self.client_socket.close()
                    break
            print("Video ended")
            self.client_socket.close()

    def stop_send_data(self):
        self.client_socket.close()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.vid = None

    def thread(self):
        if self.vid is None:
            self.vid = cv2.VideoCapture('town.mp4')
        self.connect_to_receiver()
        self.send_data()
