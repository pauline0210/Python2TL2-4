
from data_receiver import DataReceiver
from data_sender import DataSender
import socket
import threading
import argparse
# 162.158.233.108

if __name__ == "__main__":
    """
    Lancement de l'application
    """
    parser = argparse.ArgumentParser(description="Video chat application")
    parser.add_argument('--ip', help="The ip of the other computer")
    parser.add_argument('--myIp', action='store_true',
                        help="Display my ip")
    parser.add_argument('--startThreads', action='store_true',
                        help="Start server and client thread if True")

    args = parser.parse_args()
    ip = args.ip
    my_ip = args.myIp
    launch = args.startThreads
    server = None
    client = None

    if my_ip:
        print(socket.gethostbyname(socket.gethostname()))

    if ip:
        client = DataSender(ip)
        server = DataReceiver()
    else:
        print("The inputted ip address is not valid")

    if launch:
        threading.Thread(target=server.thread).start()
        threading.Thread(target=client.thread).start()
    else:
        print("Call was not done")


