import socket
import time
from datetime import datetime
#create clientsocket
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("localhost",80))

full_msg = ''
while True:
    #buffer the message
    msg = s.recv(16)
    time.sleep(1) # comment this out if you dont want to wait for all data to be transferred
    #check if there is recieved data from server left
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    if len(msg) <= 0:
        break
    #decode the bytes
    print("Recieved["+current_time+"] : "+msg.decode("utf-8"))
