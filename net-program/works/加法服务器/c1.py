import socket
import sys
# 简易对话
HOST = '127.0.0.1'
SERVER_PORT = 11111
BUFLEN = 512
# 实例化socket对象，指明协议
dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dataSocket.connect((HOST, SERVER_PORT))
print(f'我是客户端，与服务器{HOST}:{SERVER_PORT}连接成功')
toSend = input('>>>')
# 退出发送
if toSend == 'exit':
    dataSocket.send(toSend.encode())
    dataSocket.close()
    sys.exit()
# 发送消息，编码为bytes
dataSocket.send(toSend.encode())
print('Send:', repr(toSend))  # repr将变量转换成字符串对象
# 发送完成后等待接收服务端消息
recved = dataSocket.recv(BUFLEN)  # 阻塞状态会暂停运行代码
print('recv:', repr(recved.decode()))
# 如果recved为空，则服务器关闭连接
dataSocket.close()
