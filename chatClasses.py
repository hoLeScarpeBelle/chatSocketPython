import tkinter as tk
import threading
import socket


class chatSocket(threading.Thread):
    def __init__(self,type,ip,port,username,buffersize,textArea,button):
        threading.Thread.__init__(self)
        self.type = type
        self.ip = ip
        self.port = port
        self.username = username
        self.buffersize = buffersize
        self.textArea = textArea
        self.sendButton = button
        self.encoding = "utf-8"
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        if(type == 0):#server
            self.sock.bind((ip,port))
            self.serverSock = self.sock
        elif(type == 1):#client
            self.sock.connect((ip,port))
        elif(type == 2):#group
            print("")

    def run(self):
        self.sendButton.configure(state='disable')
        
        self.textArea.configure(state='normal')
        self.textArea.delete(1.0,tk.END)#per eliminare una chat precedente
        self.textArea.insert(tk.END,"----waiting connection----")
        self.textArea.configure(state='disable')
        
        if(self.type == 0):#server
            self.sock.listen()
            clientSock,addr = self.sock.accept()

            #buffersize
            clientSock.sendall(bytes(str(self.buffersize),self.encoding))
            #username
            self.otherUsername = clientSock.recv(self.buffersize)
            self.otherUsername = self.otherUsername.decode(self.encoding)
            clientSock.sendall(bytes(self.username,self.encoding))

            self.sock = clientSock#la lascero ma non ideale perche si perde il socket del server che fortunatamente in questo caso non se ne avra piu bisogno

        elif(self.type == 1):#client
            #buffersize
            self.buffersize = self.sock.recv(1024)
            self.buffersize = self.buffersize.decode(self.encoding)
            self.buffersize = int(self.buffersize)

            #username
            self.sock.sendall(bytes(self.username,self.encoding))
            self.otherUsername = self.sock.recv(self.buffersize)
            self.otherUsername = self.otherUsername.decode(self.encoding)
        elif(self.type == 2):#group
            print("")

        self.textArea.configure(state='normal')
        self.textArea.delete(1.0,tk.END)
        self.textArea.configure(state='disable')
        self.textArea.insert(tk.END,"-------all user are connected-------\n")
        self.sendButton.configure(state='normal')

        while(True):
            msg = self.sock.recv(self.buffersize)
            msg = msg.decode(self.encoding)
            self.textArea.configure(state = 'normal')
            
            if(msg != "~quit()~"):
                self.textArea.insert(tk.END,self.otherUsername + ":" + msg + "\n")
                self.textArea.configure(state = 'disable')
            else:
                self.textArea.insert(tk.END,"-------"+ self.otherUsername + " has left the chat-------\n")
                self.textArea.configure(state = 'disable')
                self.sendButton.configure(state='disable')
                break

    def sendMsg(self,msg):
        self.sock.sendall(bytes(msg,self.encoding))

    def close(self):
        try:
            self.sock.sendall(bytes("~quit()~",self.encoding))
        except:
            print("send problem")

        if(self.type != 1):#server/group
            self.sock.close()
            self.serverSock.close()
        else:#client
            self.sock.close()