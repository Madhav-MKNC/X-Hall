#!/usr/bin/env python3 
# coding: utf-8

# title: X-HALL client
# author: Madhav Kumar (https://github.com/Madhav-MKNC)
# created: 20th Feb 2023

import socket
import threading
import sys
from setup import Host
from constants import *

# client class
class Client:
    def __init__(self, name):
        self.NAME = name

        # host info
        self.HOSTIP = Host().ip
        self.PORT = Host().port

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e:
            print("[!] Failed to create a socket")
            print("[error]",str(e))
            sys.exit()
    
    def send_data(self, data):
        try:
            self.sock.send(data.encode(ENCODING))
        except ConnectionError:
            self.sock.close()
            print("[Connection to server lost!]")
            sys.exit()   

    def recv_data(self):
        try:
            data = self.sock.recv(BUFFERSIZE).decode(ENCODING)
            return data
        except ConnectionError:
            self.sock.close()
            print("[Connection to server lost!]")
            sys.exit()

    def enter_chatroom(self):
        # This method first sends the user info of the client to the server and then receives a banner or a welcome 
        self.send_data(self.NAME)
        banner = self.recv_data()
        print(banner)
    
    def connect(self):
        try:
            print(f"[*] Connecting to {self.HOSTIP}:{self.PORT}")
            self.sock.connect((self.HOSTIP,self.PORT))
            print(f"[+] Connected")
            self.enter_chatroom()
            self.chat()
        except Exception as e:
            print("[-] Failed to connect to server")
            print(str(e))
            sys.exit()
    
    def send_messages(self):
        try:
            while True:
                data = input(f"<{self.NAME} *>: ").strip()
                if len(data)==0:
                    continue
                if data.lower() in ["$exit", "$quit"]:
                    print("[You Exited!]")
                    break
                data = f"<{self.NAME}>: {data}"
                self.send_data(data)
        except KeyboardInterrupt:
            print("[You Exited!]")
            self.sock.close()

    def recv_messages(self):
        while True:
            data = self.recv_data()
            if not data: continue
            print(data)

    def chat(self):
        try:
            threading.Thread(target=self.send_messages, daemon=True).start()
            threading.Thread(target=self.recv_messages, daemon=True).start()
            threading.Event().wait() # wait forever
        except Exception as e:
            print("[ERROR]",str(e))
        self.sock.close()

if __name__ == "__main__":
    name = input("[ ] Enter your name: ")
    Client(name).connect()