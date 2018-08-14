#!/usr/bin/env python
# _*_ encoding: utf-8_*_
# import re
#
# from subprocess import PIPE, Popen
# INFO = Popen('ipconfig', stdout=PIPE, stderr=PIPE, shell=True)
# INFO = INFO.stdout.read()
# print(INFO)


# for A in range(1, 10):
#     for B in range(0, 10):
#         for C in range(0, 10):
#             for D in range(0, 10):
#                 if (1000 * A + 100 * B +10 * C + D ) * 9 == (1000 * D + 100 * C + 10 * B + A):
#                     print("{0}{1}{2}{3} * 9 = {3}{2}{1}{0}".format(A, B, C, D))
#
# """
#  -------------
#  | A | B | C |
#  -------------
#  | D | E | F |
#  -------------
#  | G | H | I |
#  -------------
# """
# number = [i for i in range(10)]
# for A in number:
#     a = number.copy()
#     a.remove(A)
#     for B in a:
#         b = a.copy()
#         b.remove(B)
#         for C in b:
#             c = b.copy()
#             c.remove(C)
#             for D in c:
#                 d = c.copy()
#                 d.remove(D)
#                 for E in d:
#                     e = d.copy()
#                     e.remove(E)
#                     for F in e:
#                         f = e.copy()
#                         f.remove(F)
#                         for G in f:
#                             g = f.copy()
#                             g.remove(G)
#                             for H in g:
#                                 h = g.copy()
#                                 h.remove(H)
#                                 for I in h:
#                                     if (A + B + C) == (A + D + G) == (D + E + F) == (G + H + I) == (C + F + I) == (
#                                             B + E + H) \
#                                             == (C + F + I) == (A + E + I) == (G + E + C):
#                                         print("""
# -------------
# | {0} | {1} | {2} |
# -------------
# | {3} | {4} | {5} |
# -------------
# | {6} | {7} | {8} |
# ------------- """.format(A, B, C, D, E, F, G, H, H, I))

# import datetime
# import time

# cpu, memory, bios = 0, '', ''
#
# list = [cpu, 'cpu_num', memory, 'memory_num', 'disk_num', 'ssd_num', bios, 'bmc']
#
# for i in range(len(list)):
#     list[i] = i
#     print(list[i])
# print(cpu)
# def test():
#     return 'a', 'b'
#
# a = test()
# print(a[0])
# import multiprocessing
#
#
# def worker(procnum, return_dict):
#     print(procnum)
#     return_dict.update({procnum: procnum})
#     print(return_dict)
#     return return_dict
#
#
# if __name__ == '__main__':
#     manager = multiprocessing.Manager()
#     return_dict = manager.dict()
#     jobs = []
#     for i in range(5):
#         p = multiprocessing.Process(target=worker, args=(i, return_dict))
#         jobs.append(p)
#         p.start()
#     for proc in jobs:
#         proc.join()
#     print return_dict
# import multiprocessing
# import time
#
#
# class Test(object):
#     def func(self):
#         print('i')
#         return {'msg': 'msg'}
#
#     def func1(self):
#         return {"msg1": "msg1"}
#
#     def func2(self):
#         return {"msg2": "msg2"}
#
#     def func3(self):
#         return {"msg3": "msg3"}
#
#     def run(self):
#         pool = multiprocessing.Pool(processes=4)
#         list = [self.func, self.func1, self.func2, self.func3]
#         result = []
#         for i in list:
#             result.append(pool.apply_async(i, ()))
#         pool.close()
#         pool.join()
#         for res in result:
#             print res.get()
#         print "Sub-process(es) done."
#
#
# if __name__ == "__main__":
#     Test().run()
#
# class test(object):
#     def __init__(self):
#         self.ret = []
#
#     def test1(self):
#         self.ret.append('test1')
#         print(self.ret)
#         return self.ret
#
#     def test2(self):
#         self.ret.append('test2')
#         print(self.ret)
#         return self.ret
#
#     def test3(self):
#         self.ret.append('test3')
#         print(self.ret)
#         return self.ret
#
#     def run(self):
#         ret = []
#         self.test1()
#         self.test2()
#         self.test3()
#         print("===")
#         return self.ret
#
#
# t = test()
# print(t.run())
# b = {'status': 'no'}
# a = {'status': [{'family': '1'}]}
# c = a.get('status')
# for k, v in c[0].items():
#     print(k, v)
# import PyMySQL
# print('1')
#
#
# def test():
#     return ''
#
#
# if test():
#     print('yes')


import datetime
import time
import itchat

def timeFun(sched_time):
    flag = 0
    while True:
        now = datetime.datetime.now()
        if sched_time < now < sched_time + datetime.timedelta(seconds=1):  # 因为时间秒之后的小数部分不一定相等，要标记一个范围判断
            send_move()
            time.sleep(1)  # 每次判断间隔1s，避免多次触发事件
            flag = 1
        else:
            # print('schedual time is {0}'.format(sched_time))
            # print('now is {0}'.format(now))
            if flag == 1:
                sched_time = sched_time + datetime.timedelta(hours=1)  # 把目标时间增加一个小时，一个小时后触发再次执行
                flag = 0


def send_move():
    # nickname = input('please input your firends\' nickname : ' )
    #   想给谁发信息，先查找到这个朋友,name后填微信备注即可,deepin测试成功
    # users = itchat.search_friends(name=nickname)
    users = itchat.search_friends(name='Kim')  # 使用备注名来查找实际用户名
    # 获取好友全部信息,返回一个列表,列表内是一个字典
    import pymysql
    conn = pymysql.connect(host="192.168.1.57", user="trusme", database="cmdb", password="6286280300")
    cur = conn.cursor()
    cmd = "select id,name,family from web_host order by id"
    cur.execute(cmd)
    data = cur.fetchall()
    # print(users)
    # 获取`UserName`,用于发送消息
    userName = users[0]['UserName']
    itchat.send(data, toUserName=userName)
    print('pass')


if __name__ == '__main__':
    itchat.auto_login(hotReload=True)  # 首次扫描登录后后续自动登录
    sched_time = datetime.datetime(2018, 4, 24, 16, 24, 00)  # 设定初次触发事件的事件点
    print('run the timer task at {0}'.format(sched_time))
    timeFun(sched_time)

