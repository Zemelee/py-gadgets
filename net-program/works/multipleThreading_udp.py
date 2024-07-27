import socket
import threading


def send_msg(udp_socket, ip, port):
    while True:
        send_data = input(">>>")
        data = send_data.encode("gbk")
        udp_socket.sendto(data, (ip, port))
        if send_data == "exit":
            print("sender exiting...")
            break


# 接收函数
def recv_msg(udp_socket):
    while True:
        # recv_from函数返回的对象是一个元组，包含数据的内容和来源
        recv_data = udp_socket.recvfrom(1024)
        data = recv_data[0].decode("gbk")
        print("你收到的数据是:", data)
        if data == "exit":
            print("Receiver exiting...")
            break


# 基于UDP的聊天
IP = '127.0.0.1'
PORT = 8081


if __name__ == "__main__":
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind((IP, PORT))
    # 4。 创建两个子线程，一个用于发送数据，一个用于接收数据
    t_send = threading.Thread(target=send_msg, args=(udp_socket, IP, PORT))
    t_recv = threading.Thread(target=recv_msg, args=(udp_socket,))
    t_recv.start()
    t_send.start()
