import random
import socket
import json
import logging
import time
import threading
import sys
import ssl
import os

server_name = '172.16.16.101'
server_port = 12002

def make_socket(destination_address='localhost', port=12000):
    try:
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.verify_mode=ssl.CERT_OPTIONAL
        context.load_verify_locations(os.getcwd() + '/certs/domain.crt')

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (destination_address, port)
        sock.connect(server_address)
        secure_socket = context.wrap_socket(sock, server_hostname=destination_address)
        
        return secure_socket

    except Exception as ee:
        logging.warning(f'error {str(ee)}')

def deserialized(s):
    return json.loads(s)


def send_request(request_str):
    sock = make_socket(server_name, server_port)
    logging.warning(f'connecting to {server_name} for request {request_str.strip()}')

    try:
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

        return result
    except Exception as e:
        logging.warning(f'error during data receiving {str(e)}')
        return False


def get_player_data(number=0):
    request = f'{number}\r\n\r\n'
    result = send_request(request)
    return result

def request_player_data(index, results):
    time_request_start = time.perf_counter()

    result = get_player_data(random.randint(1, 25))
    if (result):
        latency = time.perf_counter() - time_request_start
        print(result['name'], result['number'], result['position'])
        print(f'latency: {latency * 1000:.2f} ms')
        results[index] = latency
    else:
        print('kegagalan pada data transfer')
        results[index] = -1

if __name__ == '__main__':
    thread_count = int(sys.argv[1]) if len(sys.argv) >= 2 else 5
    request_count = int(sys.argv[2]) if len(sys.argv) >= 3 else 100
    response_count = 0
    latency_sum = 0

    tasks = {}
    results = {}

    time_start = time.perf_counter()
    loops = request_count
    while loops > 0:
        loops_inner =  thread_count if loops >= thread_count else loops

        for i in range(loops_inner):
            tasks[loops - i] = threading.Thread(target=request_player_data, args=(loops - i, results))
            tasks[loops - i].start()

        for i in range(loops_inner):
            tasks[loops - i].join()
            if (results[loops - i] != -1):
                response_count += 1
                latency_sum += results[loops - i]

        loops -= loops_inner

    time_end = time.perf_counter()
    
    print(f'With {thread_count} threads')
    print(f'Request count: {request_count}')
    print(f'Response count: {response_count}')
    print(f'Average Latency: {(latency_sum / response_count) * 1000:.3f} ms')
    print(f'Execution time: {(time_end - time_start) * 1000:.3f} ms')
