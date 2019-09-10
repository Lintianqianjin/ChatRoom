from tkinter import *
import tkinter.messagebox
from Server_files.Process_client_thread import Process_client_thread
from Server_files.Server import Server
from Client_files.Client import Client
from subprocess import *
from threading import *
from time import *
from tkinter.filedialog import *
from PIL import Image,ImageTk
import matplotlib.pyplot as plt
import pyaudio
import wave
from socket import *
import json
#创建服务器，实际上这个窗口没有用到
#原因是直接就用本地IP地址和端口1234绑定服务器进程了
class Create_server():
    def __init__(self):
        # 创建根窗口
        self.root = Tk()
        # 设置窗口标题
        self.root.title("Lin-ChatRoom")
        # 设置窗口大小
        # self.root.geometry("739x495")

        self.intereaction = Frame(self.root)
        self.intereaction.grid()
        self.intereaction['background'] = 'white'

        self.port_label = Label(self.intereaction, text="端口: ", width=5, bg='white')
        self.port_prompt = StringVar()
        # 使用textvariable属性，绑定字符串变量
        self.port_text = Entry(self.intereaction, textvariable=self.port_prompt, width=30)
        self.port_prompt.set('值最好在1024-5000之间')

        self.confirm_bt = Button(self.intereaction, fg='white', bg='#87CEEB', bd=0, text='创建', width=20)
        self.back_bt = Button(self.intereaction, fg='white', bg='#87CEEB', bd=0, text='返回', width=20)
        self.confirm_bt.bind("<Button-1>", self.run_server)
        self.back_bt.bind("<Button-1>",self.go_back_first_step)


        self.port_label.grid(row=0, column=0, padx=2, pady=5)
        self.port_text.grid(row=0, column=1, padx=2, pady=5)
        self.confirm_bt.grid(row=1, column=0, columnspan=2, pady=5)
        self.back_bt.grid(row=2, column=0, columnspan=2, pady=5)

    def show(self):
        self.root.mainloop()

    def go_back_first_step(self,event):
        self.root.destroy()
        first_step = First_step()
        first_step.show()

    def run_server(self,event):
        port = self.port_text.get()
        current_server = Server(int(port))
        current_server.accept_loop()
        self.root.destroy()
        running_window = server_running()
        running_window.show()
#点击main方法，弹出的窗口，选择创建服务器还是加入聊天室
class First_step():
    def __init__(self):
        # 创建根窗口
        self.root = Tk()
        self.root.resizable(0, 0)
        screen_wid = self.root.winfo_screenmmwidth()
        screen_height = self.root.winfo_screenheight()
        x = int(screen_wid / 2 + 400)
        y = int(screen_height / 2 - 200 + 100)
        self.root.geometry('+' + str(x) + '+' + str(y))
        # 设置窗口标题
        #self.root.title("")
        # 设置窗口大小
        # self.root.geometry("300x200")

        self.intereaction = Frame(self.root)
        self.intereaction.grid()
        self.intereaction['background'] = 'white'

        self.create_server_bt = Button(self.intereaction,fg = 'white',bg='#87CEEB',bd=0 ,text = '创建服务器',width = 20)
        self.join_room_bt = Button(self.intereaction, fg='white', bg='#87CEEB', bd=0, text='加入聊天室', width=20)

        self.create_server_bt.grid(row=0, column=0, ipadx = 5,padx=5,pady=5)
        self.join_room_bt.grid(row=1, column=0, ipadx = 5,padx=5,pady=5)

        self.create_server_bt.bind("<Button-1>",self.go_to_create_server)
        self.join_room_bt.bind("<Button-1>", self.go_to_join_room)

    def show(self):
        self.root.mainloop()

    def go_to_create_server(self,event):
        self.root.destroy()
        call('python ./Server_files/Server.py')

    def go_to_join_room(self,event):
        self.root.destroy()
        #选择加入聊天室功能，需要一个客户端对象
        client_socket = Client()
        login = Login(client_socket)
        login.show()
