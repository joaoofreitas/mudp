import socket
import logging
import re
import rsa
from Validation import Regex
from zlib import compress, decompress


class ConnectionSingleton:

    _instance = None
    _username = None
    _address = None
    _port = None
    _UDPServerSocket = None
    _addr = None
    _peerKey = None
    _privateKey = None
    _publicKey = None
    _buffersize = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls, username, address, port, peerKey, publicKey, privateKey, bufferSize):
        if cls._instance is None:
            print('New instance')
            cls._instance = cls.__new__(cls)
            cls._username = username
            cls._address = address
            cls._port = port
            cls._peerKey = peerKey
            cls._publicKey = publicKey
            cls._privateKey = privateKey
            cls._bufferSize = bufferSize

            # Initialization of socket and temporary address variable.
            cls._addr = []  # If this is empty it means this client want's to start a message
            cls._UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
            cls._UDPServerSocket.bind(('0.0.0.0', cls._port))  # Better to get the IP automatically

        else:
            raise RuntimeError('Dispose before creating another instance')

        return cls._instance

    @classmethod
    def dispose(cls):
        cls._instance = None
        print("Instance disposed")

    @staticmethod
    def _connect(address, port):
        print("Connected to " + address + " " + port)

    @classmethod
    def send(cls):
        while True:  # Loops to be always expecting user input
            message = str(input('>>> '))  # User input sanitizing and prompting
            if not cls._addr or cls._peerKey.e == 0:  # Checks if a connection and handshake has been established
                client_address = ''
                client_port = ''
                while not re.search(Regex.ipRegex, client_address):
                    client_address = input("What's the target you want to send the message?: ")

                while not re.search(Regex.portRegex, client_port) or not client_port:
                    client_port = input("In which port?: ")

                cls._addr.append(client_address)
                cls._addr.append(int(client_port))

                # Exchange Public Keys using handshake
                logging.debug(f'Sending handshake to {cls._addr[0]}: PUBLIC KEY: {cls._publicKey}')
                try:
                    cls._UDPServerSocket.sendto(f'RSA|{cls._publicKey.n}|{cls._publicKey.e}'.encode('utf-8'), (cls._addr[0], cls._addr[1]))
                except OSError as error:
                    logging.info("Something went wrong, please try a different IP and/or port number!")
                    logging.debug(f'Error: {error}')
            elif message:  # Creates the message in M-UDP format. Encodes, encrypts, compresses and sends it.
                msg = f'{cls._username}|{message}\n'
                msg = msg.encode('utf-8')
                msg = rsa.encrypt(msg, cls._peerKey)
                msg = compress(msg)

                cls._UDPServerSocket.sendto(msg, (cls._addr[0], cls._addr[1]))
                logging.debug(f'Sending compressed message: {msg}')

    @classmethod
    def receive(cls):
        while True:  # Looping to receive unless commands (to implement #5) or user control

            try:
                datagram_packet = cls._UDPServerSocket.recvfrom(cls._bufferSize)  # Receives the packet with an expected buffer size
                message = datagram_packet[0]
                address = datagram_packet[1]

                if not cls._addr:
                    cls._addr.append(address[0])
                    cls._addr.append(address[1])

                logging.debug(f'Address: {cls._addr}')
                logging.debug(f'Raw Packet: {str([hex(b) for b in message])}')

                # Try to decode, if the message is compressed it will give a UnicodeDecodeError so it's an encrypted message
                try:
                    key = message.decode('utf-8').split('|', 2)
                    # Does a second validation to check if it's a real public key handshake request
                    if key[0] == 'RSA' and cls._peerKey.e == 0:
                        cls._peerKey = rsa.PublicKey(int(key[1]), int(key[2]))
                        cls._UDPServerSocket.sendto(f'RSA|{cls._publicKey.n}|{cls._publicKey.e}'.encode('utf-8'), (cls._addr[0], cls._addr[1]))

                        logging.debug(f'RSA Key Detected... Peer Public Key: {cls._peerKey}')
                        logging.debug(f'RAW Peer Public Key detected: {key}')
                except UnicodeDecodeError:  # Handles has a normal compressed and encrypted message
                    message = decompress(message)
                    message = rsa.decrypt(message, cls._privateKey)
                    message = message.decode('utf-8')

                    logging.debug(f'Decoded Message: {message}')

                    if message.count('|') != 0 and message:  # Separates username from message and print it...
                        splitter = message.split('|', 1)
                        client_username = splitter[0]
                        message = splitter[1]
                        print(f'[{client_username}] => {message}', end='')

            except ConnectionResetError as error:
                logging.info(f'Oops... Connection refused by remote peer!')
                logging.debug(f'Error: {error}')
