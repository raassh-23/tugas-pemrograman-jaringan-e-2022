import random
import socket
import json
import logging
import time
import concurrent.futures
import sys
import ssl
import os

server_name = 'localhost'
server_port = 12002

def make_socket(destination_address='localhost', port=12000):
    try:
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.verify_mode=ssl.CERT_OPTIONAL
        context.load_verify_locations(os.getcwd() + '/certs/domain.crt')

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (destination_address, port)
        # logging.warning(f"connecting to {server_address}")
        sock.connect(server_address)

        secure_socket = context.wrap_socket(sock,server_hostname=destination_address)
        # logging.warning(secure_socket.getpeercert())
        
        return secure_socket

    except Exception as ee:
        logging.warning(f'error {str(ee)}')

def deserialized(s):
    # logging.warning(f'deserializing {s.strip()}')
    return json.loads(s)


def send_request(request_str):
    sock = make_socket(server_name, server_port)
    logging.warning(f'connecting to {server_name} for request {request_str.strip()}')

    try:
        # logging.warning(f'sending message ')
        sock.sendall(request_str.encode())

        data_received = ''
        while True:
            data = sock.recv(16)

            if data:
                data_received += data.decode()
                if '\r\n\r\n' in data_received:
                    break
            else:
                break

        result = deserialized(data_received)
        # logging.warning('data received from server:')

        return result
    except Exception as e:
        # logging.warning(f'error during data receiving {str(e)}')
        return False


def get_player_data(number=0):
    request = f'{number}\r\n\r\n'
    result = send_request(request)
    return result

def request_player_data():
    time_request_start = time.perf_counter()

    result = get_player_data(random.randint(1, 25))
    if (result):
        latency = time.perf_counter() - time_request_start
        print(result['name'], result['number'], result['position'])
        print(f'latency: {latency * 1000:.2f} ms')
        return latency
    else:
        print('kegagalan pada data transfer')
        return -1

if __name__ == '__main__':
    worker = int(sys.argv[1]) if len(sys.argv) >= 2 else 5
    request_count = int(sys.argv[2]) if len(sys.argv) >= 3 else 100
    response_count = 0
    latency_sum = 0

    executor = concurrent.futures.ThreadPoolExecutor(max_workers=worker)
    tasks = {}

    time_start = time.perf_counter()
    for i in range(request_count):
        tasks[i] = executor.submit(request_player_data)

    for i in range(request_count):
        result = tasks[i].result()
        if (result != -1):
            response_count += 1
            latency_sum += result
    
    print(f'With {worker} workers')
    print(f'Request count: {request_count}')
    print(f'Response count: {response_count}')
    print(f'Execution time: {(time.perf_counter() - time_start) * 1000:.3f} ms')
    print(f'Average Latency: {(latency_sum / response_count) * 1000:.3f} ms')
