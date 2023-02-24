#!/usr/bin/env python3 
# coding: utf-8

import socket
import threading
import sys

class Client:
	def __init__(self, client_sock, hostname):
		self.sock = client_sock
		self.name = ""
		self.HOSTNAME = hostname

	def send_banner(self):
		try:
			banner = f"[ ---------- WELCOME TO THE '{self.HOSTNAME}' CHATROOM ---------- ]"
			self.sock.send(banner.encode('utf-8'))
		except Exception as e:
			print("[error]",str(e))
			self.sock.close()

	def get_name(self):
		try:
			self.name = self.sock.recv(1024).decode('utf-8')
		except Exception as e:
			print("[error]",str(e))
			self.sock.close()
	
	def send_messages(self):
		while True:
			try:
				data = input(f"<{self.HOSTNAME} *>: ")
				data = f"<{self.HOSTNAME}>: "+data
				self.sock.send(data.encode('utf-8'))
			except KeyboardInterrupt:
				self.sock.close()
				break
	
	def recv_messages(self):
		while True:
			try:
				data = self.sock.recv(1024).decode('utf-8')
				if not data: continue
				# prettify data
				print(data)
			except ConnectionResetError:
				print(f"[<{self.name}> left!]")
				self.sock.close()
				break 
		
class Server:
	def __init__(self, ip, port, name, max_connections=5):
		self.HOSTIP = ip 
		self.PORT = port 
		self.HOSTNAME = name 
		self.max_connections = max_connections

		try:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except socket.error as e:
			print("[!] Failed to create a socket")
			print("[error]",str(e))
			sys.exit()

	def chat(self, client):
		try:
			client.send_banner()
			threading.Thread(target=client.send_messages, daemon=True).start()
			threading.Thread(target=client.recv_messages, daemon=True).start()
			threading.Event().wait()
		except KeyboardInterrupt:
			self.sock.shutdown(2)
			print("[shutdown!]")
			sys.exit()
		except ConnectionResetError:
			print(f"[<{self.name}> left!]")
			client.sock.close()
		except Exception as e:
			print("[error]",str(e))
			self.sock.shutdown(2)
			print("[shutdown!]")
			sys.exit()

	def start(self):
		try:
			self.sock.bind((self.HOSTIP, self.PORT))
			# maximum connections 5
			self.sock.listen(self.max_connections)
			print(f"[+] Waiting for Connections at {self.HOSTIP}:{self.PORT}")
			
			while True:
				client_sock, addr = self.sock.accept()
				client = Client(client_sock, self.HOSTNAME)
				client.name = client.get_name()
				print(f"[+] <{client.name}> joined from {addr[0]}:{addr[1]}")
				threading.Thread(target=self.chat, daemon=True, args=(client,)).start()
				# threading.Event().wait()
		except socket.error as e:
			print("[!] Failed to start server")
			print("[error]", str(e))
			sys.exit()

if __name__ == '__main__':
	host = input("Enter host IP: ")
	# port = int(input("Enter Port: "))
	# host = "10.7.10.71"
	port = 1234
	Server(host, port, 'X-Hall').start()
