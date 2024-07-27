# UDP Server program
import socket
from Crypto.Util.number import *

e = 65537

def encrypt(e, n, m):
    m = bytes_to_long(m)
    c = pow(m, e, n)  # m的e次幂初一n后的数
    return c
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
print("已接收到客户端公钥")

PublicKey = bytes_to_long(PublicKey)
print("PublicKey----",PublicKey)
data = input(">>>").encode()
send_data = long_to_bytes(encrypt(e, PublicKey, data))
udpserver.sendto(send_data, addr)
print("密文已发送")
udpserver.close()
