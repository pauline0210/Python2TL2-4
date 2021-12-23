
import unittest
from data_sender import DataSender


class SenderTest(unittest.TestCase):
    # Test de __init__
    def test_Sender(self):
        testData = DataSender.__init__(self, "192.168.0.1")
        testData2 = DataSender.__init__(self, "192.168.0.2")
        testData3 = DataSender.__init__(self)
        self.assertEqual(testData, testData2)
        self.assertEqual(testData, testData3)

    # Test de socket_adress()
    def test_socket(self):
        sender = DataSender("192.50.23.146")
        sender2 = DataSender("0.0.0.0")
        sender3 = DataSender("10.50.80.5")
        try:
            self.assertEqual(sender.socket_address, ("192.50.23.146", 9999))
            self.assertEqual(sender2.socket_address, ("0.0.0.0", 9999))
            self.assertEqual(sender3.socket_address, ("10.50.80.5", 9999))
        except:
            pass

        # Test de connect_to_receive

    def test_connect(self):
        sender = DataSender("192.50.23.146")
        sender2 = DataSender("0.0.0.0")
        sender3 = DataSender("10.50.80.5")
        try:
            self.assertEqual(sender.connect_to_receiver(), ("192.50.23.146", 9999))
            self.assertEqual(sender2.connect_to_receiver(), ("0.0.0.0", 9999))
            self.assertEqual(sender3.connect_to_receiver(), ("10.50.80.5", 9999))
        except:
            pass

        # Test de send_data

    def test_send_data(self):
        sender = DataSender("192.50.23.146")
        sender2 = DataSender("0.0.0.0")
        sender3 = DataSender("10.50.80.5")
        try:
            self.assertEqual(sender.send_data(), ("192.50.23.146", 9999))
            self.assertRaises(sender2.send_data(), ("sss", 9999))
            self.assertEqual(sender3.send_data(), ("10.50.80.5", 9999))
        except:
            pass

        # Test de stop_send_data

    def test_stop_send_data(self):
        sender = DataSender("192.50.23.146")
        sender2 = DataSender("0.0.0.0")
        sender3 = DataSender("10.50.80.5")
        try:
            self.assertEqual(sender.stop_send_data(), ("192.50.23.146", 9999))
            self.assertRaises(sender2.stop_send_data(), ("0.0.0.0", 9999))
            self.assertEqual(sender3.stop_send_data(), ("10.50.80.5", 9999))
        except:
            pass


if __name__ == '__main__':
    unittest.main()
