import tornado.ioloop
import tornado.web
import tornado.websocket
import hashlib
import requests
import json

from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.PublicKey import RSA
import Crypto.Signature.PKCS1_v1_5 as sign_PKCS1_v1_5  # 用于签名/验签
import base64
from Crypto.Hash import MD5

# windows 系统下 tornado 使用 使用 SelectorEventLoop
import platform

if platform.system() == "Windows":
    import asyncio

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def qingyunke(text):
    a = requests.get(f"http://api.qingyunke.com/api.php?key=free&appid=0&msg={text}").text
    b = json.loads(a)
    return b['content']


# MD5加密函数
def md5(message):
    m = hashlib.md5()  # 创建md5对象
    m.update(message.encode('utf-8'))
    return m.hexdigest()  # 返回摘要，作为十六进制数据字符串值


# 加载服务器公钥文件
with open('public_server.pem', 'r') as f:
    public_server_key = f.read()
rsakey1 = RSA.importKey(public_server_key)
public_server = Cipher_pkcs1_v1_5.new(rsakey1)

# 加载服务器私钥文件
with open('private_server.pem', 'r') as f:
    private_server_key = f.read()
rsakey3 = RSA.importKey(private_server_key)
# private_server_sign = sign_PKCS1_v1_5.new(rsakey3)
private_server = Cipher_pkcs1_v1_5.new(rsakey3)

# 加载客户端公钥文件 验签
with open('public_client.pem', 'r') as f:
    public_client_key = f.read()
rsakey2 = RSA.importKey(public_client_key)
public_client = rsakey2

# 加载客户端私钥文件
with open('private_client.pem', 'r') as f:
    private_client_key = f.read()
rsakey4 = RSA.importKey(private_client_key)
private_client = Cipher_pkcs1_v1_5.new(rsakey4)


# 服务端私钥签名
def server_sign(text):
    # 初始化服务端签名私钥
    private_server_sign = sign_PKCS1_v1_5.new(rsakey3)
    hash = MD5.new()
    hash.update(text.encode())
    sign = private_server_sign.sign(hash)
    signature = base64.b64encode(sign)
    return signature


def to_verify(signature, plain_text, public_key):
    # 验签
    signature = base64.b64decode(signature)
    verifier = sign_PKCS1_v1_5.new(public_key)
    _rand_hash = MD5.new()
    _rand_hash.update(plain_text.encode())
    verify = verifier.verify(_rand_hash, signature)
    return verify  # true / false


mayday_sign = server_sign("mayday")
print("mayday_sign:", mayday_sign)
mayday_sign_verify = to_verify(mayday_sign, "mayday", rsakey1)
print("mayday_sign_verify:", mayday_sign_verify)


# 登录页面
class Login(tornado.web.RequestHandler):
    # 当浏览器访问时自动调用
    def get(self):
        # 向浏览器页面返回内容
        self.render("login.html")

    def post(self):
        uname = self.get_argument('username')
        passwd = self.get_argument('password')
        if uname in ['lzm', 'wangwu'] and passwd == '123':
            # 设置cookie，保持登录状态
            self.set_cookie('uname', uname, expires_days=1)
            # 跳转聊天室页面
            self.redirect('/chat')
        else:
            self.write('登录失败')


# 聊天室页面
class Chat(tornado.web.RequestHandler):
    # 当浏览器访问时自动调用
    def get(self):
        # 获取当前登录的用户名
        uname = self.get_cookie('uname')
        # 向浏览器页面返回内容
        self.render("chatroom.html", uname=uname)


# 聊天功能
class Chatroom(tornado.websocket.WebSocketHandler):
    # 在线用户
    online_users = []

    # 在一个新的WebSocket链接建立时，Tornado框架会调用此函数
    def open(self, *args, **kwargs):
        uname = self.get_cookie('uname')
        print(f'用户{uname}进入聊天室...')
        self.online_users.append(self)

    # 当收到来自客户端的消息时，Tornado框架会调用本函数
    def on_message(self, message):
        # 获取当前聊天室
        uname = self.get_cookie('uname')
        print(f"接收来自{uname}消息：", message)  # PUb(m|H(m))|sign(m)
        msg1 = message.split("|", 1)[0]
        msg1 = private_server.decrypt(base64.b64decode(msg1), None).decode()
        print("解密msg1得到：", msg1)
        msg11 = msg1.split("|", 1)[0]
        msg12 = msg1.split("|", 1)[1]
        if (md5(msg11) == msg12):
            print("消息完整性安全")
        else:
            print("消息完整性不安全")
        sign = message.split("|", 1)[1]
        print("sign：", sign)
        # sign = base64.b64decode(sign)
        verify = to_verify(sign, msg11, public_client)
        if (verify):
            print("签名安全")
            # private_client
            for user in self.online_users:
                # msg11_sign = server_sign(msg11)
                user.write_message(f'[{uname}]:{msg11}')
        else:
            reply = qingyunke(msg11)
            print("签名不安全")
            for user in self.online_users:
                user.write_message(f'[{uname}]:消息不安全,未予以展示！！')
                user.write_message(f'[警告]:{reply}')

    # 有用户退出聊天室
    def on_close(self):
        uname = self.get_cookie('uname')
        self.online_users.remove(self)
        print(f"用户{uname}退出聊天室...")


def make_app():
    # 创建tornado应用对象
    app = tornado.web.Application(
        handlers=[
            # 路由：网址和类的对应
            (r'/login', Login),
            (r'/chat', Chat),
            (r'/chatroom', Chatroom),
        ]
    )
    return app


if __name__ == "__main__":
    app = make_app()
    app.listen(8888, '192.168.3.5')
    print('服务已192.168.3.5:8888启动...')
    tornado.ioloop.IOLoop.current().start()
