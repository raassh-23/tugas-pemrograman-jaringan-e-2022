import socket
import logging
import json

server_name = 'localhost'
server_port = 12000

# generated randomly
player_data = {
    '1': {
        'number': 1,
        'name': 'Harmon Alden',
        'position': 'Forward',
    },
    '2': {
        'number': 2,
        'name': 'Mervyn Trent',
        'position': 'Midfielder',
    },
    '3': {
        'number': 3,
        'name': 'Walker Jarrod',
        'position': 'Defender',
    },
    '4': {
        'number': 4,
        'name': 'Joshua Keith',
        'position': 'Goalkeeper',
    },
    '5': {
        'number': 5,
        'name': 'Brion Bryant',
        'position': 'Forward',
    },
    '6': {
        'number': 6,
        'name': 'Rene Lindsey',
        'position': 'Midfielder',
    },
    '7': {
        'number': 7,
        'name': 'Sherman Wayne',
        'position': 'Defender',
    },
    '8': {
        'number': 8,
        'name': 'Hubert Garrett',
        'position': 'Goalkeeper',
    },
    '9': {
        'number': 9,
        'name': 'Kenton Angel',
        'position': 'Forward',
    },
    '10': {
        'number': 10,
        'name': 'Harper Melville',
        'position': 'Midfielder',
    },
    '11': {
        'number': 11,
        'name': 'Tye Silvester',
        'position': 'Defender',
    },
    '12': {
        'number': 12,
        'name': 'Alexis Yancy',
        'position': 'Goalkeeper',
    },
    '13': {
        'number': 13,
        'name': 'Archer Jordan',
        'position': 'Forward',
    },
    '14': {
        'number': 14,
        'name': 'Carey Kevan',
        'position': 'Midfielder',
    },
    '15': {
        'number': 15,
        'name': 'Grover Vergil',
        'position': 'Defender',
    },
    '16': {
        'number': 16,
        'name': 'Perry Hunter',
        'position': 'Goalkeeper',
    },
    '17': {
        'number': 17,
        'name': 'Braden Frazier',
        'position': 'Forward',
    },
    '18': {
        'number': 18,
        'name': 'Kenneth Shanon',
        'position': 'Midfielder',
    },
    '19': {
        'number': 19,
        'name': 'Ezekiel Shelly',
        'position': 'Defender',
    },
    '20': {
        'number': 20,
        'name': 'Malcom Colbert',
        'position': 'Goalkeeper',
    },
    '21': {
        'number': 21,
        'name': 'Trey Alton',
        'position': 'Forward',
    },
    '22': {
        'number': 22,
        'name': 'Charlton Freeman',
        'position': 'Midfielder',
    },
    '23': {
        'number': 23,
        'name': 'Walter Owen',
        'position': 'Defender',
    },
    '24': {
        'number': 24,
        'name': 'Alpha Claude',
        'position': 'Goalkeeper',
    },
    '25': {
        'number': 25,
        'name': 'Ora Boyd',
        'position': 'Forward',
    },
}

def version():
    return 'versi 0.0.1'

def process_request(request_string):
    command_string = request_string.split(' ')
    result = None

    try:
        command = command_string[0].strip()

        if (command == 'get_player_data'):
            logging.warning('Getting data')
            player_number = command_string[1].strip()

            logging.warning(f'Found data for {player_number}')
            result = player_data[player_number]

        elif (command == 'version'):
            result = version()

    except Exception:
        result = None

    return result


def serialized(data):
    serialized = json.dumps(data)

    logging.warning('serializing data')
    logging.warning(serialized)

    return serialized


def run_server(server_address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    logging.warning(f'starting up on {server_address}')
    sock.bind(server_address)

    sock.listen(1000)

    while True:
        logging.warning('waiting for a connection')
        connection, client_address = sock.accept()
        logging.warning(f'Incoming connection from {client_address}')

        data_received = ''
        while True:
            data = connection.recv(32)
            logging.warning(f'received {data}')
            if data:
                data_received += data.decode()
                if '\r\n\r\n' in data_received:
                    result = process_request(data_received)
                    logging.warning(f'Result: {result}')

                    result = serialized(result)
                    result += '\r\n\r\n'
                    connection.sendall(result.encode())
                    break              

            else:
                logging.warning(f'no more data from {client_address}')
                break

if __name__ == '__main__':
    try:
        run_server((server_name, server_port))
    except KeyboardInterrupt:
        logging.warning('Control-C: Stopping program')
        exit(0)
    finally:
        logging.warning('Finished')