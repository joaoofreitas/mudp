#!/usr/bin/python3

from getopt import getopt
from sys import argv
from queue import Empty, Queue
import socket
import threading

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


addr = [] # If this is empty it means this client want's to start a message
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort)) # Better to get the IP automatically

bufferSize  = 1024
def recieve():
    global addr
    # Listen for incoming datagrams
    while(True):
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

        message = bytesAddressPair[0] 
        address = bytesAddressPair[1]

        addr = address

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
    global addr
    # Listen for incoming datagrams
    while(True):
        message = input("Your message: ") # Waits for user input
        if addr == []: 
            a = input("What's the target you want to send the message?: ")
            p = input("In which port?: ")
            addr[0] = a
            addr[1] = p
        else:
            msg = f'{clientUsername}|{message}\n'
            UDPServerSocket.sendto(msg.encode('utf-8'), (addr[0], addr[1]))

inbound = threading.Thread(target=recieve)
outbound = threading.Thread(target=send)
inbound.start()
outbound.start()

inbound.join()
outbound.join()
    