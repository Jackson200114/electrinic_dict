import pymysql, signal, sys
from multiprocessing import Process
from socket import *
from mysql import Database

db=Database(database="dict")


# db = pymysql.connect(host="localhost",
#                      port=3306,
#                      user="root",
#                      password="123456",
#                      database="dict",
#                      charset="utf8")
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
            db.close()
            sys.exit("服务器退出")
        except Exception as e:
            print(e)
            continue

        # 为客户端创造子进程
        p = Process(target=recvcomend, args=(s, cur))
        p.start()


def recvcomend(s, cur):
    db.create_cursor()

    while True:
        comend = cur.recv(1024).decode()
        if comend == "sign":
            sign_in(s, cur)
        elif comend == "register":
            register(s, cur)
        elif comend == "quit":
            quit_out(s, cur)


def sign_in(s, cur):
    while True:
        name = cur.recv(1024).decode()
        db = pymysql.connect(host="localhost",
                             port=3306,
                             user="root",
                             password="123456",
                             database="dict",
                             charset="utf8")
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
    db.close()

def register(s, cur):
    db = pymysql.connect(
                        host="localhost",
                        port=3306,
                        user="root",
                        password="123456",
                        database="dict",
                        charset="utf8"
                        )
    c=db.cursor()
    while True:
        name=cur.recv(1024).decode()
        sql="select * from user where name=%s;"
        c.execute(sql,(name,))
        if c.fetchone():
            cur.send("用户名已存在".encode())
        else:
            cur.send("OK".encode())
            break
    password=cur.recv(1024).decode()
    sql="insert into user values(%s,%s)"
    c.execute(sql,(name,password))
    db.commit()
    cur.send("OK".encode())
    c.close()
    db.close()

def quit_out(s,cur):
    cur.send("OK".encode())


main()
