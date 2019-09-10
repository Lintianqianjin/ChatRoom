# ChatRoom
a chatting room based on python

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
![](https://github.com/Lintianqianjin/ChatRoom/blob/master/MD_imgs/accept_loop.png)  
