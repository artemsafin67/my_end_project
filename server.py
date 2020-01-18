import socket


def make_database(file):
    """Делает базу данных клиетов по чтению из файла"""

    clients = {}

    for string in file:  # Перебираем строки в файле
        name, client_address = string.strip('\n').split(':')

        if '(' in name:  # Если строка имеет вид: address:name
            name, client_address = client_address, name

        # Обработка строки
        client_address_string = client_address.strip('(').strip(')')
        client_ip_string, client_port_string = client_address_string.split(',')
        client_ip = client_ip_string.strip("'")
        client_port = int(client_port_string)

        client_address = (client_ip, client_port)  # Итоговый кортёж

        # Добавляем клиента
        clients[name] = client_address
        clients[client_address] = name

    return clients.copy()


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Создание сокета udp

# Инициализация ip и порта сервера
ip = socket.gethostbyname(socket.gethostname())
port = 8888
address = (ip, port)

# Связываем сокет и адрес
sock.bind(address)

# Создаём базы данных для хранения пользователей и их адресов
file_with_clients = open('clients.txt')
clients = make_database(file_with_clients)
file_with_clients.close()

pairs = {}  # Словарь для пар игроков

running = True
while running:
    # Читаем поступающие сообщения
    try:
        # Получение данных
        data, sender_address = sock.recvfrom(2048)
        data = data.decode('utf-8')

        # Проверка на наличие клиента в базе данных
        if 'registration:' in data:
            sender_name = data.split(':')[1]  # data имеет вид: registration:name

            if sender_name in clients:  # Если клиент уже есть в базе данных
                continue

            # Добавляем клиента в базу данных
            clients[sender_name] = sender_address
            clients[sender_address] = sender_name

            # Дописываем новых пользователей
            clients_file = open('clients.txt', 'a')

            clients_file.write('{}:{}\n'.format(sender_name, sender_address))
            clients_file.write('{}:{}\n'.format(sender_address, sender_name))

            clients_file.close()

        sender_name = clients[sender_address]  # Получаем имя отправителя сообщения

        # Проверка на тип сообщения
        if 'message:' in data and sender_name in pairs and pairs[sender_name]:  # Должна быть пара игроков
            # Превращаем сообщение в байты
            message = data.split(':')[1]
            info = bytes('data:' + message, encoding='utf-8')

            # Отправляем сообщение
            receiver = clients[pairs[sender_name]]
            sock.sendto(info, receiver)

        if 'start_game_with:' in data:
            receiver_name = data.split(':')[1]

            if receiver_name not in clients:
                continue

            receiver_address = clients[receiver_name]  # Адрес получателя

            if receiver_name in pairs and pairs[receiver_name] == sender_name:  # Если получатель уже отправил запрос
                pairs[sender_name] = receiver_name  # Создаем пару B:A, так как была только A:B

                # Отправляем пользователям подтверждение
                sock.sendto(b'connected', sender_address)
                sock.sendto(b'connected', receiver_address)

            else:  # Создаём запрос на подключение
                pairs[sender_name] = receiver_name

        if 'cancel_invitation' in data:  # Если надо отменить запрос
            if sender_name in pairs.keys():
                del pairs[sender_name]

            if sender_name in pairs.values():
                for key, value in pairs.items():
                    if value == sender_name:
                        del pairs[key]
                        break

    except ConnectionResetError:  # В случае ошибки, когда клиент отключается
        continue
