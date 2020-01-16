import socket
import threading

class MessageSenderAndReceiver:

    def __init__(self):
        # Хранит последнее полученное сообщение
        self.received = None
        self.found_a_pair = False

        # Создание сокета udp
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Инициализация ip и порта
        self.ip = socket.gethostbyname(socket.gethostname())
        self.port = 7777
        self.address = (self.ip, self.port)
        self.sock.bind(self.address)

        # Адрес сервера, на который будут отправляться сообщения
        self.server_address_to_send_messages = ('192.168.0.115', 8888)

        # Поток для чтения данных
        thread = threading.Thread(target=self.receive_messages)
        thread.start()

    def receive_messages(self):
        while True:
            received_message = self.sock.recv(1024).decode('utf-8')
            if 'connected' in received_message:
                self.found_a_pair = True

            if 'data:' in received_message:
                self.received = received_message.split(':')[1]

    def send_message(self, message):
        info = bytes(message, encoding='utf-8')
        self.sock.sendto(info, self.server_address_to_send_messages)