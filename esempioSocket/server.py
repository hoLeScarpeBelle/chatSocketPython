#dedicated server
import socket
import threading
from reciverClass import *

#var
username = str(input("username: "))
ip = "0.0.0.0"
port = int(input("port number: "))
encoding="utf-8"
bufferSize = 1024# cambiare la possibilita di chiedere
            
#first connection
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('server started')

sock.bind((ip,port))
sock.listen()
ClientSock,addr = sock.accept()
print("connection")
#--username
clientUsername = ClientSock.recv(bufferSize)
clientUsername = clientUsername.decode(encoding)
print("the user "+ clientUsername + " join in the chat")
ClientSock.sendall(bytes(username,encoding))

#--buffersize
ClientSock.sendall(bytes(bufferSize,encoding))# da rifare perche non posso fare questo per fare un operazione cosi stupida

#reciver
servRecv = ServerRecever(ClientSock,bufferSize,encoding,clientUsername)
servRecv.start()#th.join() to finish

#sender
while(True):
    msg = input(">")
    ClientSock.sendall(bytes(msg,encoding))

sock.close()