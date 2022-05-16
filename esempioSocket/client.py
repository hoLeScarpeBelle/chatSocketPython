import socket
import threading
from reciverClass import *

# var
ip = str(input("server ip: "))
port = int(input("port: "))
username = str(input("username: "))
encoding = "utf-8"
buffersize = 1024

# first operation
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect((ip,port))

#--username 
sock.sendall(bytes(username,"utf-8"))
serverUsername = sock.recv(buffersize)
serverUsername = serverUsername.decode(encoding)
#--buffersize
buffersize = sock.recv(buffersize)
buffersize = buffersize.decode(encoding)
buffersize = int(buffersize)


#reciver
servRecv = ServerRecever(sock,buffersize,encoding,serverUsername)
servRecv.start()

#sender
while(True):
    msg = str(input(">"))
    sock.sendall(bytes(msg,"utf-8"))


sock.close()