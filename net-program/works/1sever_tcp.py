import socket

HOST = '127.0.0.1'
PORT = 21211
BUFLEN = 256
# 实例化一个socket对象listen
# AF_INET表示该socket网络层使用ip协议，SOCK_STREAM传输层使用tcp协议，SOCK_DGRAM是基于UDP
# socket.bind 、listen、accept、recv、send
listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# socket绑定地址和端口，客户端需要连接该socket的ip和port
listen.bind((HOST, PORT))
# 使socket处于监听状态，等待客户端连接
# 1表示最多接受1个客户端，listen用来监听
listen.listen(1)
# print("listen3-------->",listen)
print(f'服务启动成功，在{PORT}端口等待连接...')
# dataSocket产生新的socket
# address---->('127.0.0.1', ****)
dataSocket, address = listen.accept()


while True:
    data = dataSocket.recv(BUFLEN)
    # data--->b'(客户端发送的消息)'
    # 如果返回空bytes表示对方关闭连接，退出循环结束消息收发
    if not data:
        print("not a data")
        break
    print("data", data)
    # 读取字节数据为byte类型，需解码为字符串
    info = data.decode()
    print(f'收到客户端信息--->{info}')
    dataSocket.send(f'我是服务器,你的消息是‘{info}’,我已经知道了'.encode())
    # 发送的类型必须为bytes，所以要编码

dataSocket.close()  # 关闭客户端套接字
listen.close()  # 关闭服务端端套接字
