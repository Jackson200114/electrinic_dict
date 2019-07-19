"""
    加密演示
"""
import getpass
import hashlib

pwd=getpass.getpass()
print(pwd)

#加密处理
hash=hashlib.md5("%&^$45".encode())#加盐处理
hash.update(pwd.encode())#算法加密
pwd=hash.hexdi
print(pwd)