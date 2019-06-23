import socket
import sys

arguments = sys.argv

HOST = arguments[1]
PORT = 25565
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySocket.connect((HOST,PORT))

mySocket.send(arguments[2])
reply = mySocket.recv(1024)
print reply
