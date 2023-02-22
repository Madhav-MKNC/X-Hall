#!/usr/bin/env python3 
# coding: utf-8

import socket
import _thread
import sys

class Server:
	def __init__(self, ip, port, name):
		self.HOST = ip 
		self.PORT = port 
		self.HOSTNAME = name 
		self.client_name = dict()

		try:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except socket.error as e:
			print("[!] Failed to create a socket")
			print("[error]",str(e))
			sys.exit()
	
	def send_message(self, client):
		while True:
			try:
				data = input(f"<{self.HOSTNAME} *>: ")
				data = f"<{self.HOSTNAME}>: "+data
				client.send(data.encode('utf-8'))
			except KeyboardInterrupt:
				break
    
	def recv_message(self, client):
		while True:
			try:
				data = client.recv(1024).decode('utf-8')
				if not data: continue
				# prettify data
				print(data)
			except ConnectionResetError:
				print(f"[<{self.client_name[client]}> left!]")
				break

	def chat(self, client):
		try:
			client.send("[ ---------- WELCOME TO THE 'X-HALL' CHATROOM ---------- ]".encode('utf-8'))
			_thread.start_new_thread(self.send_message, (client,))
			_thread.start_new_thread(self.recv_message, (client,))
		except KeyboardInterrupt:
			self.sock.shutdown(2)
			print("[shutdown!]")
		except ConnectionResetError:
			print(f"[<{self.client_name[client]}> left!]")
		
	def start(self):
		try:
			self.sock.bind((self.HOST, self.PORT))
			# maximum connections 5
			self.sock.listen(5)
			print(f"[+] Waiting for Connections at {self.HOST}:{self.PORT}")
			
			while True:
				client, addr = self.sock.accept()
				self.client_name[client] = client.recv(1024).decode('utf-8')
				print(f"[+] <{self.client_name[client]}> joined from {addr[0]}:{addr[1]}"	)
				_thread.start_new_thread(self.chat, (client,))
		except socket.error as e:
			print("[!] Failed to start server")
			print("[error]", str(e))
			sys.exit()

if __name__ == '__main__':
	host = "10.184.26.49"
	port = 1234
	Server(host, port, 'X-Hall').start()
