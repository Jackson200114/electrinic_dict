import pymysql


class Database:
    def __init__(self, host="localhost",
                 port=3306,
                 user="root",
                 passwd="123456",
                 charset="utf8",
                 database=None):
        self.host = host
        self.port = port
        self.user = user
        self.password = passwd
        self.charset = charset
        self.database = database
        self.connect_database()  # 连接数据库

    def connect_database(self):
        self.db = pymysql.connect(host=self.host,
                                  port=self.port,
                                  user=self.user,
                                  password=self.password,
                                  charset=self.charset,
                                  database=self.database)

    def increase(self):
        pass
    def close(self):
        self.db.close()
    def create_cursor(self):
        self.cur=self.db.cursor()