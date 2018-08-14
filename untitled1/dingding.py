#!/usr/bin/env python
# TIME:2018/4/23 15:24
# _*_ encoding:utf-8 _*_
# FILE:dingding.py
from dingtalkchatbot.chatbot import DingtalkChatbot

if __name__ == '__main__':
    import pymysql
    conn = pymysql.connect(host="192.168.1.57", user="trusme", database="cmdb", password="6286280300")
    cur = conn.cursor()
    cmd = "select id,name from web_host order by id limit 1"
    cur.execute(cmd)
    data = cur.fetchall()
    msg = ''
    for i in data:
        msg += "{} 红包 ".format(i[1])
    print(msg)
    webhook = 'https://oapi.dingtalk.com/robot/send?access_token=6756c78eda73a873ed2c168b1d9736ceddb70bc739253b87303f12c99f5b3af3'
    xiaoding = DingtalkChatbot(webhook)
    at_mobiles = [13560190720]
    # xiaoding.send_text(msg=msg, is_at_all=True)
    xiaoding.send_text(msg=msg, at_mobiles=at_mobiles)
