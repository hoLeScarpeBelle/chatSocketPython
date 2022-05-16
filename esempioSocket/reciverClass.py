import socket
import threading

#server reciver
class ServerRecever(threading.Thread):
    def __init__(self,socket,buffersize,encoding,clientUsername):
        threading.Thread.__init__(self)
        self.socket = socket
        self.buffersize = buffersize
        self.encoding = encoding
        self.clientUsername = clientUsername

    def run(self):#la classe da cui starta
        print("reciver up")
        while(True):
            msg = self.socket.recv(self.buffersize)
            msg = msg.decode(self.encoding)
            print(self.clientUsername + ':'+ msg)