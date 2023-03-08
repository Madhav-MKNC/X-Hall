#!/usr/bin/env python3 
# coding: utf-8

"""
This is setup script which will set the environment for client.py program
"""

import os
import sys
from os import system as cmd

def filterinfo(ip,port):
    try:
        if ip=='localhost':
            if 0<port<65535:
                return ip, port
        elif all(0<i<256 for i in list(map(int,ip.split('.')))) and 0<port<2**16: 
            return ip, port
    except:
        pass
    
    print(ip,port)
    print("[!] Invalid Host IP or Port input, using default [localhost:1234]")
    return 'localhost',1234
    # default host => 'localhost'
    # default port => 1234

class Host:
    def __init__(self) -> None:
        try:
            with open('.hostinfo','r') as file:
                info = file.read()
            self.ip, self.port = filterinfo(info)
        except Exception as e:
            print("[error]",str(e))
            self.ip, self.port = filterinfo(info)
            print("[+] using default [localhost:1234]")
            sys.exit()


if __name__ == "__main__":
    ip = input("[=] Enter Host IP: ")
    port = int(input("[=] Enter port to connect: "))

    ip, port = filterinfo(ip,port)
    info = f"{ip}:{port}"

    file = open('.hostinfo','w')
    file.write(info)
    file.close()
    print("[+] Host info saved")

    try:
        if os.path.exists('requirements.txt'):
            print("[+] Wait for a moment, installing dependencies (requirements.txt)")
            cmd("pip install -r requirements.txt")
    except Exception as e:
        print("[!]",str(e))
    
