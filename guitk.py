from faulthandler import disable
from textwrap import fill
import tkinter as tk
from tkinter.constants import NONE, X
from typing import Text
from chatClasses import *

win = tk.Tk()

#window configuration
win.title("chat molto bella")
win.geometry('500x500')
win.rowconfigure(0,weight=1)
win.columnconfigure(0,weight=1)

mainFrame = tk.Frame(win)
chatFrame = tk.Frame(win)
comunicationSocket = ""
username = ""

mainFrame.grid(row=0,column=0,sticky="nswe")
chatFrame.grid(row=0,column=0,sticky="nswe")
mainFrame.lift()

#function

def changePanel(value):
    if(value==0):
        #manca di pulire le entry
        clientConfigFrame.pack_forget()
        serverConfigFrame.pack(side=tk.TOP,expand=1,fill=tk.BOTH)
    else:
        #manca di pulire le entry
        serverConfigFrame.pack_forget()
        clientConfigFrame.pack(side=tk.TOP,expand=1,fill=tk.BOTH)

def sendInfo(selection,ip,port,username,buffersize):
    global comunicationSocket
    try:
        if(selection == 0):#server
            print("ip =" + str(ip) + ";port =" + str(port) + ";username = " + str(username) + ";buffersize =" + str(buffersize))
            #controllo
            port = int(port)
            if(port > 65000 or port < 0):
                print("error port")
                raise Exception("error invalid port number")
            
            buffersize = int(buffersize)
            
            comunicationSocket = chatSocket(0,ip,port,username,buffersize,chatArea,sendMsgButt)
        
        elif(selection == 1):#client
            print("ip =" + str(ip) + ";port =" + str(port) + ";username = " + str(username) + ";buffersize =" + str(buffersize))
            
            numbers = ip.split(".")
            count = 0
            for number in numbers:
                count+=1
                num = int(number)
                if(count > 4):
                    print("error count")
                    raise Exception("error invalid ip")
            if(count < 4):
                raise Exception("error invalid ip")
            
            port = int(port)
            if(port > 65000 or port < 0):
                print("error port")
                raise Exception("error invalid port number")

            comunicationSocket = chatSocket(1,ip,port,username,0,chatArea,sendMsgButt)
        
        else:#group(future)
            print("ip =" + str(ip) + ";port =" + str(port) + ";username = " + str(username) + ";buffersize =" + str(buffersize))

        #start chat
        errorLabel.configure(text="")
        msgEntry.delete(0,tk.END)
        chatFrame.lift()
        comunicationSocket.start()


    except Exception as e:
            print("error format")
            print(e)
            errorLabel.configure(text="" + str(e))
            #mainFrame.lift()

#--------------------------------------------------
#selection frame
selFrame = tk.Frame(mainFrame, background='white',height=80)

#--selection label
tk.Label(selFrame,text='chat role',background='white').grid(column=0,row=0,padx=5,pady=2,sticky=tk.NW)

#--radio button frame
selectionVar = tk.StringVar()

SRBttn = tk.Radiobutton(selFrame,text = 'server',var=selectionVar,value=0,background='white',command=lambda:changePanel(0))
SRBttn.grid(column=0,row=1,padx=5,pady=(5,10) ,sticky=tk.W)

CRButtn = tk.Radiobutton(selFrame,text='client',var=selectionVar,value=1,background='white',command=lambda:changePanel(1))
CRButtn.grid(column=1,row=1,padx=5,pady=(5,10),sticky=tk.W)

selFrame.pack(side=tk.TOP,fill=tk.BOTH,expand=0,anchor=tk.NW)

#-------------------------------------------------
#stupid one side border
tk.Frame(mainFrame,background="black",height=2).pack(side=tk.TOP,fill=tk.X)
#--------------------------------------------------
#server config
serverConfigFrame = tk.Frame(mainFrame)
#serverConfigFrame.pack(side=tk.TOP,expand=1,fill=tk.BOTH)
serverConfigFrame.columnconfigure(2,weight=1)

#--port
tk.Label(serverConfigFrame,text="port:").grid(row = 0 , column = 0, padx = 5 ,pady = 10)
serverPortEntry = tk.Entry(serverConfigFrame)
serverPortEntry.grid(row=0,column=1,padx=5,pady=10)

#--username
tk.Label(serverConfigFrame,text="username:").grid(row=1,column=0,padx=5,pady=10)
serverUsernameEntry = tk.Entry(serverConfigFrame)
serverUsernameEntry.grid(row=1,column=1,padx=5,pady=10)