#注册窗口，可以填写注册信息，发送注册请求，
class signup():
    def __init__(self,client_socket):
        self.client_socket = client_socket
        # 创建根窗口
        self.root = Tk()
        # self.go = False
        # 设置窗口标题
        self.root.title("注册")
        # 设置窗口大小
        # self.root.geometry("300x200")
        self.root.resizable(0, 0)
        screen_wid = self.root.winfo_screenmmwidth()
        screen_height = self.root.winfo_screenheight()
        x = int(screen_wid / 2 + 350)
        y = int(screen_height / 2 - 200 + 50)
        self.root.geometry('+' + str(x) + '+' + str(y))

        self.intereaction = Frame(self.root)
        self.intereaction.grid()
        self.intereaction['background'] = 'white'

        self.name_label = Label(self.intereaction, text="姓名: ", width=5, bg='white')
        self.pw_label = Label(self.intereaction, text="密码: ", width=5, bg='white')
        # self._label = Label(self.intereaction, text="端口: ", width=5, bg='white')

        self.name_prompt = StringVar()
        # 使用textvariable属性，绑定字符串变量
        self.name_text = Entry(self.intereaction, textvariable=self.name_prompt, width=30)
        self.name_prompt.set('请输入用户名')

        self.pw_prompt = StringVar()
        # 使用textvariable属性，绑定字符串变量
        self.pw_text = Entry(self.intereaction, textvariable=self.pw_prompt, width=30)
        self.pw_prompt.set('请输入密码')

        self.confirm_bt = Button(self.intereaction, fg='white', bg='#87CEEB', bd=0, text='注册', width=20)
        self.confirm_bt.bind("<Button-1>", self.send_signup)

        self.back_bt = Button(self.intereaction, fg='white', bg='#87CEEB', bd=0, text='返回', width=20)
        self.back_bt.bind("<Button-1>", self.go_to_loginup)

        self.name_label.grid(row=0, column=0, padx=2, pady=5)
        self.pw_label.grid(row=1, column=0, padx=2, pady=5)
        # self.port_label.grid(row=2,column=0,padx = 2,pady=5)

        self.name_text.grid(row=0, column=1, padx=2, pady=5)
        self.pw_text.grid(row=1, column=1, padx=2, pady=5)
        # self.port_text.grid(row =2,column = 1,padx = 2,pady=5)

        self.confirm_bt.grid(row=3, column=0, columnspan=2, pady=5)
        self.back_bt.grid(row=4, column=0, columnspan=2, pady=5)

    def go_to_loginup(self,event):
        self.root.destroy()
        login = Login(self.client_socket)
        login.show()

    def send_signup(self,event):
        name = self.name_text.get()
        pw = self.pw_text.get()
        self.client_socket.signup_request(name, pw)
        print('注册请求已发送')
        receive_thread = Thread(target=self.update)
        receive_thread.start()

    def update(self):
        while True:
            msg = self.client_socket.receive_data()
            if msg is not None:
                if msg['type'] == 'signupreply':
                    print('收到注册回复')
                    if msg['content']['result'] == False:
                        tkinter.messagebox.showinfo('失败', msg['content']['reason'])
                    else:
                        tkinter.messagebox.showinfo('成功', msg['content']['reason'])
                        break

    def show(self):
        self.root.mainloop()
#登录窗口
class Login():
    def __init__(self,client_socket):
        self.client_scoket = client_socket
        try:
            self.client_scoket.connect_server(gethostbyname(gethostname()), 1234)
        #如果是从注册界面返回，则已经连接会连接失败
        except:
            print('已经连接服务器')
        # 创建根窗口
        self.root = Tk()
        self.go = False
        # 设置窗口标题
        self.root.title("Login")
        # 设置窗口大小
        #self.root.geometry("300x200")
        self.root.resizable(0, 0)
        screen_wid = self.root.winfo_screenmmwidth()
        screen_height = self.root.winfo_screenheight()
        x = int(screen_wid / 2 + 350)
        y = int(screen_height / 2 - 200+50)
        self.root.geometry('+' + str(x) + '+' + str(y))

        self.intereaction = Frame(self.root)
        self.intereaction.grid()
        self.intereaction['background'] = 'white'

        self.name_label = Label(self.intereaction,text = "姓名: ",width=5,bg='white')
        self.pw_label = Label(self.intereaction,text="密码: ",width=5,bg='white')
        #self._label = Label(self.intereaction, text="端口: ", width=5, bg='white')

        self.name_prompt = StringVar()
        # 使用textvariable属性，绑定字符串变量
        self.name_text = Entry(self.intereaction, textvariable=self.name_prompt,width=30)
        self.name_prompt.set('请输入用户名')

        self.pw_prompt = StringVar()
        # 使用textvariable属性，绑定字符串变量
        self.pw_text = Entry(self.intereaction, textvariable=self.pw_prompt,width=30)
        self.pw_prompt.set('请输入密码')

        #self.port_prompt = StringVar()
        # 使用textvariable属性，绑定字符串变量
        #self.port_text = Entry(self.intereaction, textvariable=self.port_prompt, width=30)
        #self.port_prompt.set('请输入你要连接的服务器端口')

        self.confirm_bt = Button(self.intereaction, fg='white', bg='#87CEEB', bd=0, text='登陆', width=20)
        self.confirm_bt.bind("<Button-1>", self.go_to_chat_box)
        #self.intereaction.bind("<Return>", self.go_to_chat_box)

        self.back_bt = Button(self.intereaction, fg='white', bg='#87CEEB', bd=0, text='注册', width=20)
        self.back_bt.bind("<Button-1>", lambda x : self.go_to_signup(x,self.client_scoket))

        self.name_label.grid(row=0,column=0,padx = 2,pady=5)
        self.pw_label.grid(row=1,column=0,padx = 2,pady=5)
        #self.port_label.grid(row=2,column=0,padx = 2,pady=5)

        self.name_text.grid(row=0,column=1,padx = 2,pady=5)
        self.pw_text.grid(row =1,column = 1,padx = 2,pady=5)
        #self.port_text.grid(row =2,column = 1,padx = 2,pady=5)

        self.confirm_bt.grid(row = 3 , column = 0 ,columnspan = 2 ,pady = 5)
        self.back_bt.grid(row=4, column=0, columnspan=2, pady=5)

    def go_to_signup(self,event,client_socket):
        self.root.destroy()
        sign_up = signup(client_socket)
        sign_up.show()

    def go_to_chat_box(self,event):
        name = self.name_text.get()
        pw = self.pw_text.get()
        self.client_scoket.login_request(name,pw)
        print('登录请求已发送')
        while True:
            msg = self.client_scoket.receive_data()
            if msg is not None:
                if msg['type'] == 'loginreply':
                    if msg['content']['result'] == False:
                        tkinter.messagebox.showinfo('失败', msg['content']['reason'])
                        break
                    else:
                        self.open_chatroom()
                        break

    def open_chatroom(self):
        name = self.name_text.get()
        self.root.destroy()
        print(name)
        chat_room = Main_chat_box(name, gethostbyname(gethostname()), 1234, self.client_scoket)
        receive_thread = Thread(target=chat_room.update)
        receive_thread.start()
        chat_room.show()

    def show(self):
        self.root.mainloop()
