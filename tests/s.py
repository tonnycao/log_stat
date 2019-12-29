import socket
import asyncio
from config.config import *

HOST = '0.0.0.0'
PORT = 8080

# soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
# soc.bind((HOST, PORT))
#
# (clientsocket, address) = soc.accept()
# while True:
#     data = clientsocket.recv(1024)
#     if not data: break
#     clientsocket.sendall(data)
# clientsocket.close()


HOST = '127.0.0.1'    # The remote host
PORT = 50007              # The same port as used by the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    msg = 'Hello 曹建90000000000kjjjhdsssssaaaqwer'.encode('utf-8')
    fod = open(DATA_PATH+'/tb_visitor_history.txt')
    txt = fod.readlines(1024*1024*100)
    fod.close()
    msg = ''.join(txt)
    s.sendall(msg.encode('utf-8'))
    data = s.recv(1024*1024*100)
    read_msg = data.decode('utf-8')
print('Received', repr(read_msg))
print('length ', len(data)/1024)


