#!/usr/bin/env python3 
# coding: utf-8

# title: X-HALL server
# author: Madhav Kumar (https://github.com/Madhav-MKNC)
# created: 20th Feb 2023

import socket
import threading
import sys

from constants import BUFFERSIZE, ENCODING, MAX_CONNECTIONS
from utils import get_username

# INNER Class STUFF TO BE DONE
class Client:
    def __init__(self, client_sock, hostname):
        self.sock = client_sock
        self.name = ""
        self.HOSTNAME = hostname
    
    def exists(self, name):
        # check the username if already active on the server
        return False

    def send_banner(self):
        banner = f"[ ---------- WELCOME TO THE '{self.HOSTNAME}' CHATROOM ---------- ]"
        self.send_message(banner)

    def set_username(self):
        self.send_message(f"[username? @{self.HOSTNAME}] ")
        response = self.recv_message().strip()
        if len(response)>0 and self.exists(response)==False:
            self.name = response
        else:
            self.name = get_username()
            self.send_message(f"[{self.HOSTNAME}] Username Invalid! You are {self.name}")

    def send_message(self, message):
        try:
            message = f"<{self.name}>@{self.HOSTNAME}: "+message
            self.sock.send(message.encode(ENCODING))
        except ConnectionError:
            print(f"[<{self.name}> DISCONNECTED!]")
            self.sock.close()

    def recv_message(self):
        try:
            data = self.sock.recv(BUFFERSIZE).decode(ENCODING)
            return data
        except ConnectionError:
            print(f"[<{self.name}> DISCONNECTED!]")
            self.sock.close()


class Server:
    def __init__(self, ip, port, hostname):
        self.HOSTIP = ip 
        self.PORT = port 
        self.HOSTNAME = hostname 
        self.clients = []

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e:
            print("[!] Failed to create a socket")
            print("[error]",str(e))
            sys.exit()

    def chat(self, client):
        try:
            client.send_banner()
            client.get_name()
            self.broadcast(f"[+] <{client.name}> joined the chat room.")
            self.clients.append(client)
            threading.Thread(target=client.send_messages, daemon=True).start()
            threading.Thread(target=client.recv_messages, daemon=True).start()
            threading.Event().wait()
        except KeyboardInterrupt:
            self.sock.shutdown(2)
            print("[shutdown!]")
            sys.exit()
        except ConnectionResetError:
            self.clients.remove(client)
            self.broadcast(f"[<{client.name}> left!]")
            client.sock.close()
        except Exception as e:
            print("[error]",str(e))
            self.sock.shutdown(2)
            print("[shutdown!]")
            sys.exit()

    def broadcast(self, message):
        for client in self.clients:
            try:
                client.send_message(message)
            except:
                self.clients.remove(client)

    def start(self):
        try:
            self.sock.bind((self.HOSTIP, self.PORT))
            # maximum connections 5
            self.sock.listen(MAX_CONNECTIONS)
            print(f"[+] Waiting for Connections at {self.HOSTIP}:{self.PORT}")
            
            while True:
                client_sock, addr = self.sock.accept()
                client = Client(client_sock, self.HOSTNAME)
                print(f"[+] New client connected from {addr[0]}:{addr[1]}")
                threading.Thread(target=self.chat, daemon=True, args=(client,)).start()
                # threading.Event().wait()
        except socket.error as e:
            print("[!] Failed to start server")
            print("[error]", str(e))
            sys.exit()




if __name__ == '__main__':   
    try: 
        host = input("Enter host IP: ")
        # port = int(input("Enter Port: "))
        # host = "10.7.10.71"
        port = int(input("Enter port: "))
    except:
        # defaults
        host = "localhost"
        port = 1234
    Server(host, port, 'X-Hall').start()
	