#主聊天窗口，是整个客户端界面的核心部分
#客户端接收消息并作出反应在这里进行
class Main_chat_box():

    def __init__(self,name,host,port,current_client):
        self.current_client = current_client
        self.current_client.set_name(name)
        #self.current_client.connect_server(host,port)
        name_info = json.dumps({'type': 'nameinfo',
                               'content': name}).encode('utf-8')
        self.current_client.client_socket.send(name_info)

        #创建根窗口
        self.root = Tk()
        #设置窗口标题
        self.root.title("Lin-ChatRoom")
        #设置窗口大小
        screen_wid = self.root.winfo_screenmmwidth()
        screen_height = self.root.winfo_screenheight()
        x = int(screen_wid/2+150)
        y = int(screen_height/2-200)
        self.root.geometry('+'+str(x)+'+'+str(y))
        self.root.resizable(0,0)
        #self.root.geometry("739x495")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.intereaction = Frame(self.root)
        self.intereaction.grid()
        self.intereaction['background'] = 'white'

        self.canvas = Canvas(self.intereaction,bg = 'white')  # 创建canvas
        self.msg_scroll = Scrollbar(self.intereaction,bd = 0,orient='vertical',command=self.canvas.yview,width= 20)
        #self.msg_scroll.set(1)
        self.canvas['yscrollcommand']=self.msg_scroll.set
        #self.canvas.create_text((10,0),anchor = 'nw' ,text='lin')
        #self.img = PhotoImage(file = '../emoji/笑哭.png')
        #self.canvas.create_image((10,20),anchor = 'nw',image = self.img)

        #self.canvas.create_text((10, 55), anchor='nw', text='lin 14:37:59')
        #self.canvas.create_image((10, 75), anchor='nw', image=self.img)

        self.canvas.grid(row = 0, column = 2 ,columnspan = 5,stick = S+W+N+E)
        #self.msg_list = Listbox(self.canvas,yscrollcommand=self.msg_scroll)
        #self.msg_list.configure(height=20, width=80,bd = 0)
        self.msg_list_length = 0
        #self.msg_scroll.config(command=self.msg_list.yview)
        #msg_scroll.configure(height=400, width=10)
        #self.msg_list.grid(row=0,column=2)
        self.msg_scroll.grid(row=0,column=6,sticky = N+E+S)


        self.text_field = Text(self.intereaction)
        self.text_field.configure(height=8, width=75,bd = 0)
        self.text_field.bind('<Return>',self.send_msg)


        self.send_bt = Button(self.intereaction)
        self.send_bt.configure(fg = 'white',bg='#87CEEB',bd=0 ,text = '发送',width = 5)
        self.send_bt.bind('<Button-1>',self.send_msg)

        self.text_field.grid(row = 1,column = 2,columnspan = 5 , sticky = N+W+E)
        self.send_bt.grid(row = 2 ,column = 5 ,columnspan = 2,sticky =E)

        self.imgbiaoqingbo = PhotoImage(file='./Gui/resources/表情包.png')
        self.biaoqingbao_label = Label(self.intereaction, image=self.imgbiaoqingbo, bd=0)
        self.biaoqingbao_label.grid(row=2, column=2, sticky=W)
        self.biaoqingbao_label.bind('<Button-1>',self.show_biaoqingbao_window)

        self.imgyuyin = PhotoImage(file='./Gui/resources/语音.png')
        self.yuyin_label = Label(self.intereaction, image=self.imgyuyin, bd=0)

        self.yuyin_label.grid(row=2, column=3, padx = 30)
        self.yuyin_label.bind('<Button-1>', self.show_audio_window)

        self.imgtupian = PhotoImage(file='./Gui/resources/图片.png')
        self.tupian_label = Label(self.intereaction, image=self.imgtupian, bd=0)
        self.tupian_label.grid(row=2, column=4)
        self.tupian_label.bind('<Button-1>', lambda x: self.show_file_select(x,'send'))

        self.imgwenjian = PhotoImage(file='./Gui/resources/文件.png')
        self.wenjian_label = Label(self.intereaction, image=self.imgwenjian, bd=0)
        self.wenjian_label.grid(row=2, column=5)
        self.wenjian_label.bind('<Button-1>', lambda x: self.show_file_select(x,'send'))


        self.user_scroll = Scrollbar(self.intereaction,bd = 0)
        self.user_list = Listbox(self.intereaction,yscrollcommand=self.user_scroll.set,bd = 0)
        self.user_list_length = 0
        self.user_scroll.config(command=self.user_list.yview)
        self.user_count = StringVar()
        # 使用textvariable属性，绑定字符串变量
        self.user_count.set('当前用户' + str(self.user_list_length) + '人')
        self.user_count_label = Label(self.intereaction, textvariable=self.user_count, width=30,fg = '#7B68EE')
        self.user_count_label.grid(row=2, column=0, sticky=S + E + W)


        self.user_scroll.grid(row=0,column=1,rowspan = 3,sticky = N+W+E+S)

        #user_list.configure(height=26, width=20)
        self.user_list.grid(row=0,column=0,rowspan = 2,sticky = N+W+E+S)

        self.user_list.insert(END, self.current_client.name)
        self.user_list_length += 1
        self.update_users_count_label()
        self.user_list.itemconfigure(self.user_list_length - 1, {'fg': '#4169E1'})

    def show_biaoqingbao_window(self,event):
        biaoqingbao = Emoji(self.current_client)
        biaoqingbao.show()

    def show_file_select(self,event,type):
        selectfile = select_file(self.current_client,type)
        selectfile.show()

    def show_audio_window(self,event):
        audio = send_audio_window(self.current_client,self)
        audio.show()

    def delete_enter_n(self):
        sleep(0.01)
        self.text_field.delete('0.0', 'end')

    def send_msg(self,event):
        msg = self.text_field.get('0.0','end')
        #因为是自己的消息，所以将它展现在对话框的右边，而与别人的消息区分开来
        speaker = Label(self.intereaction,text =self.current_client.name + '  (' + strftime("%m-%d %a %H:%M:%S",localtime()) + ')',fg='#1E90FF',bg='white')
        content = Label(self.intereaction,text =msg, fg='#A9A9A9',bg='white')
        self.canvas.create_window((500, self.msg_list_length), window = speaker, anchor='ne')
        self.canvas.create_window((500, self.msg_list_length + 20), window=content, anchor='ne')
        factor = len(msg.split('\n'))
        self.msg_list_length += 50 + (factor - 2) * 20
        self.canvas["scrollregion"] = "%d %d %d %d" % (0, 0, 600, self.msg_list_length+20 )
        self.canvas.yview_moveto(1)

        #self.text_field.mark_set('insert','0.0')
        if event.keycode == 13:
            delete_huanhang = Thread(target=self.delete_enter_n)
            delete_huanhang.start()
        #if msg == '\n':
        #    tkinter.messagebox.showerror('警告', '发送内容不得为空')
        #else:
        self.current_client.send_msg(msg)

    def update_users_count_label(self):
        self.user_count.set('当前用户' + str(self.user_list_length) + '人')
        self.user_count_label.configure(textvariable=self.user_count)

    def update(self):
        while True:
            self.root.update()
            msg_need_show = self.current_client.receive_data()
            if msg_need_show is not None:
                if msg_need_show['type'] == 'msg':
                    text_msg = msg_need_show['content']
                    partions  = text_msg.split(',')
                    if partions[0] == 'NamesInRoom':
                        for name in partions:
                            if name == 'NamesInRoom':
                                continue
                            else:
                                self.user_list.insert(END,name)
                                self.user_list_length += 1
                                self.update_users_count_label()
                                self.user_list.itemconfigure(self.user_list_length - 1, {'fg': '#4169E1'})
                    else:
                        speaker = Label(self.intereaction,text =partions[0] + '  ('+ partions[1]+')',fg='#1E90FF',bg = 'white')
                        content = Label(self.intereaction,text =partions[2], fg='#A9A9A9',bg = 'white')
                        self.canvas.create_window((10, self.msg_list_length), window=speaker, anchor='nw')
                        self.canvas.create_window((10, self.msg_list_length + 20), window=content, anchor='nw')
                        factor = len(partions[2].split('\n'))
                        self.msg_list_length += 50+(factor-2)*20
                        self.canvas["scrollregion"] = "%d %d %d %d" % (0, 0, 600, self.msg_list_length +20)
                        self.canvas.yview_moveto(1)
                elif msg_need_show['type'] == 'file':
                    if msg_need_show['fileextension'] in ['.bmp', '.jpg', '.png', '.jpeg']:
                        self.current_client.receive_file(filename=msg_need_show['filename'], fileextension=msg_need_show['fileextension'],filesize=msg_need_show['filesize'])
                        filename = msg_need_show['filename']
                        fileextension = msg_need_show['fileextension']
                        speaker = Label(self.intereaction, text=msg_need_show['sendername'] + '  (' + msg_need_show['sendertime'] + ')', fg='#1E90FF', bg='white')
                        while True:
                            if os.path.isfile('./Client_files/buffer_files/'+filename+fileextension):
                                img = Image.open('./Client_files/buffer_files/'+filename+fileextension)
                                ratio = min(100 / img.size[0], 100 / img.size[1])
                                wid, hei = int(img.size[0] * ratio), int(img.size[1] * ratio)
                                resizedimg = img.resize((wid, hei))
                                # tkinter的PhotoImage只能识别gif、PGM、PPM格式的图片，而对于jpg、png等图片不能识别。
                                photo = ImageTk.PhotoImage(resizedimg)
                                photolabel = Label(self.canvas,image=photo)
                                if msg_need_show['sendername'] == self.current_client.name:
                                    self.canvas.create_window((500, self.msg_list_length), window=speaker, anchor='ne')
                                    #self.canvas.create_image((500, self.msg_list_length + 20), image=photo,anchor='ne')
                                    self.canvas.create_window((500, self.msg_list_length + 20), window=photolabel, anchor='ne')
                                    #self.msg_list_length += 50+hei-10
                                else:
                                    self.canvas.create_window((10, self.msg_list_length), window=speaker, anchor='nw')
                                    #self.canvas.create_image((10, self.msg_list_length + 20), image=photo, anchor='nw')
                                    self.canvas.create_window((10, self.msg_list_length + 20), window=photolabel, anchor='nw')
                                self.msg_list_length += 50 + hei - 10
                                self.canvas["scrollregion"] = "%d %d %d %d" % (0, 0, 600, self.msg_list_length +20)
                                self.canvas.yview_moveto(1)
                                break
                            else:
                                continue
                    elif msg_need_show['fileextension'] == '.wav':
                        self.current_client.receive_file(filename=msg_need_show['filename'],
                                                         fileextension=msg_need_show['fileextension'],
                                                         filesize=msg_need_show['filesize'])
                        print('收到录音文件')
                        filename = msg_need_show['filename']
                        fileextension = msg_need_show['fileextension']
                        speaker = Label(self.intereaction,
                                        text=msg_need_show['sendername'] + '  (' + msg_need_show['sendertime'] + ')',
                                        fg='#1E90FF', bg='white')
                        #whlie True并判断的原因是担心用户点击时，语音文件还未完整地接收并写入到本地磁盘中
                        while True:
                            if os.path.isfile('./Client_files/buffer_files/' + filename + fileextension):
                                button_yuyin = Button(self.canvas, text='点击收听语音',bd=0,bg='#7B68EE',fg = 'white')
                                self.canvas.create_window((10, self.msg_list_length), window=speaker, anchor='nw')
                                self.canvas.create_window((10, self.msg_list_length + 20), window=button_yuyin,
                                                              anchor='nw')

                                button_yuyin.bind('<Button-1>',lambda x: self.play_audio(x, 'Client_files/buffer_files/new_wav.wav'))
                                #更新消息框的画布大小即可以滚动的范围
                                self.msg_list_length += 50
                                self.canvas["scrollregion"] = "%d %d %d %d" % (0, 0, 600, self.msg_list_length+20)
                                self.canvas.yview_moveto(1)
                                break
                            else:
                                continue
                    else:
                        print('非图片及语音')
                        print(msg_need_show['filename']+msg_need_show['fileextension'])
                        #filepath = os.path.join(self.current_client.save_path+, msg_need_show['filename']+msg_need_show['fileextension'])
                        #print(filepath)
                        self.current_client.receive_file_in_diypath(self,filename=msg_need_show['filename'],
                                                         fileextension=msg_need_show['fileextension'],
                                                         filesize=msg_need_show['filesize'],filepath=self.current_client.save_path)
                elif msg_need_show['type'] == 'biaoqingbao':
                    biaoqingbaoname = msg_need_show['content']
                    partions = biaoqingbaoname.split(',')
                    speaker = Label(self.intereaction, text=partions[0] + '  (' + partions[1] + ')', fg='#1E90FF',
                                    bg='white')
                    biaoqingbaoname=partions[2]
                    img = Image.open('./emoji/' + biaoqingbaoname)
                    photo = ImageTk.PhotoImage(img)
                    photolabel = Label(self.canvas, image=photo,bg = 'white')
                    if partions[0] == self.current_client.name:
                        self.canvas.create_window((500, self.msg_list_length), window=speaker, anchor='ne')
                        self.canvas.create_window((500, self.msg_list_length + 20), window=photolabel, anchor='ne')
                    else:
                        self.canvas.create_window((10, self.msg_list_length), window=speaker, anchor='nw')
                        self.canvas.create_window((10, self.msg_list_length + 20), window=photolabel, anchor='nw')
                    self.msg_list_length += 50
                    self.canvas["scrollregion"] = "%d %d %d %d" % (0, 0, 600, self.msg_list_length +20)
                    self.canvas.yview_moveto(1)
                elif msg_need_show['type'] == 'fileack':
                    sendername = msg_need_show['content']['sendername']
                    send_time = msg_need_show['content']['sendtime']
                    speaker = Label(self.intereaction, text=sendername + '  (' + send_time + ')', fg='#1E90FF',bg='white')

                    (path, file) = os.path.split(msg_need_show['content']['filepath'])
                    (filename, extension) = os.path.splitext(file)

                    if sendername == self.current_client.name:
                        recv_file_button1 = Button(self.canvas, text=filename + extension + '已发送，点击可重新下载', bd=0, bg='#4169E1',
                                                  fg='white')
                        self.canvas.create_window((500, self.msg_list_length), window=speaker, anchor='ne')
                        self.canvas.create_window((500, self.msg_list_length + 25), window=recv_file_button1, anchor='ne')
                        recv_file_button1.bind('<Button-1>',
                                              lambda x: self.send_download_ack(x, msg_need_show['content']['filepath']))
                    else:
                        recv_file_button2 = Button(self.canvas, text=filename + extension + ',点击接收', bd=0, bg='#4169E1',
                                                  fg='white')
                        self.canvas.create_window((10, self.msg_list_length), window=speaker, anchor='nw')
                        self.canvas.create_window((10, self.msg_list_length + 25), window=recv_file_button2, anchor='nw')
                        recv_file_button2.bind('<Button-1>',lambda x: self.send_download_ack(x, msg_need_show['content']['filepath']))
                    self.msg_list_length += 55
                    self.canvas["scrollregion"] = "%d %d %d %d" % (0, 0, 600, self.msg_list_length+20)
                    self.canvas.yview_moveto(1)
                elif msg_need_show['type'] == 'someoneleave':
                    leavename = msg_need_show['content']
                    for i in range(self.user_list_length):
                        if self.user_list.get(i) == leavename:
                            self.user_list.delete(i)
                            self.user_list_length -= 1
                            self.update_users_count_label()
                elif msg_need_show['type'] == 'close':
                    break
        self.current_client.client_socket.shutdown(SHUT_RDWR)
        self.current_client.client_socket.close()

    def send_download_ack(self,event,serverfilepath):
        selectfile = select_file(self.current_client, 'save',serverfilepath)
        selectfile.show().run()

    def play_audio(self,event,filename):
        CHUNK = 1024
        # 只读方式打开wav文件

        f = wave.open(filename, "rb")

        p = pyaudio.PyAudio()

        # 打开数据流
        stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                        channels=f.getnchannels(),
                        rate=f.getframerate(),
                        output=True)

        # 读取数据
        data = f.readframes(CHUNK)

        # 播放
        while data != b"":
            stream.write(data)
            data = f.readframes(CHUNK)
            print('循环中')
            print(data)

        # 停止数据流
        stream.stop_stream()
        stream.close()
        f.close()

        # 关闭 PyAudio
        p.terminate()
        print('结束')

    def on_closing(self):
        if tkinter.messagebox.askokcancel("退出", "确定退出吗？"):
            self.current_client.close_connect()
            self.root.destroy()


    def show(self):
        self.root.mainloop()
