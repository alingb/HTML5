#!/usr/bin/env python
# coding=utf-8
# -*-enconding:utf-8-*-
# TIME:2018/4/23 9:34
# FILE:test.py


# import Queue
# import threading
# import time
# import random
#
# q = Queue.Queue(0)
# NUM_WORKERS = 3
#
#
# class MyThread(threading.Thread):
#     def __init__(self, input, worktype):
#         self._jobq = input
#         self._work_type = worktype
#         super(MyThread, self).__init__()
#
#     def run(self):
#         while True:
#             Thread.acquire()
#             if self._jobq.qsize() > 0:
#                 Thread.release()
#                 self._process_job(self._jobq.get(), self._work_type)
#             else:
#                 Thread.release()
#                 break
#
#     def _process_job(self, job, worktype):
#         doJob(job, worktype)
#
#
# def doJob(job, worktype):
#     time.sleep(random.random() * 3)
#     print("doing", job, " worktype ", worktype)
#
#
# if __name__ == '__main__':
#     Thread = threading.Lock()
#     print "begin...."
#     for i in range(NUM_WORKERS * 2):
#         q.put(i)
#     print "job qsize:", q.qsize()
#
#     for x in range(NUM_WORKERS):
#         MyThread(q, x).start()

# def A():
#     print("this is A")
#
#
# def B():
#     print("this is B")
#
#
# func_list = [A, B]
# for i in func_list:
#     i()

# class Test1(object):
#     def __init__(self, error, test):
#         self.error = error
#         self.test = test
#
# class Test2(object):
#     def __init__(self, ip):
#         self.ip = ip
#
#
# a = {'a': 1}
# b = {"b": 2}
# c = list()
# c.append(Test1(a, 'b'))
# c.append(Test1(b, 'c'))
# c.append(Test2(b))
# print(c)

# import hashlib
#
# md5 = hashlib.md5()
# msg = "test"
# md5.update(msg.encode("utf-8"))
# print(md5.hexdigest())

# from io import StringIO
# from io import BytesIO
# s = StringIO()
# s.write("")
# print(s.getvalue())
# b = BytesIO()
# b.write(b'ls')
# b.write(b'dir')
# b.write(b'ip')
# print(b.getvalue())
# b.write(''.encode("utf-8"))
# print(b.getvalue())
#

