import socket

from lib.mvp.client import Client
from lib.mvp.server import Server
import threading


def server(ip):
    serv1 = Server(ip)
    serv1.socket_binding()
    serv1.server_listening()
    serv1.server_client_connected()


def client(ip):
    clie1 = Client(ip)
    clie1.client_connection()
    clie1.client_video_sending()


if __name__ == "__main__":
    """
    C'est ici qu'on lance "l'appel". ça lance 2 threads de chaque classe. Faut juste correctement mettre les ip.
    """
    server_thread = threading.Thread(target=server, args=("10.99.1.198",))
    server_thread.start()

    client_thread = threading.Thread(target=client, args=("10.99.1.198",))
    client_thread.start()
