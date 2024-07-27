"""
假设有票的编号为 1-100，有 4 个窗⼝可以同时售票，车票按顺序依次售出。
1号和2号窗⼝有20 ⼈排队，3 号和 4 号窗⼝有 30 ⼈ 排队
每售出⼀张票，显示售票窗⼝号、票号以及余票数量
"""
import threading
import time

tickets = 100  # 票
t_num = 0  # 票号
lock = threading.Lock()


# 售票窗口类
class TicketWindows(threading.Thread):
    def __init__(self, window_name, num):
        threading.Thread.__init__(self)
        self.num = num
        self.window_name = window_name

    def run(self):
        sell_tickets(self.window_name, self.num)


def sell_tickets(threadName, num):
    global tickets
    global t_num
    while tickets > 0 and num > 0 and t_num <= 100:
        lock.acquire()  # 加一个同步锁
        if tickets > 0 and num > 0:
            print(threadName, f"准备票号{t_num + 1}，总余票还余：{tickets}张,本窗口还余{num}张")
            tickets -= 1
            num -= 1
            t_num += 1
            print(threadName, f"出票{t_num}，总余票还余：{tickets}张,本窗口还余{num}张")
            print("----------------------------------")
        else:
            print(threadName, "车票售空！")
        lock.release()  # 释放同步锁
        try:
            time.sleep(0.5)
        except RuntimeError:
            print("error!")


if __name__ == '__main__':
    window1 = TicketWindows("窗口1", 20)
    window2 = TicketWindows("窗口2", 20)
    window3 = TicketWindows("窗口3", 30)
    window4 = TicketWindows("窗口4", 30)
    window1.start()
    window2.start()
    window3.start()
    window4.start()
    window1.join()
    window2.join()
    window3.join()
    window4.join()
    print("退出主线程")
