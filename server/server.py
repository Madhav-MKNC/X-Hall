#!/usr/bin/env python3 
# coding: utf-8

# title: X-HALL server
# author: Madhav Kumar (https://github.com/Madhav-MKNC)
# created: 20th Feb 2023

import socket
import threading
import sys
from constants import BUFFERSIZE, ENCODING, MAX_CONNECTIONS
from utils import get_username, filterinfo

# INNER Class STUFF TO BE DONE
class Client:
    def __init__(self, client_sock, hostname):
        self.sock = client_sock
        self.name = ""
        self.HOSTNAME = hostname
    
    def exists(self, name):
        # check the username if already active on the server (INNER CLASS implementation will fix this)
        return False

    def set_username(self):
        response = self.recv()
        if len(response)>0 and self.exists(response)==False:
            self.name = response
        else:
            self.name = get_username()
            self.send(f"[{self.HOSTNAME}] Username Invalid! You are {self.name}")
    
    def send_banner(self):
        banner = f"[ ---------- WELCOME TO THE '{self.HOSTNAME}' CHATROOM ---------- ]"
        self.send(banner)

    def send(self, message):
        try:
            self.sock.send(message.encode(ENCODING))
        except ConnectionError:
            print(f"[<{self.name}> DISCONNECTED!]")
            self.sock.close()

    def recv(self):
        try:
            data = self.sock.recv(BUFFERSIZE).decode(ENCODING)
            return data
        except ConnectionError:
            print(f"[<{self.name}> DISCONNECTED!]")
            self.sock.close()
    
    def send_messages(self):
        while True:
            try:
                message = input(f"<{self.HOSTNAME} *> ").strip()
                if len(message)==0: continue
                if message=="shutdown":
                    # self.shutdown()
                    print("[shutdown!]")
                    sys.exit()
                message = f"<{self.HOSTNAME} *> "+message
                self.send(message)
            except Exception as e:
                print("[error]",str(e))
                break

    def recv_messages(self):
        while True:
            try:
                data = self.recv()
                if data: print(data)
            except Exception as e:
                print("[error]",str(e))
                break
    



class Server:
    def __init__(self, ip, port, hostname):
        self.HOSTIP = ip 
        self.PORT = port 
        self.HOSTNAME = hostname 
        self.clients = []

    def chat(self, client):
        try:
            client.send_banner()
            client.set_username()
            self.clients.append(client)
            self.broadcast(f"[+] <{client.name}> joined the chat room.")
            threading.Thread(target=client.send_messages, daemon=True).start()
            threading.Thread(target=client.recv_messages, daemon=True).start()
            threading.Event().wait()
        except KeyboardInterrupt:
            self.sock.shutdown(2)
            print("[shutdown!]")
            sys.exit()
        except ConnectionError:
            self.clients.remove(client)
            self.broadcast(f"[<{client.name}> left!]")
            client.sock.close()
        except Exception as e:
            print("[error]",str(e))
            self.sock.close()
            sys.exit()

    def broadcast(self, message):
        for client in self.clients:
            try:
                client.send(message)
            except:
                self.clients.remove(client)
                self.broadcast(f"[<{client.name}> left!]")

    def start(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
    host = input("Enter host IP: ")
    # port = int(input("Enter Port: "))
    # host = "10.7.10.71"
    port = input("Enter port: ")
    host, port = filterinfo(host, port)

    Server(host, port, 'X-Hall').start()
	