# import random
# from faker import Factory
# from sqlalchemy import create_engine, Table
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import ForeignKey
# from sqlalchemy import Column, String, Integer, Text
# from sqlalchemy.orm import sessionmaker, relationship
#
# engine = create_engine('mysql+mysqldb://trusme:6286280300@192.168.1.57:3306/blog', echo=True)
# Base = declarative_base()
#
#
# class User(Base):
#     __tablename__ = 'users'
#
#     id = Column(Integer, primary_key=True)
#     username = Column(String(64), nullable=False, index=True)
#     password = Column(String(64), nullable=False)
#     email = Column(String(64), nullable=False, index=True)
#     articles = relationship('Article', backref='author')
#     userinfo = relationship('UserInfo', backref='user', uselist=False)
#
#     def __repr__(self):
#         return '%s(%r)' % (self.__class__.__name__, self.username)
#
#
# class UserInfo(Base):
#     __tablename__ = 'userinfos'
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String(64))
#     qq = Column(String(11))
#     phone = Column(String(11))
#     link = Column(String(64))
#     user_id = Column(Integer, ForeignKey('users.id'))
#
#
# class Article(Base):
#     __tablename__ = 'articles'
#
#     id = Column(Integer, primary_key=True)
#     title = Column(String(255), nullable=False, index=True)
#     content = Column(Text)
#     user_id = Column(Integer, ForeignKey('users.id'))
#     cate_id = Column(Integer, ForeignKey('categories.id'))
#     tags = relationship('Tag', secondary='article_tag', backref='articles')
#
#     def __repr__(self):
#         return '%s(%r)' % (self.__class__.__name__, self.title)
#
#
# class Category(Base):
#     __tablename__ = 'categories'
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String(64), nullable=False, index=True)
#     articles = relationship('Article', backref='category')
#
#     def __repr__(self):
#         return '%s(%r)' % (self.__class__.__name__, self.name)
#
#
# article_tag = Table(
#     'article_tag', Base.metadata,
#     Column('article_id', Integer, ForeignKey('articles.id')),
#     Column('tag_id', Integer, ForeignKey('tags.id'))
# )
#
#
# class Tag(Base):
#     __tablename__ = 'tags'
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String(64), nullable=False, index=True)
#
#     def __repr__(self):
#         return '%s(%r)' % (self.__class__.__name__, self.name)
#
#
# if __name__ == '__main__':
#     Base.metadata.create_all(engine)
#     faker = Factory.create()
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     print session.query(User).all()
#     faker_users = [User(
#         username=faker.name(),
#         password=faker.word(),
#         email=faker.email(),
#     ) for i in range(10)]
#     session.add_all(faker_users)
#
#     faker_categories = [Category(name=faker.word()) for i in range(5)]
#     session.add_all(faker_categories)
#
#     faker_tags = [Tag(name=faker.word()) for i in range(20)]
#     session.add_all(faker_tags)
#
#     for i in range(100):
#         article = Article(
#             title=faker.sentence(),
#             content=' '.join(faker.sentences(nb=random.randint(10, 20))),
#             author=random.choice(faker_users),
#             category=random.choice(faker_categories)
#         )
#         for tag in random.sample(faker_tags, random.randint(2, 5)):
#             article.tags.append(tag)
#         session.add(article)
#
#     session.commit()
#     print session.query(User).all()
# func = filter(lambda x: x[0] if x else x, 'xabcdef')
# print(func)
# # test = lambda x: True if x else False
# # print(test(1))

# import redis
# import random
#
# number = random.choice(range(0, 100))
# num = number * random.randint(1, 100)
# pool = redis.ConnectionPool(host='192.168.1.57')
# r = redis.Redis(connection_pool=pool)
# r.set('shanghai', 'beijing')
# print(r.get('shanghai'))
# r.mset(name='1', name1='2')
# r.set('n', number)
# for i in range(r.llen('name2')):
#     r.lpop(name='name2')
# r.lpush('name2', number, number * num, number * num)
# r.rpush('name2', number)
# print(r.lrange('name2', 0, 100))
# print(r.mget('name', 'name1', 'shanghai', 'n'))
# r.hmset('test', {'key': number})
# r.hmset('test', {'xinwei': num})
# print(r.hmget('test', 'key', 'xinwei'))


# import redis
# import MySQLdb
#
# pool = redis.ConnectionPool(host='192.168.1.57')
# r = redis.Redis(connection_pool=pool)
# mysql = MySQLdb.connect(host='192.168.1.57', user='trusme', passwd='6286280300', db='command')
# cur = mysql.cursor()
# cur.execute('select * from base')
# msg = cur.fetchall()
# r.lpush('base', list(msg))
# for i in r.lrange('base', 0, 100):
#     print(i,)

# import random
# import string
#
# from PIL import Image, ImageFont, ImageDraw, ImageFilter
#
# font_path = "msyh.ttf"
# number = 6
# size = (100, 30)
# bgcolor = (255, 255, 255)
# fontcolor = (0, 0, 255)
# linecolor = (255, 0, 0)
# draw_line = True

# line_number = 5
#
#

#
# def getNumber():
#     source = list(string.ascii_letters) + list(string.digits)
#     return "".join(random.sample(source, number))
#
#

