from Server_files.Process_client_thread import *

class Server:
    #初始化基本的一些变量
    def __init__(self,port):
        # 创建一个字典用于存放每一个用户的socket对应的用户名
        # 方便之后服务器广播，以及设置传输的信息的姓名字段
        self.clients_names = {}
        #存储用户的姓名和密码
        self.clients_name_pw = {}
        #将本地用户账户密码读入缓存，存储到self.clients_name_pw字典中
        # 不使用数据库的原因是，如果我的这个程序给别人用，别人还要自己配置数据库
        #但是使用本地文件就没有这个问题，另外这样也可以减少与数据库通讯的开销
        users = open('./Server_files/buffer_files/init/users.txt','r+',encoding='utf-8')
        for line in users:
            parts = line.strip().split('\t')
            self.clients_name_pw[parts[0]] = parts[1]
        users.close()

        self.BUFFER_SIZE = 1024
        # 创建一个socket对象
        #   1.参数AF_INET不仅可以用作本机的跨进程通信，同样的可以用于不同机器之间的通信。
        # 而AF_UNIX参数是数据到达内核缓冲区后，由内核根据指定路径名找到接收方socket对应的内核缓冲区
        # 直接将数据拷贝过去，不经过协议层编解码，节省系统cpu，并且不经过网卡，所以只能用于本机内进程之间的通信。
        # 所以这里使用AF_INET
        #   2.参数SOCK_STREAM提供面向连接的稳定数据传输，即TCP协议。SOCK_DGRAM是基于UDP的。所以这里选择SOCK_STREAM。
        self.serversocket = socket(AF_INET, SOCK_STREAM)

        #1. 调用bind之后，内核就会将这个socket的绑定到设定的套接字上，套接字的端口的选择与常用端口错开，在本机唯一就行。
        #2.使用gethostname()，以便对外可见，并且限制为只接受那些目的地址为此主机地址的客户连接
        # 如果'localhost'或'127.0.0.1'，则只在同一台机器中可见。
        # 若'',则接受主机碰巧拥有的目的地址任意的访问。
        #gethostbyname(gethostname())
        self.serversocket.bind((gethostbyname(gethostname()), port))

        # listen函数使主动连接套接口变为被连接套接口，使得一个进程可以接受其它进程的请求，从而成为一个服务器进程。
        #即进入了三次握手中服务器端的LISTEN状态
        #参数5的意义是该socket可以连接的请求的最大个数
        self.serversocket.listen(5)
        print('server is running')

    #循环获取连接请求的socket对象
    def accept_loop(self):
        while True:
            # accept() 被动接受TCP客户端连接,(阻塞式)等待连接的到来，
            # 返回值为两个，前者是一个socket对象，后者是对应地址
            (client_socket, address) = self.serversocket.accept()
            # 因为socket的recv、send等方法是会阻塞的，所以使用多线程的方式处理
            #否则不收到当前客户端的信息，则无法进入下一次循环
            current_client = Process_client_thread(client_socket, self,self.BUFFER_SIZE)
            current_client.start()

if __name__ == '__main__':
    server = Server(1234)
    server.accept_loop()