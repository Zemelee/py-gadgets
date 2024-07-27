# 服务端
import hashlib
import socket
from Crypto.Cipher import AES
import base64
import gmpy2
from Crypto.Util.number import *

# 生成公钥私钥
def keys():
    e = 65537
    p1 = getPrime(512)
    q1 = getPrime(512)
    T = (p1 - 1) * (q1 - 1)
    PublicKey = int(p1 * q1)
    PrivateKey = gmpy2.invert(e, T)  # 求大整数e模T的逆元,e * PriKey = 1 mod T
    return PublicKey, int(PrivateKey), e


def encrypt(e, n, m):
    m = bytes_to_long(m)
    c = pow(m, e, n)  # m的e次幂模n
    return c


# MD5加密函数
def MD5(message):
    m = hashlib.md5()  # 创建md5对象
    m.update(message.encode('utf-8'))
    return m.hexdigest()  # 返回摘要，作为十六进制数据字符串值


# 将原始的明文用空格填充到16字节
def pad(data):
    pad_data = data
    for i in range(0, 16 - len(data)):
        pad_data = pad_data + ' '.encode()
    return pad_data


# 将明文用AES加密
def AES_en(content):
    iv = '1234567887654321'
    key = 'seckeyneed16byte'
    # 将长度不足16字节的字符串补齐
    if len(content) < 16:
        content = pad(content)
    # print("content---",type(content))
    # 创建加密对象  decode:二进制数据解码成unicode编码  encode将unicode编码的字符串编码成二进制
    AES_obj = AES.new(key.encode("utf-8"), AES.MODE_CBC, iv.encode("utf-8"))
    # 完成加密
    AES_en_str = AES_obj.encrypt(content)
    # print("AES_en_str1", AES_en_str)
    # Base64就是一种基于64个可打印字符来表示二进制数据的方法
    AES_en_str = base64.b64encode(AES_en_str)
    # print("AES_en_str2", AES_en_str)
    # 最后将密文转化成字符串
    AES_en_str = AES_en_str.decode("utf-8")
    # print("AES_en_str3", AES_en_str)
    return AES_en_str


# 发送公钥、文件内容、发送RSA密文、AES密文
S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
S.bind(('127.0.0.1', 11111))
S.listen(1)
print('服务在11111端口等待连接...')
dataSocket, CliAdd = S.accept()
print('接受到一个客户端连接：', CliAdd)

PublicKey, PrivateKey, e = keys()
# 发送公钥至客户端(int--->bytes)
dataSocket.send(long_to_bytes(PublicKey))
print("公钥已发送至客户端:\n", PublicKey)
# 发送文件内容
with open("a.txt", 'r') as f:
    content = f.read()
print("content:\n", content)
dataSocket.send(content.encode())
print("文件内容已发送:\n", content)

# 生成摘要
hash = MD5(content)
print("hash值：\n", hash)
hash = str(hash)
# 生成密文
AES_txt = AES_en(hash.encode())
print("AES对称加密后的密文：\n", AES_txt,"\nAES密文类型：\n",type(AES_txt))

# 私钥加密
data = AES_txt.encode()
RSA_txt = long_to_bytes(encrypt(e, PublicKey, data))

# 发送RSA密文
dataSocket.send(RSA_txt)  # 发送至B
print("RSA密文已发送:\n", RSA_txt)
# 发送密文
dataSocket.send(AES_txt.encode())  # 发送至B
print("AES密文已发送：\n", AES_txt)
