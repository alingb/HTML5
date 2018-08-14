#!/usr/bin/env python
# _*_enconding:utf-8_*_
# TIME:2018/6/1 13:40
# FILE:clinet.py

import socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
ip_port = ('127.0.0.1', 9999)
client.connect(ip_port)
while True:
    s = input('Client:').strip()
    if len(s) == 0:
        break
    client.send(bytes(s, encoding='utf-8'))
    if s == 'exit':
        break
    ready_data = str(client.recv((1024)), encoding='utf-8')
    if ready_data.startswith('Ready'):
        msg_size = int(ready_data.split('|')[1])
        client.send(bytes('Start', encoding='utf-8'))
        recv_size = 0
        recv_msg = b''
        while recv_size < msg_size:
            recv_data = client.recv(1024)
            recv_msg += recv_data
            recv_size += len(recv_data)
            print('数据总长：%s,已接收数据长度：%s' % (msg_size, recv_size))
        print('Server:', str(recv_msg, encoding='utf-8'))
