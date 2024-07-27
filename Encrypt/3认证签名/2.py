# 客户端
import hashlib
import socket
import base64
from Crypto.Cipher import AES
from Crypto.Util.number import *
import gmpy2


# MD5加密函数
def MD5(message):
    m = hashlib.md5()  # 创建md5对象
    m.update(message.encode('utf-8'))
    return m.hexdigest()  # 返回摘要，作为十六进制数据字符串值


# 解密函数

def AES_de(data):
    iv = '1234567887654321'
    key = 'seckeyneed16byte'

    # 解密过程逆着加密过程写
    # 将密文字符串重新编码成二进制形式
    data = data.encode("utf-8")
    # 将base64的编码解开
    data = base64.b64decode(data)
    # 创建解密对象
    AES_de_obj = AES.new(key.encode("utf-8"), AES.MODE_CBC, iv.encode("utf-8"))
    # 完成解密
    AES_de_str = AES_de_obj.decrypt(data)
    # 去掉补上的空格
    AES_de_str = AES_de_str.strip()
    # 对明文解码
    AES_de_str = AES_de_str.decode("utf-8")
    return AES_de_str


def decrypt(d, n, c):
    m = pow(c, d, n)  # c的d次方模n
    return m


e = 65537
p1 = getPrime(512)
q1 = getPrime(512)
T = (p1 - 1) * (q1 - 1)
PrivateKey = gmpy2.invert(e, T)

# 接收公钥、接收明文、接收RSA密文、接收AES密文、
C = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
C.connect(('127.0.0.1', 11111))
print('连接成功')

# 接收服务端公钥
PublicKey, addr = C.recvfrom(1024)

# n 服务端公钥
PublicKey = bytes_to_long(PublicKey)
print("接收到服务端公钥：\n", PublicKey, "\nPublicKey：\n", type(PublicKey))

content = C.recv(512).decode('utf-8')
print("明文已接收:\n", content)

# 接收密文
en_txt = C.recv(512)
print("接收到的密文en_txt：\n", en_txt)

# 解密RSA密文
cipher = bytes_to_long(en_txt)
# PublicKey = bytes_to_long(PublicKey)
# cipher 的 PrivateKey 次方模 PublicKey
AESTXT = long_to_bytes(decrypt(PrivateKey, PublicKey, cipher))
print("解密后的AES密文:\n", AESTXT)

print("-" * 10)
AEStxt = C.recv(512).decode('utf-8')
print("AES密文：\n", AEStxt)

# 解密AES密文
hash2 = AES_de(AEStxt)
print("解密AES密文的hash2值：\n", hash2)

hash1 = MD5(content)
print("明文hash1值为：\n", hash1)
if hash1 == hash2:
    print("相同")
else:
    print("不同")
