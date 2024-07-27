import socket

HOST = '127.0.0.1'
SERVER_PORT = 21211
BUFLEN = 256
data = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
data.connect((HOST, SERVER_PORT))
print('连接成功')

while True:
    toSend = input('>>>')
    if toSend == 'exit':
        break
        # 发送消息，编码为bytes
    data.send(toSend.encode())
    # 发送完成后等待接收服务端消息
    recved = data.recv(BUFLEN)  # 阻塞状态会暂停运行代码
    # 如果recved为空，则服务器关闭连接
    if not recved:
        break
    print("toSend--->", toSend)
    print("recvd.decode()---->", recved.decode())

data.close()
