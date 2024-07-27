# 回声服务器编:服务器能够返回客户端发送的数据(运行时请输入自己的学号、姓名)。
import socket
from threading import Thread

IP = '127.0.0.1'
PORT = 8982
sever_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sever_udp.bind((IP, PORT))


# 接受
def recv_fun():
    print('----接收程序已就绪----')
    while True:
        # sever_udp is binding with (IP,PORT)
        recv_data = sever_udp.recvfrom(1024)
        if recv_data[0].decode('utf-8') == '':
            print('检测到用户无输入，接收程序即将退出...')
            break
        print('recv_data', recv_data)
        print('{}:--->{}'.format(recv_data[1], recv_data[0].decode('utf-8')))
    print('接收程序已退出')


# 发送
def send_fun():
    print('----发送程序已就绪----')
    while True:
        addr = (IP, PORT)
        data = input('>>>')
        if data == 'exit' or data == "":
            print('检测到用户退出，发送程序即将停止...')
            break
        sever_udp.sendto((data.encode('utf-8')), addr)
    print("发送程序已退出")


if __name__ == '__main__':
    # 创建线程对象
    t1 = Thread(target=send_fun)  # t1 <Thread(Thread-1 (send_fun), initial)>
    t2 = Thread(target=recv_fun)  # t2 <Thread(Thread-2 (recv_fun), initial)>
    t1.start()  # 启动线程
    t2.start()
    t1.join()  # 回收阻塞
    t2.join()
print('程序已关闭')
