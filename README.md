# ChatRoom
a chatting room based on python  
GUI based on tkinter  
This assignment is a hasty rush, so it is for reference only. There are many areas where code needs to be improved, such as soundness, security, and modularity.  

---  

## a scenario 
![](https://github.com/Lintianqianjin/ChatRoom/blob/master/MD_imgs/scene1.png)  
![](https://github.com/Lintianqianjin/ChatRoom/blob/master/MD_imgs/scene2.png)  
![](https://github.com/Lintianqianjin/ChatRoom/blob/master/MD_imgs/scene3.png)  
![](https://github.com/Lintianqianjin/ChatRoom/blob/master/MD_imgs/scene4.png)  

## server body
核心逻辑是创建一个socket对象，然后将进程绑定到特定的端口上，之后设置监听数量，进入LISTEN状态，开始循环接收客户端发起的TCP连接，并用多线程的方式处理每一个连接。  
### init
![](https://github.com/Lintianqianjin/ChatRoom/blob/master/MD_imgs/serverMain.png)  
### accept loop
![](https://github.com/Lintianqianjin/ChatRoom/blob/master/MD_imgs/accept_loop.png)  
### each thread that processes a client
![](https://github.com/Lintianqianjin/ChatRoom/blob/master/MD_imgs/process_client_thread.png)  

### client is very similiar to thread that processes a client

## some gui  
### sign up  
![](https://github.com/Lintianqianjin/ChatRoom/blob/master/MD_imgs/signUp1.png)  
![](https://github.com/Lintianqianjin/ChatRoom/blob/master/MD_imgs/signUp2.png)  
### log in  
![](https://github.com/Lintianqianjin/ChatRoom/blob/master/MD_imgs/logIn1.png)  
![](https://github.com/Lintianqianjin/ChatRoom/blob/master/MD_imgs/logIn2.png)  
### send and save files
![](https://github.com/Lintianqianjin/ChatRoom/blob/master/MD_imgs/sendFile.png)  
![](https://github.com/Lintianqianjin/ChatRoom/blob/master/MD_imgs/sendFile2.png)  
![](https://github.com/Lintianqianjin/ChatRoom/blob/master/MD_imgs/saveFile1.png)  
![](https://github.com/Lintianqianjin/ChatRoom/blob/master/MD_imgs/saveFile2.png)  
### send and listening audio  
![](https://github.com/Lintianqianjin/ChatRoom/blob/master/MD_imgs/audio1.png)  
![](https://github.com/Lintianqianjin/ChatRoom/blob/master/MD_imgs/audio2.png)  
![](https://github.com/Lintianqianjin/ChatRoom/blob/master/MD_imgs/audio3.png)  
