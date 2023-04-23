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
        self.HOSTIP = Host().ip
        self.PORT = Host().port
        self.sys_exit = False
    
    def send(self, data):
        try:
            self.sock.send(data.encode(ENCODING))
        except ConnectionError:
            self.sock.close()
            print("[Connection lost!]")
            self.sys_exit = True

    def recv(self):
        try:
            data = self.sock.recv(BUFFERSIZE).decode(ENCODING)
            return data
        except ConnectionError:
            self.sock.close()
            print("[Connection lost!]")
            self.sys_exit = True

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
            self.sock.close()
    
    def send_messages(self):
        try:
            while True:
                print(f"<{self.NAME} *> ",end="")
                data = input().strip()
                if len(data)==0:
                    continue
                if data.lower() in ["exit", "quit"]:
                    print("[You Exited!]")
                    self.sock.close()
                    self.sys_exit = True
                data = f"<{self.NAME}>: {data}"
                self.send(data)
        except KeyboardInterrupt:
            print("[You Exited!]")
            self.sock.close()
            self.sys_exit = True

    def recv_messages(self):
        try:
            while True:
                data = self.recv()
                if data: print(data)
        except Exception as e:
            print("[error]",str(e))
            self.sock.close()
            self.sys_exit = True

    def chat(self):
        try:
            if self.sys_exit: sys.exit()
            threading.Thread(target=self.send_messages, daemon=True).start()
            threading.Thread(target=self.recv_messages, daemon=True).start()
            threading.Event().wait() # wait forever
        except Exception as e:
            print("[ERROR]",str(e))
        self.sock.close()

if __name__ == "__main__":
    name = input("[ ] Enter your name: ").strip().replace(' ','_')
    Client(name).connect()