from flask import Flask, render_template,request  # 调用flask工具中的render_template类


app = Flask(__name__)  # 定义一个实例对象叫app,引用flask类

@app.route('/')  # 定义路径为/。即根目录（直接点击网址进入的界面）
def index():  # 在这个路径下定义一个方法叫index
    return '搭建服务测试'  # 调用这个方法会返回'搭建服务测试'，即令页面显示这串字符


@app.route('/login')  # 定义路径为根目录/login
def login():  # 在这个路径下定义一个方法叫login

    return render_template("login.html")  # 调用这个方法会返回HTML网页【login】


@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        return 'get'
    if request.method == 'POST':
        return 'post'

    return 'ok'

if __name__ == '__main__':  # 固定格式，上面放定义的函数，下面放函数的调用
    app.run()  # 运行app

