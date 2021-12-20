
import struct
import pickle
import cv2


class ServerInstance:
    """
    TODO: Documentation de la classe ServerInstance
    """
    def __init__(self, server_socket):
        self.client_socket, self.address = server_socket
        print(f"GOT CONNECTION FROM:{self.address}")

    def server_to_client(self):
        self.client_socket.send(input("Input : ").encode())
        self.client_socket.close()

    def show_client(self):
        try:
            print(f"Client {self.address} CONNECTED")
            if self.client_socket:
                data = b""
                payload_size = struct.calcsize("Q")
                while True:
                    while len(data) < payload_size:
                        packet = self.client_socket.recv(4*1024)
                        if not packet:
                            break
                        data += packet
                    packed_msg_size = data[:payload_size]
                    data = data[payload_size:]
                    msg_size = struct.unpack("Q", packed_msg_size)[0]

                    while len(data) < msg_size:
                        data += self.client_socket.recv(4*1024)
                    frame_data = data[:msg_size]
                    data = data[msg_size:]
                    frame = pickle.loads(frame_data)
                    cv2.imshow(f"FROM {self.address}", frame)
                    key = cv2.waitKey(1) & 0xFF
                    if key == "q":
                        break
                self.client_socket.close()
        except Exception:
            print(f"CLIENT {self.address} DISCONNECTED")
            pass
