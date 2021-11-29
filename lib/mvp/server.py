
import cv2
import imutils
import pickle
import socket
import struct

# Création du socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Récupération de l'adresse ip
host_ip = socket.gethostbyname((socket.gethostname()))
print('HOST IP:', host_ip)
# Port aléatoire(9999 est souvent libre)
port = 9999
# L'adresse attribuée au socket reprend le port et l'adresse IP
socket_address = (host_ip, port)

# Liaison du socket au point de communication correspondant
server_socket.bind(socket_address)

# Le socket vérifie si un client se connecte sur la même adresse que lui
server_socket.listen(5)
print("LISTENING AT:", socket_address)


while True:
    # Si un client est trouvé, on l'accepte et on lance une capture vidéo
    client_socket, addr = server_socket.accept()
    print('GOT CONNECTION FROM:', addr)
    if client_socket:
        vid = cv2.VideoCapture(0)
        # Tant que la vidéo est en cours, on crée un frame contenant notre caméra
        # Si on clique sur q ça quitte la caméra
        while vid.isOpened():
            img, frame = vid.read()
            frame = imutils.resize(frame, width=320)
            a = pickle.dumps(frame)
            message = struct.pack("Q", len(a)) + a
            client_socket.sendall(message)

            cv2.imshow('TRANSMITTING VIDEO', frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                client_socket.close()
