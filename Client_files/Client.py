from socket import *
from threading import *
import json
import math
import os
import time
from time import *
from tkinter import *

class Client():
    def __init__(self,*name):
        #创建socket对象
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        if name:
            self.name =name[0]
        self.buffer_size = 1024
        self.data_gram = 500
        self.send_file_list = {}
        self.save_path = ''
    #给当前的Client对象绑定名字，即用户名
    def set_name(self,name):
        self.name = name
    #像服务器发送登陆的请求
    def login_request(self,name,pw):
        msg_info = json.dumps({'type': 'loginrequest',
                                    'content': {'name':name,'pw':pw}}).encode('utf-8')
        self.client_socket.send(msg_info)
        print('登录请求已发送')
    #向服务器发送注册的请求
    def signup_request(self,name,pw):
        msg_info = json.dumps({'type': 'signuprequest',
                               'content': {'name': name, 'pw': pw}}).encode('utf-8')
        self.client_socket.send(msg_info)
    #连接对应ip和端口的服务器
    def connect_server(self,ip,port):
        # 连接服务，指定主机和端口
        self.client_socket.connect((ip,port))
    #发送文本消息
    def send_msg(self,msg):
        #msg = input()
        #因为当此客户端关闭后，对方会不断收到空信息
        #为了使服务端接收消息正常，认定当空消息时断开连接
        #因此不能在其他时候发送空字符
        if msg:
            msg_info = json.dumps({'type': 'msg',
                                    'content': msg}).encode('utf-8')
            self.client_socket.send(msg_info)
            #self.client_socket.close()
        else:
            print('无内容不得发送')
    #发送表情包消息
    def send_biaoqingbao(self,biaoqingbaoname):
        msg_info = json.dumps({'type': 'biaoqingbao',
                                    'content': biaoqingbaoname
                               }).encode('utf-8')
        self.client_socket.send(msg_info)
    #发送请求下载文件的消息
    def download_file_ack(self,filepath):
        print(filepath)
        msg_info = json.dumps({'type': 'filedownloadack',
                               'content': {'filepath':filepath}}).encode('utf-8')
        self.client_socket.send(msg_info)
    #接收服务器发来的数据
    def receive_data(self):
        data = self.client_socket.recv(self.buffer_size).decode('utf-8')
        if data:
            data_info = json.loads(data)
            return data_info
        else:
            return None
    #向服务器发送文件，会调用下面两个方法
    def send_file(self,filepath):
        (path, file) = os.path.split(filepath)
        (filename, extension) = os.path.splitext(file)
        filesize=os.stat(filepath).st_size
        self.send_file_list[(filename,extension,filesize)] = filepath
        send_thread = Thread(target=self.send_file_header_thread, args=(filepath,))
        #send_thread.setDaemon(True)
        send_thread.run()
    #向服务器发送文件描述信息
    def send_file_header_thread(self,filepath):
        (path, file) = os.path.split(filepath)
        (filename, extension) = os.path.splitext(file)
        filesize = os.stat(filepath).st_size
        #先把整个文件的头部以JSON的格式发送过去
        current_data_bag_info = {'type': 'file',
                                 'filename': filename,
                                 'fileextension': extension,
                                 'filesize': filesize,
                                 'sendername':self.name,
                                 'sendertime':strftime("%m-%d %a %H:%M:%S",localtime())}
        bytes_length = len(json.dumps(current_data_bag_info).encode('utf-8'))
        str = ''
        for i in range(1011 - bytes_length):
            str += '0'
        current_data_bag_info['blank'] = str
        # print(will_send)
        will_send = json.dumps(current_data_bag_info).encode('utf-8')
        #print(len(will_send))
        self.client_socket.send(will_send)
        #time.sleep(1)
        self.send_file_bytes(filepath)
    #将文件转为bytes发送给服务器
    def send_file_bytes(self,filepath):
        #filepath = self.send_file_list[(filename,extension,filesize)]
        #开始循环分段发送文件
        file = open(filepath, 'rb')
        while True:
            filedata = file.read(self.data_gram)
            #print(filedata)
            #print(filedata)
            if not filedata:
               break
            else:
                self.client_socket.send(filedata)
    #接收服务器发来的文件，存入“缓存”本地文件夹
    def receive_file(self,filesize,filename,fileextension):
        print('开始接收文件')
        received_length = 0
        file_data = b''
        need_receive_file_size = filesize
        #print(filesize)
        while True:
            #以最大缓存获取
            part_data = self.client_socket.recv(self.buffer_size)

            print(part_data)
            #print(len(part_info['content']))
            #print(part_info['content'])
            #拼接文件字节流数据
            file_data += part_data
            print(part_data)
            received_length += len(part_data)
            if received_length == filesize:
                break
        print('接收完成，准备写入')
        # 合成文件名及存储相对路径，进行存储
        path = os.path.join('./Client_files/buffer_files', filename+fileextension)
        current_file = open(path,'wb')
        current_file.write(file_data)
        current_file.close()
    #接收服务器发来的文件，存入本地自定义的文件夹
    def receive_file_in_diypath(self,chatbox,filesize,filename,fileextension,filepath):
        print('开始接收文件')
        received_length = 0
        file_data = b''
        need_receive_file_size = filesize
        #print(filesize)
        while True:
            #以最大缓存获取
            part_data = self.client_socket.recv(self.buffer_size)

            print(part_data)
            #print(len(part_info['content']))
            #print(part_info['content'])
            #拼接文件字节流数据
            file_data += part_data
            print(part_data)
            received_length += len(part_data)
            if received_length == filesize:
                break
        print('接收完成，准备写入')
        # 合成文件名及存储相对路径，进行存储
        print(filepath)
        print(filename)
        print(fileextension)
        path = os.path.join(filepath+'/', filename+fileextension)
        current_file = open(path,'wb')
        current_file.write(file_data)
        current_file.close()

        self.send_msg(filename+fileextension+'已接收\n')

        speaker = Label(chatbox.intereaction, text=self.name + '  (' + strftime("%m-%d %a %H:%M:%S", localtime()) + ')', fg='#1E90FF', bg='white')
        content = Label(chatbox.intereaction,text=filename+fileextension+'已接受',fg='#A9A9A9',bg = 'white')

        chatbox.canvas.create_window((500, chatbox.msg_list_length), window=speaker, anchor='ne')
        chatbox.canvas.create_window((500, chatbox.msg_list_length + 25), window=content, anchor='ne')

        chatbox.msg_list_length += 50
        chatbox.canvas["scrollregion"] = "%d %d %d %d" % (0, 0, 600, chatbox.msg_list_length+20)
        chatbox.canvas.yview_moveto(1)
    #向服务器发出关闭连接的消息
    def close_connect(self):
        msg_info = json.dumps({'type': 'close',
                               'content': ''}).encode('utf-8')
        self.client_socket.send(msg_info)

        #sys.exit(0)

if __name__ == '__main__':
    test = Client('lin')
    test.connect_server('10.131.1.229',1234)
    #test.send_msg('lin')
    test.send_file(r'C:\Users\lenovo\Desktop\任务占比-柱形.png')