#表情包发送窗口
class Emoji:
    def __init__(self,client_socket):

        self.client_socket = client_socket
        self.root = Toplevel()
        # 设置窗口标题
        self.root.title("Lin-ChatRoom")
        # 设置窗口大小
        screen_wid = self.root.winfo_screenmmwidth()
        screen_height = self.root.winfo_screenheight()
        x = int(screen_wid / 2 +390)
        y = int(screen_height / 2 +175)
        self.root.geometry('+'+str(x)+'+'+str(y))
        self.root.overrideredirect(True)

        self.intereaction = Frame(self.root)
        self.intereaction.grid()
        self.intereaction['background'] = 'white'

        self.img1 = PhotoImage(file='./emoji/笑哭.png')
        self.img2 = PhotoImage(file='./emoji/委屈.png')
        self.img3 = PhotoImage(file='./emoji/生气.png')
        self.img4 = PhotoImage(file='./emoji/坏笑.png')
        self.img5 = PhotoImage(file='./emoji/尴尬.png')
        self.img6 = PhotoImage(file='./emoji/开心.png')

        self.Button_xiaocry = Button(self.intereaction, image=self.img1,bg = 'white',bd=0)
        self.Button_weiqu = Button(self.intereaction, image=self.img2,bg = 'white',bd=0)
        self.Button_shengqi = Button(self.intereaction, image=self.img3,bg = 'white',bd=0)
        self.Button_huaixiao = Button(self.intereaction, image=self.img4,bg = 'white',bd=0)
        self.Button_ganga = Button(self.intereaction, image=self.img5,bg = 'white',bd=0)
        self.Button_kaixin = Button(self.intereaction, image=self.img6,bg = 'white',bd=0)

        self.Button_xiaocry.grid(row = 0,column = 1)
        self.Button_weiqu.grid(row=0, column=2)
        self.Button_shengqi.grid(row=0, column=3)
        self.Button_huaixiao.grid(row=0, column=4)
        self.Button_ganga.grid(row=0, column=5)
        self.Button_kaixin.grid(row=0, column=6)

        self.Button_xiaocry.bind('<Button-1>',self.send_xiaocry)
        self.Button_weiqu.bind('<Button-1>', self.send_weiqu)
        self.Button_shengqi.bind('<Button-1>', self.send_shengqi)
        self.Button_huaixiao.bind('<Button-1>', self.send_huaixiao)
        self.Button_ganga.bind('<Button-1>',self.send_ganga)
        self.Button_kaixin.bind('<Button-1>', self.send_kaixin)

    def send_xiaocry(self,event):
        #filepath = ('./emoji/笑哭.png')
        self.root.destroy()
        self.client_socket.send_biaoqingbao('笑哭.png')

    def send_weiqu(self,event):
        #filepath = ('./emoji/')
        self.root.destroy()
        self.client_socket.send_biaoqingbao('委屈.png')

    def send_shengqi(self,event):
        #filepath = ('./emoji/)
        self.root.destroy()
        self.client_socket.send_biaoqingbao('生气.png')

    def send_huaixiao(self,event):
        #filepath = ('./emoji/')
        self.root.destroy()
        self.client_socket.send_biaoqingbao('坏笑.png')

    def send_ganga(self,event):
        #filepath = ('./emoji/')
        self.root.destroy()
        self.client_socket.send_biaoqingbao('尴尬.png')

    def send_kaixin(self,event):
        #filepath = ('./emoji/')
        self.root.destroy()
        self.client_socket.send_biaoqingbao('开心.png')

    def show(self):
        self.root.mainloop()
