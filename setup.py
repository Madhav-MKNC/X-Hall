#!/usr/bin/env python3 
# coding: utf-8

"""
This is setup script which will set the environment for client.py program
"""

import sys
from os import system as cmd

class Server:
    hostname = "X-Hall"
    ip = input("[ ] Enter Host IP: ")
    port = int(input("[ ] Enter port to connect: "))

