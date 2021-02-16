#!/usr/bin/python3

from getopt import gnu_getopt
from sys import argv
import socket
import threading
import logging

logging.basicConfig(level=logging.DEBUG)

username = 'Anonymous'
PORT = 8080
bufferSize = 1024
debugMode = True

# usage: python3 main.py --username=Username --port=8080 --debug
opts, argv = gnu_getopt(argv[1:], 'u:p:d:', ["username=", "port=", 'debug'])  # Fix me
for k, v in opts:
    if k == '-u' or k == '--username':
        username = str(v)
    elif k == '-p' or k == '--port':
        PORT = int(v)
    elif k == '-d' or k == '--debug':
        debugMode = True

if debugMode:
    logging.debug(f'Username: {username}')
    logging.debug(f'Port: {PORT}')
    logging.debug(f'Debug: {debugMode}')

addr = []  # If this is empty it means this client want's to start a message
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind(('0.0.0.0', PORT))  # Better to get the IP automatically


def receive():
    global addr
    while True:
        bytes_address_pair = UDPServerSocket.recvfrom(bufferSize)

        message = bytes_address_pair[0]
        address = bytes_address_pair[1]
        addr.append(address[0])
        addr.append(address[1])

        packet = [hex(b) for b in message]  # For debug purposes
        message = message.decode('utf-8')

        if debugMode:
            logging.debug(f'Address: {addr}')
            logging.debug(f'Raw Packet: {str(packet)}')
            logging.debug(f'Decoded Message: {message}')

        if message.count('|') != 0:
            splitter = message.split('|', 1)
            client_username = splitter[0]
            message = splitter[1]

            print(f'[{client_username}] => {message}')


def send():
    global addr
    while True:
        message = input('> ')  # Waits for user input
        if not addr:
            client_address = input("What's the target you want to send the message?: ")
            client_port = input("In which port?: ")
            addr.append(client_address)
            addr.append(int(client_port))
        elif message != '' or message != ' ':  # Need to put this null or empty right
            msg = f'{username}|{message}\n'
            UDPServerSocket.sendto(msg.encode('utf-8'), (addr[0], addr[1]))


inbound = threading.Thread(target=receive)
outbound = threading.Thread(target=send)
inbound.start()
outbound.start()
inbound.join()
outbound.join()