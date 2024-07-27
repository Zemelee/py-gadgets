# UDP Client program
import socket


udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# cd 网络编程\practice  python udpServer.py

udp.sendto(b"sa", ("127.0.0.1", 11111))
print("已发送至服务端")
msg = udp.recv(1024)
print("信息已接收：", msg.decode('utf-8'))



udp.close()
