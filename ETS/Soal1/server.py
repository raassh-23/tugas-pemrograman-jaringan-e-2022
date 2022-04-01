import socket
import logging
import json

server_name = 'localhost'
server_port = 12000

player_data = {}
with open('../player_data.json', 'r') as f:
    player_data = json.load(f)

def process_request(request_string):
    result = None
    try:
        player_number = request_string.strip()

        logging.warning(f'Found data for {player_number}')
        result = player_data[player_number]
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
