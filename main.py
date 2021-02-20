#!/usr/bin/python3

from getopt import gnu_getopt
from sys import argv
from zlib import compress, decompress
import socket
import threading
import logging
import rsa

bufferSize = 1024
(PUBLIC_KEY, PRIVATE_KEY) = rsa.newkeys(bufferSize, poolsize=1)
username = 'Anonymous'
peerPublicKey = rsa.PublicKey(0, 0)
PORT = 8080
debugMode = False

# usage: python3 main.py --username=Username --port=8080 --debug
opts, argv = gnu_getopt(argv[1:], 'u:p:d:', ["username=", "port=", 'debug'])  # Fix me
for k, v in opts:
    if k == '-u' or k == '--username':
        username = str(v)
    elif k == '-p' or k == '--port':
        PORT = int(v)
    elif k == '-d' or k == '--debug':
        logging.basicConfig(level=logging.DEBUG)

logging.debug(f'Public key: {PUBLIC_KEY}')
logging.debug(f'Private key: {PRIVATE_KEY}')
logging.debug(f'Username: {username}')
logging.debug(f'Port: {PORT}')
logging.debug(f'Debug: {debugMode}')

addr = []  # If this is empty it means this client want's to start a message
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind(('0.0.0.0', PORT))  # Better to get the IP automatically


def receive():
    global addr
    global peerPublicKey
    while True:
        bytes_address_pair = UDPServerSocket.recvfrom(bufferSize)

        message = bytes_address_pair[0]
        address = bytes_address_pair[1]
        addr.append(address[0])
        addr.append(address[1])

        packet = [hex(b) for b in message]
        handshake = False
        logging.debug(f'{peerPublicKey.e}')

        try:
            key = message.decode('utf-8').split('|', 2)
        except UnicodeDecodeError:
            handshake = True
        if key[0] == 'RSA' and peerPublicKey.e == 0:
            peerPublicKey = rsa.PublicKey(int(key[1]), int(key[2]))
            UDPServerSocket.sendto(f'RSA|{PUBLIC_KEY.n}|{PUBLIC_KEY.e}'.encode('utf-8'), (addr[0], addr[1]))
            logging.debug(f'RSA Key Detected... Peer Public Key: {peerPublicKey}')
            logging.debug(f'RAW Peer Public Key detected: {key}')
        elif key[0] != 'RSA' or handshake:
            message = decompress(message)
            message = rsa.decrypt(message, PRIVATE_KEY)
            message = message.decode('utf-8')

            logging.debug(f'Address: {addr}')
            logging.debug(f'Raw Packet: {str(packet)}')
            logging.debug(f'Decoded Message: {message}')

            if message.count('|') != 0 and message:
                splitter = message.split('|', 1)
                client_username = splitter[0]
                message = splitter[1]
                print(f'[{client_username}] => {message}', end='')


def send():
    global addr
    global peerPublicKey
    while True:
        message = str(input('>>> '))  # Waits for user input
        if not addr or peerPublicKey.e == 0:
            client_address = input("What's the target you want to send the message?: ")
            client_port = input("In which port?: ")
            addr.append(client_address)
            addr.append(int(client_port))

            # Exchange Public Keys using handshake
            logging.debug(f'Sending handshake to {addr[0]}: PUBLIC KEY: {PUBLIC_KEY}')
            UDPServerSocket.sendto(f'RSA|{PUBLIC_KEY.n}|{PUBLIC_KEY.e}'.encode('utf-8'), (addr[0], addr[1]))
        elif message:
            msg = f'{username}|{message}\n'
            msg = msg.encode('utf-8')
            msg = rsa.encrypt(msg, peerPublicKey)
            msg = compress(msg)

            logging.debug(f'Sending compressed message: {msg}')
            UDPServerSocket.sendto(msg, (addr[0], addr[1]))


inbound = threading.Thread(name='Inbound', target=receive)
outbound = threading.Thread(name="Outbound", target=send)
inbound.start()
outbound.start()
inbound.join()
outbound.join()