# def getLine(draw, width, height):
#     begin = random.randint(0, width), random.randint(0, height)
#     end = random.randint(0, width), random.randint(0, height)
#     draw.line([begin, end], fill=linecolor)
#
#
# def getCode():
#     width, height = size
#     image = Image.new("RGBA", size, bgcolor)
#     font = ImageFont.truetype(font_path, 25)
#     draw = ImageDraw.Draw(image)
#     text = getNumber()
#     print(text)
#     font_width, font_height = font.getsize(text)
#     draw.text(((width - font_width) / 2, (height - font_height) / 2), text, font=font, fill=fontcolor)
#     if draw_line:
#         for i in range(line_number):
#             getLine(draw, width, height)
#
#     # image = image.transform((width + 20, height + 10), Image.AFFINE, (1, -0.3, 0, -0.1, 1, 0), Image.BILINEAR)
#     image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
#     image.save('idencode.png')
#     # image.show()
#
#
# if __name__ == '__main__':
#     getCode()

# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
功能：
    登录验证模块
详细说明：
    1.密码文件为passwd
    2.passwd未创建或丢失，会提示：密码文件不存在，建议重新注册！！
    3.未注册用户登录会提示：用户名不存在，请您先进行注册！
    4.已注册用户登录时，忘记密码，尝试3次后密码还不正确则退出验证，等一会儿则可以重新登录
    5.作为装饰器进行登录验证
"""
import json
import hashlib
import os

pwd = os.getcwd()
fileName = os.path.join(pwd, "passwd")


# 将明文密码通过md5进行加密,返回一个加密后的md5的值
def calc_md5(passwd):
    md5 = hashlib.md5("haliluya")
    md5.update(passwd)
    ret = md5.hexdigest()
    return ret


# 新用户注册模块
def register():
    # 判断密码文件passwd是否存在，存在则载入列表，不存在就重新创建一个空字典
    if os.path.exists(fileName):
        # 载入用户列表，数据结构为字典，k=userName,v=passwdMd5
        with open("passwd", "r+") as loadsFn:
            userDB = json.loads(loadsFn.read())
    else:
        userDB = {}
    # 让用户输入用户名
    userName = raw_input("姓名：")
    # 标志位：控制循环跳出
    flag = True
    while flag:
        # 用户注册时，需输入两次密码
        passwd1 = raw_input("密码：")
        passwd2 = raw_input("确认密码：")
        # 如果两次密码不一致，则不执行下一步，再次输入密码并进行确认
        if not passwd1 == passwd2:
            continue
        else:
            # 两次输入密码一致，标志位置为False，下次跳出循环
            flag = False
        # 调用calc_md5函数将明文密码转为对应的md5值，用于保存
        passwdMd5 = calc_md5(passwd1)
    # 将用户名与密码对应存入字典userDB中
    userDB[userName] = passwdMd5
    # 将用户名和密码存入文件
    with open(fileName, "w") as dumpFn:
        dumpFn.write(json.dumps(userDB))


# 用户登录验证,装饰器
def login(func):
    def decorater(*args, **kwargs):
        # 判断passwd文件是否存在，存在则载入userDB（用户：密码），否则就重新注册新的passwd文件并返回
        if os.path.exists(fileName):
            with open("passwd", "r+") as loadsFn:
                userDB = json.loads(loadsFn.read())
        else:
            print "密码文件不存在，建议重新注册！！"
            register()
            return

        name = raw_input("用户名：")
        # 用户名是否存在，存在就继续输入密码，不存在则进行注册
        if name in userDB.keys():
            flag = True
            counter = 0
            # 循环输入密码，密码正确，flag=False（下次直接跳出循环）并执行函数，密码错误则允许尝试3次，超过3次验证失败，退出验证
            while flag:
                passwd = raw_input("密码：")
                passwdMd5 = calc_md5(passwd)
                if passwdMd5 == userDB[name]:
                    flag = False
                    func(*args, **kwargs)
                elif counter > 2:
                    print "您已经尝试了3次，请过会儿再试！！"
                    return
                else:
                    counter += 1
        else:
            print "用户名不存在，请您先进行注册！"
            register()

    return decorater


if __name__ == "__main__":
    @login
    def hello():
        print "Hello world!"


    hello()
