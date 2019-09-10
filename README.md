# ChatRoom
GUI based on tkinter.  
This assignment is a hasty rush, so it is for reference only. There are many areas where code needs to be improved, such as soundness, security, and modularity.  

---  

## a scenario 
![scenario 1](https://github.com/Lintianqianjin/ChatRoom/blob/master/MD_imgs/scene1.png)  
![scenario 2](https://github.com/Lintianqianjin/ChatRoom/blob/master/MD_imgs/scene2.png)  
![scenario 3](https://github.com/Lintianqianjin/ChatRoom/blob/master/MD_imgs/scene3.png)  
![scenario 4](https://github.com/Lintianqianjin/ChatRoom/blob/master/MD_imgs/scene4.png)  

## server body
The core logic is to create a socket object, then bind the server process to a specific port, and then set the number of listeners. The server enters the LISTEN state, begins to cyclically receive the TCP connection initiated by the client, and processes each connection in a multi-threaded manner.  
### init
![server object initialization](https://github.com/Lintianqianjin/ChatRoom/blob/master/MD_imgs/serverMain.png)  
### accept loop
![LISTEN](https://github.com/Lintianqianjin/ChatRoom/blob/master/MD_imgs/accept_loop.png)  
### each thread that processes a client
![process thread](https://github.com/Lintianqianjin/ChatRoom/blob/master/MD_imgs/process_client_thread.png)  

### client is very similiar to thread that processes a client

## some gui  
### sign up  
![sign up 1](https://github.com/Lintianqianjin/ChatRoom/blob/master/MD_imgs/signUp1.png)  
![sign up 2](https://github.com/Lintianqianjin/ChatRoom/blob/master/MD_imgs/signUp2.png)  
### log in  
![log in 1](https://github.com/Lintianqianjin/ChatRoom/blob/master/MD_imgs/logIn1.png)  
![log in 2](https://github.com/Lintianqianjin/ChatRoom/blob/master/MD_imgs/logIn2.png)  
### send and save files
![send file 1](https://github.com/Lintianqianjin/ChatRoom/blob/master/MD_imgs/sendFile.png)  
![send file 2](https://github.com/Lintianqianjin/ChatRoom/blob/master/MD_imgs/sendFile2.png)  
![save file 1](https://github.com/Lintianqianjin/ChatRoom/blob/master/MD_imgs/saveFile1.png)  
![save file 2](https://github.com/Lintianqianjin/ChatRoom/blob/master/MD_imgs/saveFile2.png)  
### send and listening audio  
![audio 1](https://github.com/Lintianqianjin/ChatRoom/blob/master/MD_imgs/audio1.png)  
![audio 2](https://github.com/Lintianqianjin/ChatRoom/blob/master/MD_imgs/audio2.png)  
![audio 3](https://github.com/Lintianqianjin/ChatRoom/blob/master/MD_imgs/audio3.png)  
