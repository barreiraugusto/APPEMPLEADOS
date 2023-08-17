import socket


class UDPSender:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_value(self, value):
        packed_data = value.encode('utf-8')
        self.sock.sendto(packed_data, (self.host, self.port))
        self.sock.settimeout(2)

        try:
            received_data, server_address = self.sock.recvfrom(1024)
            return received_data
        except socket.timeout:
            return None

    def close(self):
        self.sock.close()


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    mi_valor = 0x00003EF5

    udp_sender = UDPSender(HOST, PORT)
    received_data = udp_sender.send_value(mi_valor)
    udp_sender.close()

    print("Received:", received_data)