#选择文件（存储路径和发送文件）的窗口
class select_file:
    def __init__(self,client_socket,type,*serverfilepath):
        self.client_socket = client_socket
        if serverfilepath:
            self.serverfilepath = serverfilepath[0]
        #self.needupdatechatbox = updatechatbox
        self.root = Toplevel()
        self.type = type
        screen_wid = self.root.winfo_screenmmwidth()
        screen_height = self.root.winfo_screenheight()
        x = int(screen_wid / 2 + 750)
        y = int(screen_height / 2 + 125)
        self.root.geometry('+' + str(x) + '+' + str(y))

        self.root.grid()
        self.root.resizable(0, 0)
        self.path = StringVar()
        self.Label=Label(self.root, text="目标路径:",fg = '#7B68EE')
        self.Label.grid(row=0, column=0)
        self.Entry=Entry(self.root, textvariable=self.path,width=20)
        self.Entry.grid(row=0, column=1)
        self.Button=Button(self.root, text="路径选择",fg = 'white',bg='#87CEEB',bd=0 , command=self.selectPath)
        self.Button.grid(row=0, column=2)
        self.Button_confirm = Button(self.root, text="确认",fg = 'white',bg='#87CEEB',bd=0 ,width = 20)
        self.Button_confirm.grid(row=1,columnspan = 3)
        self.Button_confirm.bind('<Button-1>',self.confirm)

    def selectPath(self):
        if self.type == 'send':
            path_ = askopenfilename()
            self.path.set(path_)
        elif self.type=='save':
            path_ = askdirectory()
            self.path.set(path_)

    def confirm(self,event):
        filepath = self.Entry.get()
        #print(filepath)
        self.root.destroy()
        if self.type == 'send':
            self.client_socket.send_file(filepath)
        elif self.type == 'save':
            self.client_socket.save_path = filepath
            print(filepath)
            print('可以发送确认了')
            self.client_socket.download_file_ack(self.serverfilepath)

    def show(self):
        self.root.mainloop()
