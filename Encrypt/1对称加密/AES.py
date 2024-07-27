import base64
from Crypto.Cipher import AES

"""
iv是初始化向量，第一组明文就是用它加密的
key是密钥，这里选择的长度是128比特，所以字符串的长度要固定在16
data就是需要加密的数据
"""
iv = '1234567887654321'
key = 'miyaoxuyao16ziji'


# 将原始的明文用空格填充到16字节
def pad(data):
    pad_data = data
    for i in range(0, 16 - len(data)):
        pad_data = pad_data + ' '.encode()
    return pad_data


# 将明文用AES加密
def AES_en(key):
    with open("a.txt", 'rb') as file:
        content = file.read()
        print("content", content)
        # 将长度不足16字节的字符串补齐
        if len(content) < 16:
            content = pad(content)
        # 创建加密对象  decode:二进制数据解码成unicode编码  encode将unicode编码的字符串编码成二进制
        AES_obj = AES.new(key.encode("utf-8"), AES.MODE_CBC, iv.encode("utf-8"))
        # 完成加密
        AES_en_str = AES_obj.encrypt(content)
        print("AES_en_str1", AES_en_str)
        # Base64就是一种基于64个可打印字符来表示二进制数据的方法
        AES_en_str = base64.b64encode(AES_en_str)
        print("AES_en_str2", AES_en_str)
        # 最后将密文转化成字符串
        AES_en_str = AES_en_str.decode("utf-8")
        print("AES_en_str3", AES_en_str)
        return AES_en_str


def AES_de(key, data):
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


data = AES_en(key)
print("2222", type(data))

data = AES_de(key, data)
print(data)
