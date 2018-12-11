from websocket_server import WebsocketServer as WSServer

class WebsocketServer():

	def __init__(self, host='0.0.0.0', PORT=8000):

		self.websocket = WSServer(PORT, host=host)

		self.websocket.set_fn_new_client(self.new_client)
		self.websocket.set_fn_client_left(self.client_left)
		self.websocket.set_fn_message_received(self.message_received)

		self.on_message = None
		self.on_closed = None
		self.on_enter = None
		
	def start(self):
		try:
			self.websocket.run_forever()
		except KeyboardInterrupt:
			pass
		

	# Called for every client connecting (after handshake)
	def new_client(self, client, server):
		print("New client connected and was given id %d" % client['id'])
		self.websocket.send_message_to_all("Hey all, a new client has joined us")
		if self.on_enter != None:
			self.on_enter(client)

	# Called for every client disconnecting
	def client_left(self, client, server):
		print("Client(%d) disconnected" % client['id'])
		if self.on_closed != None:
			self.on_closed(client)

	# Called when a client sends a message
	def message_received(self, client, server, message):
		if self.on_message != None:
			self.on_message(message, client)