#打开录制并发送语音的窗口
class send_audio_window(Toplevel):
    def __init__(self,client_socket,chat_gui):
        super().__init__()
        self.chat_gui = chat_gui
        self.client_socket = client_socket
        screen_wid = self.winfo_screenmmwidth()
        screen_height = self.winfo_screenheight()
        x = int(screen_wid / 2 + 600)
        y = int(screen_height / 2 + 175)
        self.geometry('+' + str(x) + '+' + str(y))
        self.grid()
        self.overrideredirect(True)

        self.send_flag = True

        self.button_rec = Button(self,text = '开始录音',bg = '#00BFFF',bd = 0,fg = 'white')
        self.button_rec.grid(row =0,column  = 0)
        self.button_rec.bind('<Button-1>',self.start_rec_and_send)

        self.button_end = Button(self, text='结束录音', bg='#00BFFF', bd=0, fg='white')
        self.button_end.bind('<Button-1>',self.end_rec)

    def end_rec(self,event):
        #点击结束后，改变记录音频字节流的判断条件
        # 使得循环记录停止，并形成wav文件
        self.send_flag = False
        self.destroy()

    def start_rec_and_send(self,evnet):
        #将开始录音的按钮改为停止录音的按钮
        self.button_rec.grid_forget()
        self.button_end.grid(row =0,column  = 0)
        #启动录音的线程
        thread = Thread(target=self.rec_audio)
        thread.start()
        #thread.join()

    def rec_audio(self):
        print('开始录音')
        #一次读取的字节长度
        CHUNK = 1024
        #采样值的量化格式，值可以为paFloat32、paInt32、paInt24、paInt16、paInt8等。
        FORMAT = pyaudio.paInt16
        #声道数
        CHANNELS = 2
        #采样率
        RATE = 16000

        #使用pyaudio录音
        p = pyaudio.PyAudio()
        #传入定义好的参数，打开录音
        #input:输入流标志，Ture表示开始输入流
        stream = p.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,frames_per_buffer=CHUNK)
        frames = []

        while self.send_flag:
            data = stream.read(CHUNK)
            print(data)
            frames.append(data)

        button_yuyin = Button(self.chat_gui.canvas, text='点击收听语音', bd=0, bg='#7B68EE', fg='white')
        time = strftime("%m-%d %a %H:%M:%S", localtime())
        speaker = Label(self.chat_gui.intereaction, text=self.client_socket.name + ' (' + time + ')', bg='white',
                        fg='#1E90FF')
        self.chat_gui.canvas.create_window((500, self.chat_gui.msg_list_length), window=speaker, anchor='ne')
        # self.canvas.create_image((10, self.msg_list_length + 20), image=photo, anchor='nw')11
        self.chat_gui.canvas.create_window((500, self.chat_gui.msg_list_length + 20), window=button_yuyin, anchor='ne')
        self.chat_gui.msg_list_length += 50
        self.chat_gui.canvas["scrollregion"] = "%d %d %d %d" % (0, 0, 600, self.chat_gui.msg_list_length+20)
        self.chat_gui.canvas.yview_moveto(1)
        button_yuyin.bind('<Button-1>',lambda x : self.play_audio(x,'Client_files/buffer_files/new_wav.wav'))

        stream.stop_stream()
        stream.close()
        p.terminate()

        # open返回一个的是一个Wave_read类的实例，通过调用它的方法读取WAV文件的格式和数据：
        wf = wave.open('Client_files/buffer_files/new_wav.wav', 'wb')
        #设置声道数
        wf.setnchannels(CHANNELS)
        #采样精度
        wf.setsampwidth(p.get_sample_size(FORMAT))
        #采样率
        wf.setframerate(RATE)
        #写入操作
        wf.writeframes(b''.join(frames))
        wf.close()
        #向服务器发送该语音
        self.client_socket.send_file('Client_files/buffer_files/new_wav.wav')

    def play_audio(self,event,filename):
        # 只读方式打开wav文件
        CHUNK = 1024
        f = wave.open(filename, "rb")

        p = pyaudio.PyAudio()

        # 打开数据流
        stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                        channels=f.getnchannels(),
                        rate=f.getframerate(),
                        output=True)

        # 读取数据
        data = f.readframes(CHUNK)

        # 播放
        while data != b"":
            stream.write(data)
            data = f.readframes(CHUNK)
            print('循环中')
            print(data)

        # 停止数据流
        stream.stop_stream()
        stream.close()
        f.close()

        # 关闭 PyAudio
        p.terminate()
        print('结束')

    def show(self):
        self.mainloop()