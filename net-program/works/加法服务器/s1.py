# collect the integers sent by multiple clients at the same time,
# and return the sum of these integers to each client.
import socket

HOST = '127.0.0.1'
PORT = 11111
BUFLEN = 512
listenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listenSocket.bind((HOST, PORT))
# Support three client connections at the same time
listenSocket.listen(3)
print("我是服务器！！！！")
print(f'服务启动成功，在{PORT}端口等待连接...')

sum = 0
while True:
    dataSocket, address = listenSocket.accept()
    print('接受到一个客户端连接:', address)
    data = dataSocket.recv(BUFLEN)
    if not data:
        break
    info = data.decode()
    if info == "exit":
        break
    print(f'来自客户端{address}的消息：{info}')
    info = int(info)
    sum = sum + info
    print(f'sum={sum}')
    dataSocket.send(f'客户端{sum},'.encode())
    print(f'服务器回复了sum：{sum}')
dataSocket.close()  # 关闭客户端套接字
listenSocket.close()  # 关闭服务端端套接字
