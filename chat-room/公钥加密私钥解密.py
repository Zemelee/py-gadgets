from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64


# 公钥验签，加密
def rsa_encrypt(plain):
    with open('public_client.pem', 'rb') as f:
        data = f.read()
        key = RSA.importKey(data)
        rsa = PKCS1_v1_5.new(key)
        cipher = rsa.encrypt(plain)
        return base64.b64encode(cipher)


# 私钥加签，解密
def rsa_decrypt(cipher):
    with open('private_client.pem', 'rb') as f:
        data = f.read()
        key = RSA.importKey(data)
        rsa = PKCS1_v1_5.new(key)
        plain = rsa.decrypt(base64.b64decode(cipher), 'ERROR')  # 'ERROR'必需
        return plain


if __name__ == '__main__':
    plain_text = b'mayday'
    cipher = rsa_encrypt(plain_text)
    print("cipher:", cipher)
    mayday_js_sign = b"pLfH5eXesiL9cw9nE+nLzjxqJCbWogaPfbx5bQLO7a6X7BtvEi9y88g29snsnbFYH8vemT/CenGK1n9KYWJRmpENyU223bAZZ3MS7omPnjdxPhKyoSMHrkljTKWd1Z/OCSLdxOMRGhyCxdnYG54KVHK46fxfDf1jWC8mgO1aDNQ="
    plain = rsa_decrypt(cipher)
    print("plain", plain)
