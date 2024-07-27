import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("www.sicnu.edu.cn", 80))
# 根据http协议格式,向服务器发送headers请求
s.send('GET / HTTP/1.1\r\n'.encode())  # 去掉回车换行反斜杠
s.send('Host:www.sicnu.edu.cn\r\n'.encode())
s.send('Connection:close\r\n\r\n'.encode())
buffer = []
while True:
    d = s.recv(1024)
    if d:
        buffer.append(d)
    else:
        break
data = b''.join(buffer)
s.close()
header, html = data.split(b'\r\n\r\n', 1)  # 1代表分割
print(header.decode('utf-8'))
# 接受到的数据写入文件，生成网页
with open('web.html', 'wb') as f:
    f.write(html)
s.close()
