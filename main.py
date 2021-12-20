
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
    server_thread = threading.Thread(target=server, args=('192.168.0.194',)).start()
    threading.Thread(target=client, args=('192.168.0.194',)).start()

    # helloKivy = HelloKivy()
    # server_thread = helloKivy.run()
    # server_thread.start()
