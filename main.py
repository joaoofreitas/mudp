import socket

localIP     = "127.0.0.1"
localPort   = 34000
bufferSize  = 1024

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")

# Listen for incoming datagrams
while(True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    
    
    packet = [hex(b) for b in message]
    message = message.decode('utf-8')
    print(packet)
    print(message)

    # Sending a reply to client
    reply = input() + '\n'
    UDPServerSocket.sendto(str.encode(reply), address)