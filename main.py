#!/usr/bin/python3

from getopt import gnu_getopt
from sys import argv
from Connection import ConnectionSingleton
import threading
import logging
import rsa

# Default variables
username = 'Anonymous'
PORT = 8080
bufferSize = 1024

# Generation and initialization of RSA Keys
(PUBLIC_KEY, PRIVATE_KEY) = rsa.newkeys(bufferSize, poolsize=1)
peerPublicKey = rsa.PublicKey(0, 0)

# Default logging level
logging.basicConfig(level=logging.INFO)

# Sets and creates the arguments and flags for initializing the program
# Example usage: python3 main.py --username=Username --port=8080 --debug
opts, argv = gnu_getopt(argv[1:], 'u:p:d:', ["username=", "port=", 'debug'])  # Fix me
for k, v in opts:
    if k == '-u' or k == '--username':
        username = str(v)
    elif k == '-p' or k == '--port':
        PORT = int(v)
    elif k == '-d' or k == '--debug':
        logging.getLogger().setLevel(level=logging.DEBUG)

# Debug Mode Logs
logging.debug(f'Public key: {PUBLIC_KEY}')
logging.debug(f'Private key: {PRIVATE_KEY}')
logging.debug(f'Username: {username}')
logging.debug(f'Port: {PORT}')

connection = ConnectionSingleton.instance(username, "0.0.0.0", PORT, peerPublicKey, PUBLIC_KEY, PRIVATE_KEY, bufferSize)

# Initializes and starts threads running a certain function (either send or receive)
inbound = threading.Thread(name='Inbound', target=connection.receive)
outbound = threading.Thread(name="Outbound", target=connection.send)
inbound.start()
outbound.start()
inbound.join()
outbound.join()
