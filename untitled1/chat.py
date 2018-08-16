#!/usr/bin/env python
# _*_enconding:utf-8_*_
# TIME:2018/4/24 17:10
# FILE:chat.py


import requests
import itchat
import random
import pymysql

KEY = '04f44290d4cf462aae8ac563ea7aac16'
HELP = "帮助信息:\n" \
       "老化数量(正在老化的机器的数量)\n" \
       "老化状态(老化机器的运行状态)\n" \
       "老化压力(老化机器的cpu、memory使用率)\n" \
       "已老化机器数量（已老化机器的数量）"

robots = ['——By机器人小杨', '——By机器人白杨', '——By反正不是本人']

WECHA_NAME = '永远'

INPUT_MSG = {'hostname,status': '老化状态', "count(*)": '老化数量', "hostname,cpu,mem": '老化压力'}


class MysqlData(object):
    def __init__(self):
        self.base = None
        self.mysql_conf = {
            'host': '192.168.1.57',
            'user': 'trusme',
            'password': '6286280300',
            'database': 'command'
        }

    def mysqlConn(self):
        conn = pymysql.connect(**self.mysql_conf)
        return conn

    def getConne(self):
        if not self.base:
            self.base = self.mysqlConn()
        else:
            print(self.base)
        return self.base


def get_response(msg):
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key': KEY,
        'info': msg,
        'userid': 'wechat-robot',
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        return r.get('text')
    except Exception as e:
        return e


@itchat.msg_register(itchat.content.TEXT)
def tuling_reply(msg):
    ret_msg = ''
    defaultReply = 'I received: ' + msg['Text']
    reply = "没有机器在老化" + random.choice(robots)
    for key, value in INPUT_MSG.items():
        if msg['Text'] == value:
            conn = MysqlData().getConne()
            cur = conn.cursor()
            cur.execute('select {} from web_stat'.format(key))
            cur.execute('select {} from web_stat'.format(key))
            sql_msg = cur.fetchall()
            cur.close()
            conn.close()
            ret_msg = ''
            for ret in sql_msg:
                ret_msg += str(ret) + '\n'
            if ret_msg:
                return ret_msg
        elif msg['Text'] == '帮助' or msg["Text"] == 'help':
            return HELP
        else:
            return HELP
    if not ret_msg:
        return reply or defaultReply


@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def text_reply(msg):
    if msg['isAt']:
        ret_msg = ''
        re_msg = msg["Text"].split(WECHA_NAME)[1].strip()
        reply = get_response(msg['Text']) + random.choice(robots)
        for key, value in INPUT_MSG.items():
            if re_msg == value:
                conn = MysqlData().getConne()
                cur = conn.cursor()
                cur.execute('select {} from web_stat'.format(key))
                sql_msg = cur.fetchall()
                cur.close()
                conn.close()
                ret_msg = ''
                for ret in sql_msg:
                    ret_msg += str(ret) + '\n'
                if ret_msg:
                    itchat.send(u'@%s\u2005: %s' % (msg['ActualNickName'], ret_msg), msg['FromUserName'])
        if re_msg == '帮助' or ret_msg == 'help':
            itchat.send(u'@%s\u2005: %s' % (msg['ActualNickName'], HELP), msg['FromUserName'])
        elif not ret_msg:
            itchat.send(u'@%s\u2005: %s' % (msg['ActualNickName'], reply), msg['FromUserName'])


if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    itchat.run()
