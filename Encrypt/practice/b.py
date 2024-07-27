# UDP Server program
import socket


udpserver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpserver.bind(("127.0.0.1", 11111))
print("服务已开启...")
# 接收来自客户端的公钥和地址
"""
n 公钥
data 明文
send_data 加密后的数据
"""
PublicKey, addr = udpserver.recvfrom(1024)
print("PublicKey----",PublicKey)
print("已接收到客户消息")

data = input(">>>").encode()

udpserver.send(data)
print("密文已发送")
udpserver.close()
