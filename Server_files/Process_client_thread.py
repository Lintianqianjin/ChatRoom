from socket import *
import threading
from time import *
import json
import os

class Process_client_thread(threading.Thread):
    def __init__(self,client_socket, Server,BUFFER_SIZE):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.buffer_size = BUFFER_SIZE
        self.server = Server
        self.data_gram=500
    #循环接受客户端发来的消息
    def run(self):
        while True:
            data_info = self.receive_data()
            if data_info is None:
                continue
            else:
                if data_info['type'] == 'msg':
                    msg = data_info['content']
                    print(msg)
                    #测试发现客户端close后，会不断收到空字符，所以需要加此判断。
                    if msg:
                        #print(msg.decode('utf-8'))
                        speaker_name = self.server.clients_names[self.client_socket]
                        time = strftime("%m-%d %a %H:%M:%S",localtime())
                        will_send_msg = (speaker_name + ',' + time + ','+msg)
                        self.broadcast(will_send_msg)
                    else:
                        self.client_socket.close()
                        break
                    #break
                elif data_info['type']=='file':
                    self.receive_file(filename=data_info['filename'],fileextension=data_info['fileextension'],filesize=data_info['filesize'])
                    if data_info['fileextension'] in ['.bmp','.jpg','.png','.jpeg']:
                        path = os.path.join('./Server_files/buffer_files', data_info['filename'] + data_info['fileextension'])
                        self.broadcast_img(path,data_info['sendername'],data_info['sendertime'])
                    elif data_info['fileextension'] == '.wav':
                        path = os.path.join('./Server_files/buffer_files', data_info['filename'] + data_info['fileextension'])
                        self.broadcast_audio(path,data_info['sendername'],data_info['sendertime'])
                    else:
                        path = os.path.join('./Server_files/buffer_files',
                                            data_info['filename'] + data_info['fileextension'])
                        self.broadcast_filerecack(path, data_info['sendername'], data_info['sendertime'])
                elif data_info['type']=='filedownloadack':
                    threading.Thread(target=self.send_file,
                                     args=(self.client_socket,
                                           data_info['content']['filepath'],
                                           'server_from_'+self.server.clients_names[self.client_socket],
                                           strftime("%m-%d %a %H:%M:%S", localtime()),)).run()
                elif data_info['type']=='biaoqingbao':
                    speaker_name = self.server.clients_names[self.client_socket]
                    time = strftime("%m-%d %a %H:%M:%S", localtime())
                    will_send_msg = (speaker_name + ',' + time + ',' + data_info['content'])
                    self.broadcast_biaoqingbao(will_send_msg)
                elif data_info['type'] == 'loginrequest':
                    print('接收到登录请求')
                    self.check_login(data_info['content']['name'],data_info['content']['pw'])
                elif data_info['type'] == 'signuprequest':
                    print('收到注册请求')
                    self.check_signup(data_info['content']['name'],data_info['content']['pw'])
                elif data_info['type'] == 'nameinfo':
                    name = data_info['content']
                    print(name + '已连接')
                    # 将新用户的名字广播给各个用户，让他们的用户列表里添加该用户
                    self.broadcast('NamesInRoom,' + name)
                    self.server.clients_names[self.client_socket] = name
                    # 对于该新进入的用户来说，他没有之前的用户列表，所以将所有的用户发送给他
                    NamesInRoom = ''
                    for client_socket in self.server.clients_names:
                        if client_socket != self.client_socket:
                            NamesInRoom += ',' + self.server.clients_names[client_socket]
                    self.send_msg('NamesInRoom' + NamesInRoom)
                elif data_info['type'] == 'close':
                    print(self.server.clients_names[self.client_socket]+'断开连接')
                    #在当前服务器需要通讯的用户列表中删除该用户
                    name = self.server.clients_names.pop(self.client_socket)
                    self.broadcast_someone_leave(name)
                    self.close_connect()
                    break
        #SHUT_RDWR参数为关闭读和写的通道，python先shutdown在close是合理的关闭
        self.client_socket.shutdown(SHUT_RDWR)
        self.client_socket.close()
    #从客户端接收文件
    def receive_file(self,filesize,filename,fileextension):
        received_length = 0
        file_data = b''
        need_receive_file_size = filesize
        print(filesize)
        print('开始接收')
        while True:
            #以最大缓存获取或仅读取文件的最后一部分（不足1024字节）
            part_data = self.client_socket.recv(min(self.buffer_size,need_receive_file_size-received_length))

            #拼接文件字节流数据
            file_data += part_data
            received_length += len(part_data)
            if received_length == filesize:
                break
        # 合成文件名及存储相对路径，进行存储
        print('接收完成')
        path = os.path.join('./Server_files/buffer_files', filename+fileextension)
        current_file = open(path,'wb')
        current_file.write(file_data)
        current_file.close()
    #从客户端接收消息
    def receive_data(self):
        data = self.client_socket.recv(self.buffer_size).decode('utf-8')
        if data:
            return json.loads(data)
        else:
            return None
    #像客户端发送文本消息
    def send_msg(self,msg):
        msg_info = json.dumps({'type': 'msg',
                               'content': msg}).encode('utf-8')
        #print('已发送')
        self.client_socket.send(msg_info)
        #self.client_socket.send(msg.encode('utf-8'))
    #关闭与当前客户端的连接，发送关闭消息
    def close_connect(self):
        msg_info = json.dumps({'type': 'close',
                               'content': ''}).encode('utf-8')
        self.client_socket.send(msg_info)
    #检查登陆的账号密码，并反馈给用户是否成功
    def check_login(self,name,pw):
        if name not in self.server.clients_name_pw.keys():
            msg_info = json.dumps({'type': 'loginreply',
                                   'content': {'result': False, 'reason': '用户名不存在'}}).encode('utf-8')
            self.client_socket.send(msg_info)
            print('用户名不存在已发送')
        elif self.server.clients_name_pw[name] != pw:
            msg_info = json.dumps({'type': 'loginreply',
                                   'content': {'result': False, 'reason': '密码错误'}}).encode('utf-8')
            self.client_socket.send(msg_info)
            print('密码错误已发送')
        else:
            msg_info = json.dumps({'type': 'loginreply',
                                   'content': {'result': True, 'reason': '验证通过'}}).encode('utf-8')
            self.client_socket.send(msg_info)
            print('登陆成功已发送')
    #检查注册的用户名，并反馈给用户是否成功，新用户的消息要存入本地
    def check_signup(self,name,pw):
        if name in self.server.clients_name_pw.keys():
            msg_info = json.dumps({'type': 'signupreply',
                                   'content': {'result':False, 'reason': '用户名已存在'}}).encode('utf-8')
            self.client_socket.send(msg_info)
            #print('已发送注册回复')
        else:
            self.server.clients_name_pw[name] = pw
            threading.Thread(target=self.add_user,args=(name,pw,)).start()
            msg_info = json.dumps({'type': 'signupreply',
                               'content': {'result': True, 'reason': '注册成功'}}).encode('utf-8')
            self.client_socket.send(msg_info)
            #print('已发送注册回复')
    #添加新用户到本地用户文件
    def add_user(self,name,pw):
        users = open('./Server_files/buffer_files/init/users.txt','a+',encoding='utf-8')
        users.write(name+'\t'+pw+'\n')
        users.close()
    #向客户端发送文件，会调用下面两个方法
    def send_file(self,client_socket,filepath,sender,sendtime):
        send_thread = threading.Thread(target=self.send_file_header_thread, args=(client_socket,filepath,sender,sendtime,))
        #send_thread.setDaemon(True)
        send_thread.run()
    #向客户端发送文件描述信息
    def send_file_header_thread(self,client_socket,filepath,sender,sendtime):
        (path, file) = os.path.split(filepath)
        (filename, extension) = os.path.splitext(file)
        filesize = os.stat(filepath).st_size
        #先把整个文件的头部以JSON的格式发送过去
        current_data_bag_info = {'type': 'file',
                                 'filename': filename,
                                 'fileextension': extension,
                                 'filesize': filesize,
                                 'sendername':sender,
                                 'sendertime':sendtime
                                 }
        bytes_length = len(json.dumps(current_data_bag_info).encode('utf-8'))
        str = ''
        for i in range(1011 - bytes_length):
            str += '0'
        current_data_bag_info['blank'] = str
        # print(will_send)
        will_send = json.dumps(current_data_bag_info).encode('utf-8')
        #print(len(will_send))
        client_socket.send(will_send)
        #time.sleep(1)
        self.send_file_bytes(client_socket=client_socket,filepath=filepath)
    #将文件以bytes的形式发送给客户端
    def send_file_bytes(self,client_socket,filepath):
        #filepath = self.send_file_list[(filename,extension,filesize)]
        #开始循环分段发送文件
        file = open(filepath, 'rb')
        print('循环发送文件中')
        while True:
            filedata = file.read(self.data_gram)
            #print(filedata)
            #print(filedata)
            if not filedata:
               break
            else:
                client_socket.send(filedata)
    #广播文本消息
    def broadcast(self, msg):
        msg_info = json.dumps({'type': 'msg',
                               'content': msg}).encode('utf-8')
        #print('广播正常')
        for client_socket in self.server.clients_names:
            if client_socket != self.client_socket:
                client_socket.send(msg_info)
    #广播表情包消息
    def broadcast_biaoqingbao(self,senderinfo_and_biaoqingbaoname):
        msg_info = json.dumps({'type': 'biaoqingbao',
                               'content': senderinfo_and_biaoqingbaoname}).encode('utf-8')

        for client_socket in self.server.clients_names:
            client_socket.send(msg_info)
    #广播可以直接发在消息框中的图片
    def broadcast_img(self,filepath,sender,sendtime):
        for client_socket in self.server.clients_names:
            #if client_socket != self.client_socket:
            print('发送中')
            send_thread = threading.Thread(target=self.send_file, args=(client_socket, filepath,sender,sendtime,))
            send_thread.run()
    #广播语音消息
    def broadcast_audio(self,filepath,sender,sendtime):
        for client_socket in self.server.clients_names:
            if client_socket != self.client_socket:
                print('发送语音中')
                send_thread = threading.Thread(target=self.send_file, args=(client_socket, filepath,sender,sendtime,))
                send_thread.run()
    #广播有一个用户上传了文件的消息
    def broadcast_filerecack(self,filepath,sender,sendtime):
        msg_info = json.dumps({'type': 'fileack',
                               'content': {'filepath':filepath,'sendername':sender,'sendtime':sendtime}}).encode('utf-8')
        for client_socket in self.server.clients_names:
            #if client_socket != self.client_socket:
            client_socket.send(msg_info)
    #广播一个用户离开了
    def broadcast_someone_leave(self,name):
        msg_info = json.dumps({'type': 'someoneleave',
                               'content': name}).encode('utf-8')
        for client_socket in self.server.clients_names:
            if client_socket != self.client_socket:
                client_socket.send(msg_info)

