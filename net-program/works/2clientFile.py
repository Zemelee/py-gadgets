import socket

HOST = '127.0.0.1'
SERVER_PORT = 6666
tcp_socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket_client.connect((HOST, SERVER_PORT))
print('连接成功')

# 4、接收⽤户输⼊的⽂件名
file_name = input("输入要下载的文件名:")
tcp_socket_client.send(file_name.encode("utf-8"))
print('请求已发送')
# 6、创建⽂件，准备接收服务端返回的⽂件数据
flag = 0  # 0无1有
with open("D:\PyGadgets\网络编程\practice\\" + file_name, "wb") as file:
# 7、保存⽂件数据
    while True:
        recv_data = tcp_socket_client.recv(1024 * 10)
        print('recv_data----', recv_data)
        if recv_data != b'':
            flag = 1
            print('正在写入文件...')
            file.write(recv_data)
            print("刚写进的数据是---->", recv_data)
            break
        else:
            print("break")
            break
    print("文件关闭啦")
file.close()

if flag == 1:
    print('下载完成')
else:
    print('无此文件，下载失败')

print('断开连接')

# 8、关闭套接字
tcp_socket_client.close()
print("和服务器已断开连接")
