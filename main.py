#!/usr/bin/python3

from getopt import getopt
from sys import argv
import socket
import threading

localIP     = "127.0.0.1"
localPort   = 34000


# usage: python3 main.py --user=User_2 --ip=127.0.0.1 --port=34000
opts, argv = getopt(argv[1:], 'u:i:p:', ["username=", "ip=", "port="])
for k, v in opts:
    if k == '-u' or k == '--username':
        clientUsername = str(v)
        print(clientUsername)
    elif k == '-i' or k == '--ip':
        localIP = str(v)
        print(localIP)
    elif k == '-p' or k == '--port':
        localPort = int(v)
        print(localPort)

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))

print('MUDP server up and listening')

bufferSize  = 1024
def recieve():
# Listen for incoming datagrams
    while(True):
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]
        print(bytesAddressPair[1])
        packet = [hex(b) for b in message] # For debug purposes
        message = message.decode('utf-8')
        print(packet)
        print(message)

        if message.count('|') != 0:
            spliter = message.split('|', 1)
            username = spliter[0]
            message = spliter[1]

            print(f'[{username}] => {message}')

def send():
    while(True):
        msg = f'{clientUsername}|{input()}\n'
        UDPServerSocket.sendto(msg.encode('utf-8'), (localIP, localPort))

inbound = threading.Thread(target=recieve)
inbound.start()

outbound = threading.Thread(target=send)
outbound.start()
    