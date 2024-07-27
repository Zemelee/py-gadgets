import socket
import ssl

# Web page request based on https
baidu = "www.baidu.com"  # 1
autumnfish = "autumnfish.cn"  # 2
music = "music.163.com"  # 3
# create a ssl socket
s = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
s.connect((f"{baidu}", 443))
print("connect~!")
# Send headers request to the server according to the http protocol format
# 根据http协议格式向服务器发送头请求
s.send('GET / HTTP/1.1\r\n'.encode())  # Remove carriage return line break backslash
s.send(f'Host:{baidu}\r\n'.encode())
s.send(
    'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) '
    'Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10'.encode())
s.send('Connection:close\r\n\r\n'.encode())

buffer = []
while True:
    d = s.recv(1024)
    # print('d--->', d)
    if d:
        buffer.append(d)
    else:
        break
data = b''.join(buffer)
# print('data----->', data)
s.close()
# header：响应头，html：请求体（源代码）
header, html = data.split(b'\r\n\r\n', 1)
print(html)
print("---------------------------")
print(header.decode('utf-8'))
# The received data is written to a file to generate a web page
with open('download.html', 'wb') as f:
    f.write(html)
s.close()
