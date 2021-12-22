import socket


class DataReceiver:
    """
    Cette classe est utilisé afin de pouvoir se connecter avec un socket client et recevoir les informations transmises.
    """
    def __init__(self):
        """
        Le constructeur a 4 attributs
        :receiver_socket: un objet socket est créé avec le protocole TCP_IP
        :host_ip: l'adresse ip de la machine
        :port: le port qui sera ouvert sur host_ip
        :client_socket: initialisé à None, servira par après
        :address: initialisé à None, servira par après
        """
        self.receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host_ip = socket.gethostbyname(socket.gethostname())
        self.port = 9999
        self.client_socket, self.address = None, None

    @property
    def socket_address(self):
        """
        Permet d'avoir à l'adresse ip et au port du socket dans un tuple
        :PRE: /
        :POST: retourne un tuple de self.host_ip et self.port
        """
        return self.host_ip, self.port

    def socket_binding(self):
        """
        Lie l'adresse ip et le port avec l'objet self.receiver_socket
        :PRE: /
        :POST: self.receiver_socket est paramétré avec l'adresse ip et le port
        """
        self.receiver_socket.bind(self.socket_address)

    def socket_listening(self):
        """
        Attendant toutes connexion entrantes avec self.receiver_socket
        :PRE: /
        :POST: self.receiver_socket est en attente de connexion
        """
        self.receiver_socket.listen()

    def socket_connected(self):
        """
        Accepte la première connexion entrante sur self.receiver_socket
        :PRE: /
        :POST: retourne le socket entrant et l'adresse sous forme de tuple
        """
        return self.receiver_socket.accept()

    def stop_receiving(self):
        """
        Met self.receiver_socket en état fermé
        :PRE: /
        :POST: self.receiver_socket est fermé et un autre socket est recréé pour d'autres connexion
        """
        self.receiver_socket.close()
        self.receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def thread(self):
        """
        Cette méthode lance la procédure pour le socket récepteur. Fonctionne notamment avec un thread afin de pouvoir
        lancer plusieurs socket avec un seul process.
        :PRE: /
        :POST: self.receiver_socket est paramétré, écouté et accepte toute connexion entrante
        """
        self.socket_binding()
        self.socket_listening()
        print(f"LISTENING AT: {self.socket_address}")
        self.client_socket, self.address = self.socket_connected()
        print(f"GOT CONNECTION FROM:{self.address}")
