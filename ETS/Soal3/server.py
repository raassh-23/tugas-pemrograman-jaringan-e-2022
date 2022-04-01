import socket
import threading
import logging
import json
import ssl
import os

server_name = 'localhost'
server_port = 12001

player_data = {}
with open('../player_data.json', 'r') as f:
    player_data = json.load(f)

class HandleRequest(threading.Thread):
	def __init__(self, connection, address):
		self.connection = connection
		self.address = address
		threading.Thread.__init__(self)
		logging.warning(f'{self.name} created')

	def run(self):
		data_received = ''
		while True:
			data = self.connection.recv(32)
			if data:
				data_received += data.decode()

				if '\r\n\r\n' in data_received:
					result = self.process_request(data_received)
					# logging.warning(f'Result: {result}')

					result = self.serialized(result)
					result += '\r\n\r\n'
					self.connection.sendall(result.encode())
					break
			else:
				break

		self.connection.close()

	def serialized(self, data):
		serialized = json.dumps(data)

		# logging.warning('serializing data')
		# logging.warning(serialized)

		return serialized
	
	def process_request(self, request_string):
		result = None
		try:
			player_number = request_string.strip()

			# logging.warning(f'Found data for {player_number}')
			result = player_data[player_number]
		except Exception:
			result = None

		return result

class Server(threading.Thread):
	def __init__(self):
		self.clients = []
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		cert_location = os.getcwd() + '/certs/'
		self.socket_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
		self.socket_context.load_cert_chain(
            certfile=cert_location + 'domain.crt',
            keyfile=cert_location + 'domain.key'
        )
		threading.Thread.__init__(self)

	def run(self):
		server_address = (server_name, server_port)
		logging.warning(f'starting up on {server_address}')
		self.socket.bind(server_address)
		self.socket.listen(1)
		while True:
			logging.warning('waiting for a connection')
			self.connection, self.client_address = self.socket.accept()
			logging.warning(f"connection from {self.client_address}")

			self.connection = self.socket_context.wrap_socket(self.connection, server_side=True)
			
			client = HandleRequest(self.connection, self.client_address)
			client.start()
			self.clients.append(client)

if __name__=="__main__":
	try:
		server = Server()
		server.start()
	except KeyboardInterrupt:
		logging.warning('Control-C: Stopping program')
		exit(0)
	finally:
		logging.warning('Finished')

