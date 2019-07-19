import pymysql, signal, sys
from multiprocessing import Process
from socket import *
from time import sleep
import hashlib
from mysql import Database

# db=Database(database="dict")
SALT = "@@@"  # 盐

db = pymysql.connect(host="localhost",
                     port=3306,
                     user="root",
                     password="123456",
                     database="dict",
                     charset="utf8")


def main():
    s = socket()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    ADDR = "0.0.0.0"
    PORT = 2333
    s.bind((ADDR, PORT))
    s.listen(5)
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
    print("listen the port 2333")
    while True:
        try:
            cur, addr = s.accept()
            print("Connect from", addr)
        except KeyboardInterrupt:
            s.close()
            # db.close()
            sys.exit("服务器退出")
        except Exception as e:
            print(e)
            continue

        # 为客户端创造子进程
        p = Process(target=recvcomend, args=(s, cur))
        p.start()


def recvcomend(s, cur):
    # db.create_cursor()

    while True:
        comend = cur.recv(1024).decode()
        if comend == "sign":
            sign_in(s, cur)
        elif comend == "register":
            register(s, cur)
        elif comend == "quit":
            quit_out(s, cur)
        elif comend == "find":
            find(s, cur)
        elif comend=="history":
            history(s,cur)


def sign_in(s, cur):
    while True:
        name = cur.recv(1024).decode()
        # db = pymysql.connect(host="localhost",
        #                      port=3306,
        #                      user="root",
        #                      password="123456",
        #                      database="dict",
        #                      charset="utf8")
        c = db.cursor()
        sql = "select name from user where name=%s;"
        c.execute(sql, (name,))
        if c.fetchone():
            cur.send("OK".encode())
            break
        else:
            cur.send("用户名不存在".encode())
    while True:
        password = cur.recv(2048).decode()
        sql = "select * from user where name=%s and password=%s;"
        c.execute(sql, (name, password))
        if c.fetchone():
            cur.send("OK".encode())
            break
        else:
            cur.send("密码错误")
    print("登录成功")
    c.close()
    # db.close()


def register(s, cur):
    # db = pymysql.connect(
    #                     host="localhost",
    #                     port=3306,
    #                     user="root",
    #                     password="123456",
    #                     database="dict",
    #                     charset="utf8"
    #                     )
    c = db.cursor()
    while True:
        name = cur.recv(1024).decode()
        sql = "select * from user where name=%s;"
        c.execute(sql, (name,))
        if c.fetchone():
            cur.send("用户名已存在".encode())
        else:
            cur.send("OK".encode())
            break
    password = cur.recv(1024).decode()
    # password = change_password(name, password)
    sql = "insert into user values(%s,%s)"
    c.execute(sql, (name, password))
    db.commit()
    cur.send("OK".encode())
    c.close()
    # db.close()


def change_password(name, password):
    hash = hashlib.md5(name + SALT).encode()  # 加盐
    hash.update(password.encode())  # 加密算法
    password1 = hash.hexdigest  # 加密后的密码
    return password1


def quit_out(s, cur):
    cur.send("OK".encode())


def find(s, cur):
    user_name = cur.recv(1024).decode()
    c = db.cursor()
    while True:
        word = cur.recv(2048).decode()
        if word == "Q":
            cur.send("OK Q".encode())
            c.close()
            break
        try:
            sql1 = "select explaining from words where word=%s;"
            c.execute(sql1, (word,))
            if c.fetchone():
                one_row = c.fetchone()
                cur.send(("S " + one_row[0]).encode())
                sql2 = "insert into hist(name,word) values(%s,%s);"
                c.execute(sql2, (user_name, word))
                hist_list = find_hist(c, user_name)
                if len(hist_list) > 10:
                    # print(len(hist_list))
                    delete_eleventh(c, user_name)
                db.commit()
            else:
                cur.send("F 查无此词，请重新输入".encode())
        except Exception as e:
            cur.send("F 查询失败".encode())
            print(e)


def find_hist(c, name):
    """
    通过姓名查找历史搜索记录
    :param c:
    :param name:
    :return:
    """
    sql = "select word from hist where name =%s order by time;"
    c.execute(sql, (name,))
    hist_list = c.fetchmany(11)
    if hist_list:
        # print(c.fetchmany(11))
        return hist_list
    else:
        return []


def delete_eleventh(c, name):
    sql = "select * from hist where name =%s order by time limit 1;"
    c.execute(sql, (name,))
    eleventh = c.fetchone()[2]
    sql2 = "delete from hist where time=%s limit 1;"
    c.execute(sql2, (eleventh,))
    db.commit()

def history(s,cur):
    c=db.cursor()
    user_name=cur.recv(1024)
    hist_list=find_hist(c,user_name)
    for i in hist_list:
        cur.send(i[0].encode())
        sleep(0.1)
    else:
        cur.send("Q".encode())

main()
