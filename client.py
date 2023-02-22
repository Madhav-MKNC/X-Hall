#!/usr/bin/env python3 
# coding: utf-8

import socket
import threading
import sys 
import setup

class Client:
    def __init__(self, name):
        self.HOST = setup.Server.ip
        self.PORT = setup.Server.port
        self.HOSTNAME = setup.Server.hostname
        self.NAME = name
        
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e:
            print("[!] Failed to create a socket")
            print("[error]",str(e))
            sys.exit()

    def send_message(self):
        while True:
            try:
                data = input(f"<{self.NAME} *>: ")
                data = f"<{self.NAME}>: "+data
                self.sock.send(data.encode('utf-8'))
            except KeyboardInterrupt:
                break 
    
    def recv_message(self):
        while True:
            try:
                data = self.sock.recv(1024).decode('utf-8')
                if not data: continue
                # prettify data
                print(data)
            except ConnectionResetError:
                print(f"[<{self.HOSTNAME}> Shutdown!]")
                break

    def chat(self):
        try:
            print(self.sock.recv(1024).decode('utf-8'))
            threading.Thread(target=self.send_message, daemon=True).start()
            threading.Thread(target=self.recv_message, daemon=True).start()
            threading.Event().wait() # wait forever
        except KeyboardInterrupt:
            print("[ ---------- You Exited ---------- ]")
            self.sock.shutdown(2)
        except ConnectionResetError:
            print("[ ---------- Connection to server lost ---------- ]")
            self.sock.shutdown(2)
    
    def connect(self):
        try:
            print("[*] Connecting...")
            self.sock.connect((self.HOST,self.PORT))
            self.sock.send(str(self.NAME).encode('utf-8'))
            print(f"[+] Connected to {self.HOSTNAME} at {self.HOST}:{self.PORT}")
            self.chat()
        except socket.error as e:
            print("[error]",e)
            sys.exit()
    

if __name__ == "__main__":
    name = input("[+] Enter your name: ")
    Client(name).connect()
