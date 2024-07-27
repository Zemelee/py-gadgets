# UDP Client program
import socket
import gmpy2
from Crypto.Util.number import *


def decrypt(d, n, c):
    m = pow(c, d, n)
    return m


e = 65537
p1 = getPrime(512)
q1 = getPrime(512)
T = (p1 - 1) * (q1 - 1)
PublicKey = int(p1 * q1)
print("公钥已生成:\n", PublicKey)
PrivateKey = gmpy2.invert(e, T)  # 求大整数e模T的逆元,e * PriKey = 1 mod T
print("私钥已生成\n", PrivateKey, "\nPrivateKey的类型：\n", type(PrivateKey))
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.sendto(long_to_bytes(PublicKey), ("127.0.0.1", 11111))
print("公钥已发送至服务端")
cipher = udp.recv(1024)
print("密文已接收：", cipher)
cipher = bytes_to_long(cipher)  # cipher 的 PrivateKey 次方模 PublicKey
message = long_to_bytes(decrypt(PrivateKey, PublicKey, cipher))
# message = long_to_bytes(decrypt(PublicKey, cipher, PrivateKey))

print("解密后的明文：", message.decode())
udp.close()
