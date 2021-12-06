
import cv2
import pickle
import socket
import struct

# Création du socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Il faut récupérer  l'adresse ip du serveur et la coller ici
host_ip = "192.168.0.194"
# Port aléatoire(9999 est souvent libre)
port = 9999
# Connexion au serveur
client_socket.connect((host_ip, port))
# data est initialisé comme un basestring
data = b""
# la taille du payload est initialisée à Q, un futur assignement 8 bit
payload_size = struct.calcsize("Q")

while True:
    # Réception des packets de données avec un buffer de 4K bits
    # La taille du message est récupérée dans le payload avant sa taille
    # La data est récupérée avec le reste des données

    while len(data) < payload_size:
        packet = client_socket.recv(4 * 1024)
        if not packet:
            break
        data += packet
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q", packed_msg_size)[0]

    # Réception de l'entièreté des données en 4K bits encore
    # Quand les données sont reçus, lancer un frame comprenant la caméra
    # Si on clique sur q ça quitte la caméra
    while len(data) < msg_size:
        data += client_socket.recv(4 * 1024)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    frame = pickle.loads(frame_data)
    cv2.imshow("RECEIVING VIDEO", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
client_socket.close()
