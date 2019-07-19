import re, os, sys
from socket import *


# cur = db.cursor()
def index():
    s = socket()
    ADDR = "127.0.0.1"
    PORT = 2333
    s.connect((ADDR, PORT))
    # cur,addr=s.accept()
    while True:
        print("====================")
        print("#    请选择服务      #")
        print("#   登录 注册 退出   #")
        print("====================")
        choice = input("选择服务为:")
        if choice == "登录":
            sign_in(s)
        elif choice == "注册":
            register(s)
        elif choice == "退出" or choice == "":
            quit_out(s)
        else:
            print("指令错误，请重新输入")


def sign_in(s):
    s.send("sign".encode())
    while True:
        name = input("请输入用户名:")
        s.send(name.encode())
        res = s.recv(1024).decode()
        if res == "OK":
            break
        else:
            print("用户名不存在")
    while True:
        password = input("请输入密码:")
        s.send(password.encode())
        res = s.recv(1024).decode()
        if res == "OK":
            print("登录成功")
            break
        else:
            print("密码错误")
    second_page(s, name)


def register(s):
    s.send("register".encode())
    while True:
        name = input("请输入新用户名:")
        s.send(name.encode())
        res = s.recv(1024).decode()
        if res == "OK":
            break
        else:
            print("用户名已存在")
    while True:
        password = input("请输入新密码:")
        password2 = input("请再一次输入相同密码:")
        if password == password2:
            break
        else:
            print("两次密码不同，请重新输入")
    s.send(password.encode())
    res2 = s.recv(1024).decode()
    if res2 == "OK":
        print("注册成功，请登录")
        sign_in(s)
    else:
        print(res2)


def quit_out(s):
    s.send("quit".encode())
    res = s.recv(1024).decode()
    if res == "OK":
        print("退出成功")
        sys.exit()


def second_page(s, name):
    while True:
        print("====================")
        print("# 请选择电子词典服务  #")
        print("# 查询 历史记录 注销  #")
        print("====================")
        choice = input("选择服务为:")
        if choice == "查询":
            s.send("find".encode())
            find(s, name)
        elif choice=="历史记录":
            s.send("history".encode())
            history(s,name)
        elif choice=="注销":
            print("注销成功")
            break
        else:
            print("指令错误，请重新输入")

def find(s, name):
    s.send(name.encode())
    while True:
        word = input("请输入要查找的单词,输入Q则取消查询:")
        s.send(word.strip().encode())
        res = s.recv(2048).decode()
        # print("res=",res)
        response = res.split(" ")
        # print("response=",response)
        if response[0] == "F":
            print(response[1])
        elif response[0] == "S":
            print(" ".join(response[1:-1]))
        elif response[0] == "OK":
            print("退出查询")
            break

def history(s,name):
    s.send(name.encode())
    print("查询历史为:")
    while True:
        res=s.recv(1024).decode()
        if res=="Q":
            break
        print("    "+res)
    print("历史记录查询完成")


index()
