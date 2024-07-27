import pyautogui  # 用于控制鼠标键盘
import urllib, requests  # 用于请求和解析链接
import pyperclip  # 用于访问剪切板
import time


# copy()函数，将用户新消息复制到剪切板
def copy():
    # new_msg1.png,用于判断是否有新消息
    if pyautogui.locateOnScreen("new_msg1.jpg") != None:
        print("检测到新消息...")
        # 定位到屏幕上新消息坐标
        msg_loc = pyautogui.locateOnScreen('message.jpg')
        # 将鼠标移动到新消息上
        pyautogui.moveTo(msg_loc, duration=0.05)
        # 右键新消息（可以出现复制选项）
        pyautogui.click(msg_loc, button="right")
        # 定位“复制”图像在屏幕上的坐标
        copy_icon = pyautogui.locateOnScreen("copy.png")
        # 确定“复制”中心点
        center = pyautogui.center(copy_icon)
        # 鼠标左键“复制”
        pyautogui.click(center, button='left')


# qingyunke()，调用青云客API
def qingyunke(msg):
    # 将剪切板最新内容（新消息）赋值给re
    re = urllib.parse.quote(msg)
    print("re:", re)
    # 调用带参的青云客API
    url = 'http://api.qingyunke.com/api.php?key=free&appid=0&msg={}'.format(re)
    # 将返回结果赋值给html
    html = requests.get(url)
    # 返回结果中的content内容
    return html.json()["content"]

def temp(msg):
    # 将剪切板最新内容（新消息）赋值给re
    re = urllib.parse.quote(msg)
    print("re:", re)


# send()函数，将qingyunke()返回结果作为回复内容发送出去
def send(reply):
    # 将reply复制一下（放在剪切板里）
    pyperclip.copy(reply)
    # 定位到微信编辑框，鼠标左键点击一次
    pyautogui.click(1400, 800, button='left')
    # 粘贴(将剪切板的内容放在编辑框)
    pyautogui.hotkey('ctrl', 'v')
    # 回车键，即发送编辑框中的内容
    pyautogui.press('enter')



time.sleep(2)
print("开始执行...")
cnt = 1
# 定时300秒
while cnt < 300:
    # 将用户新消息复制到剪切板
    copy()
    try:
        # 将消息赋值给msg
        msg = pyperclip.paste()
    except:
        # 如果没有消息，则“no message”
        msg = "no message"
    if msg != "no message":
        # 若有消息，则将新消息内容作为API参数，并将返回结果赋值给reply
        reply = qingyunke(msg)
        # 发送返回结果
        send(reply)
    pyperclip.copy("no message")
    cnt += 1
    time.sleep(1)
