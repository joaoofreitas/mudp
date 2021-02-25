#!/usr/bin/python3

from getopt import gnu_getopt
from sys import argv
from zlib import compress, decompress
import socket
import threading
import logging
import rsa
import re

# Default variables
username = 'Anonymous'
PORT = 8080
bufferSize = 1024

# Generation and initialization of RSA Keys
(PUBLIC_KEY, PRIVATE_KEY) = rsa.newkeys(bufferSize, poolsize=1)
peerPublicKey = rsa.PublicKey(0, 0)

# Initialization of socket and temporary address variable.
addr = []  # If this is empty it means this client want's to start a message
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind(('0.0.0.0', PORT))  # Better to get the IP automatically

# Regex for input validation
ipRegex = '^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$'
portRegex = '^((6553[0-5])|(655[0-2][0-9])|(65[0-4][0-9]{2})|(6[0-4][0-9]{3})|([1-5][0-9]{4})|([0-5]{0,5})|([0-9]{1,4}))$'

# Sets and creates the arguments and flags for initializing the program
# Example usage: python3 main.py --username=Username --port=8080 --debug
opts, argv = gnu_getopt(argv[1:], 'u:p:d:', ["username=", "port=", 'debug'])  # Fix me
for k, v in opts:
    if k == '-u' or k == '--username':
        username = str(v)
    elif k == '-p' or k == '--port':
        PORT = int(v)
    elif k == '-d' or k == '--debug':
        logging.basicConfig(level=logging.DEBUG)

# Debug Mode Logs
logging.debug(f'Public key: {PUBLIC_KEY}')
logging.debug(f'Private key: {PRIVATE_KEY}')
logging.debug(f'Username: {username}')
logging.debug(f'Port: {PORT}')


# Receiving function thread. Takes care of handling RSA Public Keys Handshakes, getting and printing messages.
def receive():
    global addr  # Setting variables shared between threads
    global peerPublicKey
    while True:  # Looping to receive unless commands (to implement #5) or user control
        datagram_packet = UDPServerSocket.recvfrom(bufferSize)  # Receives the packet with an expected buffer size

        message = datagram_packet[0]
        address = datagram_packet[1]
        addr.append(address[0])
        addr.append(address[1])

        logging.debug(f'Address: {addr}')
        logging.debug(f'Raw Packet: {str([hex(b) for b in message])}')

        # Try to decode, if the message is compressed it will give a UnicodeDecodeError so it's an encrypted message
        try:
            key = message.decode('utf-8').split('|', 2)
            # Does a second validation to check if it's a real public key handshake request
            if key[0] == 'RSA' and peerPublicKey.e == 0:
                peerPublicKey = rsa.PublicKey(int(key[1]), int(key[2]))
                UDPServerSocket.sendto(f'RSA|{PUBLIC_KEY.n}|{PUBLIC_KEY.e}'.encode('utf-8'), (addr[0], addr[1]))

                logging.debug(f'RSA Key Detected... Peer Public Key: {peerPublicKey}')
                logging.debug(f'RAW Peer Public Key detected: {key}')
        except UnicodeDecodeError:  # Handles has a normal compressed and encrypted message
            message = decompress(message)
            message = rsa.decrypt(message, PRIVATE_KEY)
            message = message.decode('utf-8')

            logging.debug(f'Decoded Message: {message}')

            if message.count('|') != 0 and message:  # Separates username from message and print it...
                splitter = message.split('|', 1)
                client_username = splitter[0]
                message = splitter[1]
                print(f'[{client_username}] => {message}', end='')


# Sending message thread. Handles user input and makes handshake requests and messages.
def send():
    global addr
    global peerPublicKey
    global ipRegex, portRegex
    while True:  # Loops to be always expecting user input
        message = str(input('>>> '))  # User input sanitizing and prompting
        if not addr or peerPublicKey.e == 0:  # Checks if a connection and handshake has been established
            client_address = ''
            client_port = ''
            while not re.search(ipRegex, client_address):
                client_address = input("What's the target you want to send the message?: ")

            while not re.search(portRegex, client_port):
                client_port = input("In which port?: ")

            addr.append(client_address)
            addr.append(int(client_port))

            # Exchange Public Keys using handshake
            logging.debug(f'Sending handshake to {addr[0]}: PUBLIC KEY: {PUBLIC_KEY}')
            UDPServerSocket.sendto(f'RSA|{PUBLIC_KEY.n}|{PUBLIC_KEY.e}'.encode('utf-8'), (addr[0], addr[1]))
        elif message:  # Creates the message in M-UDP format. Encodes, encrypts, compresses and sends it.
            msg = f'{username}|{message}\n'
            msg = msg.encode('utf-8')
            msg = rsa.encrypt(msg, peerPublicKey)
            msg = compress(msg)

            UDPServerSocket.sendto(msg, (addr[0], addr[1]))
            logging.debug(f'Sending compressed message: {msg}')


# Initializes and starts threads running a certain function (either send or receive)
inbound = threading.Thread(name='Inbound', target=receive)
outbound = threading.Thread(name="Outbound", target=send)
inbound.start()
outbound.start()
inbound.join()
outbound.join()