#--buffersize
tk.Label(serverConfigFrame,text="buffersize:").grid(row=2,column=0,padx=5,pady=10)
serverBufferEntry = tk.Entry(serverConfigFrame)
serverBufferEntry.grid(row=2,column=1,padx=5,pady=10)

#--send button
serverSendButton = tk.Button(serverConfigFrame,text="go",command=lambda:sendInfo(0,"0.0.0.0",serverPortEntry.get(),serverUsernameEntry.get(),serverBufferEntry.get()))
serverSendButton.grid(row=3,column=2,padx=20,pady=50,sticky=tk.E)

#----------------------------------------------------------
#client config
clientConfigFrame = tk.Frame(mainFrame)
#clientConfigFrame.pack(side=tk.TOP,expand=1,fill=tk.BOTH)
clientConfigFrame.columnconfigure(2,weight=1)

#--ip
tk.Label(clientConfigFrame,text="ip:").grid(row=0,column=0,padx=5,pady=10)
clientIpEntry = tk.Entry(clientConfigFrame)
clientIpEntry.grid(row=0,column=1,pady=10,padx=5)

#--port
tk.Label(clientConfigFrame,text="port:").grid(row=1,column=0,padx=5,pady=10)
clientPortEntry = tk.Entry(clientConfigFrame)
clientPortEntry.grid(row=1,column=1,padx=5,pady=10)

#--username
tk.Label(clientConfigFrame,text="username:").grid(row=2,column=0,pady=10,padx=5)
clientUsernameEntry = tk.Entry(clientConfigFrame)
clientUsernameEntry.grid(row=2,column=1,padx=5,pady=10)

#--sendButton selection,ip,port,username,buffersize
clientSendButton = tk.Button(clientConfigFrame,text="go",command=lambda:sendInfo(1,clientIpEntry.get(),clientPortEntry.get(),clientUsernameEntry.get(),"null"))
clientSendButton.grid(row=3,column=2,padx=20,pady=50,sticky=tk.E)

#-----------------------------------------------------------
#chat frame
chatFrame.configure(background="green")

#--top frame
def backFunc():
    try:
        comunicationSocket.close()
    except Exception as e:
        print("error back func: " + str(e))

    mainFrame.lift()

topFrame = tk.Frame(chatFrame)

tk.Label(topFrame,text="chat").pack(side=tk.LEFT,anchor=tk.CENTER,fill=tk.X,expand=1)

backButtn = tk.Button(topFrame,text="X",command=lambda:backFunc())
backButtn.pack(side=tk.RIGHT)

topFrame.pack(side=tk.TOP,anchor=tk.W,fill=tk.X)

#--chat area
chatArea = tk.Text(chatFrame,state='disable',relief='solid',borderwidth=2)
chatArea.pack(side=tk.TOP,expand=1,fill=tk.BOTH)

#--bottom frame
bottomFrame = tk.Frame(chatFrame)
bottomFrame.pack(side=tk.BOTTOM,fill=tk.X)

#----msgEntry
msgEntry = tk.Entry(bottomFrame)
msgEntry.pack(side = tk.LEFT,expand=1,fill=tk.BOTH)

#----sendMsgButt
def insText(text,msg):
    if(sendMsgButt['state'] == "normal"):
        chatArea.configure(state="normal")
        text.insert(tk.END,comunicationSocket.username + ":" + msg + "\n")
        chatArea.configure(state='disable')
        comunicationSocket.sendMsg(msg)
        msgEntry.delete(0,tk.END)

sendMsgButt = tk.Button(bottomFrame,text="send",command=lambda:insText(chatArea,str(msgEntry.get())))
sendMsgButt.pack(side=tk.LEFT)
msgEntry.bind('<Return>',(lambda event:insText(chatArea,str(msgEntry.get()))))#senza lambda esegue la funzione e poi basta

#-----------------------------------------------------------
#error label
errorLabel = tk.Label(mainFrame,text="")
errorLabel.pack(side=tk.BOTTOM,fill=tk.X,expand=1,anchor=tk.S)

#------------------------------------------------------------
def on_closing():
    try:
        comunicationSocket.close()
        comunicationSocket.join()
    except:
        print("brutal closure")
    win.destroy()

win.protocol("WM_DELETE_WINDOW",lambda: on_closing())
win.mainloop()