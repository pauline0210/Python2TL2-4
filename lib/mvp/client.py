
import cv2
import pickle
import socket
import struct
import imutils


class Client:
    """
    TODO: Documentation sur la classe Client
    C'est le ficher client.py mais en classe le fonctionnement est pareil
    """
    def __init__(self, ip, film=0, port=9999):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host_ip = ip
        self.port = port
        self.vid = cv2.VideoCapture(film)

    @property
    def socket_address(self):
        return self.host_ip, self.port

    def client_connection(self):
        self.client_socket.connect(self.socket_address)

    def client_video_sending(self):
        if self.client_socket:
            while self.vid.isOpened():
                try:
                    img, frame = self.vid.read()
                    frame = imutils.resize(frame, width=320)
                    a = pickle.dumps(frame)
                    message = struct.pack("Q", len(a)) + a
                    self.client_socket.sendall(message)
                    cv2.imshow(f"TO : {self.host_ip}", frame)
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord("q"):
                        self.client_socket.close()
                except Exception:
                    print("VIDEO TERMINATED")
                    break
            self.client_socket.close()
