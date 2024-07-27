## Attention!!! 2severFile. Py and 2clientFile.py should not be placed in the same path
## The file name entered is the file under the server path
# and the effect is that the file is downloaded to the client path!!!
# bug :下载的文件一定要在运行目录下！！！
import socket,os
tcp_socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket_server.bind(('127.0.0.1', 6666))
tcp_socket_server.listen(3)
print(f'Service started, waiting for connection at port 6666...')
client_socket, address = tcp_socket_server.accept()
# python 网络编程/works/2severFile.py
while True:
    # 6、The file name sent by the receiving client
    recv_data = client_socket.recv(1024)
    print("recv_data:", recv_data)
    # 7、Read the file data according to the file name
    if not recv_data:
        break
    file_name = recv_data.decode("utf-8")
    print("file_name:", file_name)
    # 8、Send the read file data to the client (loop)
    try:
        # rb:Binary format read-only open, default mode
        with open(file_name, "rb") as file:
            while True:
                file_data = file.read(1024)
                if file_data != "":
                    client_socket.send(file_data)
                else:
                    break
        file.close()
    except:
        print("file {} in {}  not exist".format(file_name,os.getcwd()))
        break
    else:
        print("file %s Download succeeded" % file_name)
        break
client_socket.close()
print('Client connection disconnected')
tcp_socket_server.close()
print('Sever connection disconnected')
