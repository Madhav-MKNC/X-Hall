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
    
    def send(self, data):
        try:
            self.sock.send(data.encode(ENCODING))
        except ConnectionError:
            self.sock.close()
            print("[Connection lost!]")
            sys.exit()   

    def recv(self):
        try:
            data = self.sock.recv(BUFFERSIZE).decode(ENCODING)
            return data
        except ConnectionError:
            self.sock.close()
            print("[Connection lost!]")
            sys.exit()

    def enter_chatroom(self):
        # This method first sends the user info of the client to the server and then receives a banner or a welcome 
        self.send(self.NAME)
        banner = self.recv()
        print(banner)
    
    def connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e:
            print("[!] Failed to create a socket")
            print("[error]",str(e))
            sys.exit()
        try:
            print(f"[*] Connecting to {self.HOSTIP}:{self.PORT}")
            self.sock.connect((self.HOSTIP,self.PORT))
            print(f"[+] Connected")
            self.enter_chatroom()
            self.chat()
        except Exception as e:
            print("[error]", str(e))
            sys.exit()
    
    def send_messages(self):
        try:
            while True:
                data = input(f"<{self.NAME} *>: ").strip()
                if len(data)==0:
                    continue
                if data.lower() in ["exit", "quit"]:
                    print("[You Exited!]")
                    self.sock.close()
                    sys.exit()
                data = f"<{self.NAME}>: {data}"
                self.send(data)
        except KeyboardInterrupt:
            print("[You Exited!]")
            self.sock.close()
            sys.exit()

    def recv_messages(self):
        while True:
            data = self.recv()
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
    name = input("[ ] Enter your name: ").strip().replace(' ','_')
    Client(name).connect()