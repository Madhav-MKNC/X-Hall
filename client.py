#!/usr/bin/env python3
# coding: utf-8

import socket
import threading
import sys
import logging
import setup

logging.basicConfig(level=logging.ERROR)

class Client:
    def __init__(self, name):
        self.HOST = setup.Server.ip
        self.PORT = setup.Server.port
        self.HOSTNAME = setup.Server.hostname
        self.NAME = name
        
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e:
            logging.error("Failed to create a socket")
            logging.error(str(e))
            sys.exit()

    def send_message(self):
        while True:
            try:
                data = input(f"<{self.NAME} *>: ")
                if not data.strip():
                    continue
                if message.lower().strip() in ["$exit", "$quit"]:
                    self.sock.close()
                    print("[You Exited!]")
                data = f"<{self.NAME}>: {data}"
                self.sock.send(data.encode('utf-8'))
            except KeyboardInterrupt:
                logging.error("You Exited")
                self.sock.close()
                break
            except socket.error as e:
                logging.error("Failed to send message")
                logging.error(str(e))
                break
    
    def recv_message(self):
        while True:
            try:
                data = self.sock.recv(1024).decode('utf-8')
                if not data: continue
                # prettify data
                print(data)
            except ConnectionResetError:
                logging.error("Connection to server lost")
                self.sock.close()
                break
            except socket.error as e:
                logging.error("Failed to receive message")
                logging.error(str(e))
                break

    def chat(self):
        try:
            print(self.sock.recv(1024).decode('utf-8'))
            threading.Thread(target=self.send_message, daemon=True).start()
            threading.Thread(target=self.recv_message, daemon=True).start()
            threading.Event().wait() # wait forever
        except KeyboardInterrupt:
            logging.error("You Exited")
            self.sock.close()
        except ConnectionResetError:
            logging.error("Connection to server lost")
            self.sock.close()
        except socket.error as e:
            logging.error("Failed to start chat")
            logging.error(str(e))
            self.sock.close()
    
    def connect(self):
        try:
            print("[*] Connecting...")
            self.sock.connect((self.HOST,self.PORT))
            self.sock.send(str(self.NAME).encode('utf-8'))
            print(f"[+] Connected to {self.HOSTNAME} at {self.HOST}:{self.PORT}")
            self.chat()
        except socket.error as e:
            logging.error("Failed to connect to server")
            logging.error(str(e))
            sys.exit()

if __name__ == "__main__":
    name = input("[+] Enter your name: ")
    Client(name).connect()
