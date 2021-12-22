import socket
import unittest
import threading
from data_sender import DataSender
from data_receiver import DataReceiver


class SenderReceiverTest(unittest.TestCase):
    def test_connexion(self):
        sender = DataSender(socket.gethostbyname(socket.gethostname()))
        receiver = DataReceiver()

        def sender_thread():
            sender.connect_to_receiver()
        threading.Thread(target=sender_thread).start()
        receiver.socket_binding()
        receiver.socket_listening()
        client_socket, address = receiver.socket_connected()
        self.assertEqual(address[0], sender.host_ip)
        sender.stop_send_data()
        receiver.stop_receiving()

    def test_timeout(self):
        sender = DataSender("192.50.23.146")
        receiver = DataReceiver()

        def receiver_thread():
            receiver.socket_binding()
            receiver.socket_listening()
        threading.Thread(target=receiver_thread).start()
        self.assertRaises(sender.connect_to_receiver(), TimeoutError)
        sender.stop_send_data()
        receiver.stop_receiving()


if __name__ == '__main__':
    unittest.main()
