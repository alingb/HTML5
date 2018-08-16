#!/usr/bin/env python
# _*_conding:utf-8_*_
# TIME:2018/5/29 14:03
# FILE:chat_for_stree.py

import datetime
import json
import re
# import urllib2

import itchat
import pymysql
import pyqrcode as pyqrcode
# import qrcode as qrcode
from itchat.content import *
from PIL import Image
import qrcode
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')


HELP = "帮助信息:（输入对应数字查询信息）\n" \
       "输入help显示此信息\n" \
       "1.老化信息(老化机器运行信息)\n" \
       "2.老化状态(老化机器的运行状态)\n" \
       "3.老化压力(老化机器的cpu、memory使用率)\n" \
       "4.老化机器数量(正在老化的机器数量)\n" \
       "5.关机时间（老化机器的关机时间）\n" \
       "6.运行时间（老化机器是现在老化的时间）\n" \
       "7.BMC日志（老化机器的bmc日志信息）\n" \
       "8.已老化数量(已老化机器的数量)\n" \
       "9.查询xxx的配件信息\n" \
       "10.查询订单信息"

WECHA_NAME = '永远'

ERROE_MSG = "没有正在老化的机器"


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


def checkMsg(msg):
    ret_msg = ''
    if len(msg) > 1:
        for i in msg:
            ret_msg += str(i) + "\n"
    elif len(msg) == 1:
        ret_msg = msg[0]
    if not ret_msg:
        ret_msg = ''
    return ret_msg


def getReceiveMsg(msg, cur, get_msg):
    if get_msg == "1":
        cur.execute("select num,sn,cpu,mem,status from web_stat order by num")
        sql_msg = cur.fetchall()
        send_msg = checkMsg(sql_msg)
        if send_msg:
            msg.user.send(u"{}.老化信息:\n"
                          u"(编号，[sn, sn1]，cpu使用率，内存使用率，运行状态)\n"
                          u"{}".format(get_msg, send_msg))
        else:
            msg.user.send(ERROE_MSG)
    elif get_msg == "2":
        cur.execute("select num,status from web_stat order by num")
        sql_msg = cur.fetchall()
        send_msg = checkMsg(sql_msg)
        if send_msg:
            msg.user.send(u"{}.老化状态:\n"
                          u"编号，运行状态\n"
                          u"{}".format(get_msg, send_msg))
        else:
            msg.user.send(ERROE_MSG)
    elif get_msg == "3":
        cur.execute("select num,cpu,mem from web_stat order by num")
        sql_msg = cur.fetchall()
        send_msg = checkMsg(sql_msg)
        if send_msg:
            msg.user.send(u"{}.老化压力:\n"
                          u"编号，cpu使用率，内存使用率\n"
                          u"{}".format(get_msg, send_msg))
        else:
            msg.user.send(ERROE_MSG)
    elif get_msg == "4":
        cur.execute("select count(id) from web_stat where status='running'")
        sql_msg = cur.fetchone()[0]
        msg.user.send(u"{}.老化机器数量:{} pcs（running）".format(get_msg, sql_msg))
    elif get_msg == "5":
        cur.execute("select sn from web_stat order by num")
        sql_msg = cur.fetchall()
        send_msg = ''
        for msg_list in sql_msg:
            sn, sn_1 = eval(msg_list[0])[0].strip(), eval(msg_list[0])[1].strip()
            try:
                cmd = "select message from web_host where sn='{0}' and sn_1='{1}'".format(sn, sn_1)
                cur.execute(cmd)
                host_msg = cur.fetchall()[0][0]
            except Exception as e:
                send_msg += "({0},{1},{2})\n".format(sn, sn_1, e)
                continue
            off_time = re.search(r"POWER:\s+(.*)", host_msg).group(1)
            send_msg += "{0} 关机时间为:\n{1}\n".format(sn, off_time)
        if send_msg:
            msg.user.send("{}.关机时间:\n{}".format(get_msg, send_msg))
        else:
            msg.user.send(ERROE_MSG)
    elif get_msg == "6":
        cur.execute("select sn from web_stat order by num")
        sql_msg = cur.fetchall()
        send_msg = ''
        for msg_list in sql_msg:
            sn, sn_1 = eval(msg_list[0])[0].strip(), eval(msg_list[0])[1].strip()
            try:
                cur.execute("select message from web_host where sn='{0}' and sn_1='{1}'".format(sn, sn_1))
                host_msg = cur.fetchall()[0][0]
            except Exception as e:
                send_msg += "({0},{1},{2})\n".format(sn, sn_1, e)
                continue
            boot_time = re.search(r"BOOT TIME:\s+(.*)", host_msg).group(1)
            now = datetime.datetime.now()
            boot_time = datetime.datetime.strptime(boot_time, "%Y-%m-%d %H:%M")
            run_time = now - boot_time
            run_time = str(run_time).split('.')[0]
            send_msg += "{0} 运行了:\n{1}\n".format(sn, run_time)
        if send_msg:
            msg.user.send("{}.运行时间:\n{}".format(get_msg, send_msg))
        else:
            msg.user.send(ERROE_MSG)
    elif get_msg == "8":
        cur.execute("select count(id) from web_host")
        sql_msg = cur.fetchone()[0]
        msg.user.send(u"{}.已老化数量:{} pcs".format(get_msg, sql_msg))
    elif get_msg == "7":
        cur.execute("select sn from web_stat order by num")
        sql_msg = cur.fetchall()
        send_msg = ''
        if sql_msg:
            for msg_list in sql_msg:
                sn, sn_1 = eval(msg_list[0])[0].strip(), eval(msg_list[0])[1].strip()
                try:
                    cur.execute("select sel from web_host where sn='{0}' and sn_1='{1}'".format(sn, sn_1))
                    host_msg = cur.fetchall()[0][0]
                except Exception:
                    send_msg += "{} 日志信息:\n{}\n".format(sn, "未查询到信息")
                    continue
                if host_msg:
                    send_msg = "{} 日志信息:\n{}\n".format(sn, host_msg)
                else:
                    send_msg = "没有日志信息"
                msg.user.send("{}.BMC日志:\n{}".format(get_msg, send_msg))
        else:
            msg.user.send(ERROE_MSG)
    elif get_msg == "9":
        global snReply, num
        snReply = True
        if num == 0:
            msg.user.send("请输入SN，或者输入exit退出sn查询")
            num = 1
    elif get_msg == "10":
        global makeImage, autoMake
        makeImage = True
        if not autoMake:
            msg.user.send("请输入订单号，或者输入exit退出查询")
            autoMake = True
    elif get_msg == "help":
        return HELP
    else:
        return "请输入help获取帮助"
    cur.close()


def snSeatch(msg, cur, get_msg):
    global snReply, num
    if get_msg == "exit":
        snReply = False
        num = 0
    elif get_msg == "help":
        msg.user.send("请输入sn进行查询，或者输入exit推出sn查询")
    else:
        sn = get_msg
        cmd = "select id from web_host where sn='{}'".format(sn)
        cur.execute(cmd)
        sql_msg = cur.fetchall()
        send_msg = checkMsg(sql_msg)
        if send_msg:
            send_msg = send_msg[0]
            image_name = "{}.png".format(send_msg)
            img = qrcode.make("http://trusme.imwork.net:82/technology/web/Host/detail/{}/".format(send_msg))
            img.save(image_name)
            itchat.send_image(image_name, toUserName=msg.user.UserName)
        else:
            send_msg = "查询不到这个SN"
            msg.user.send(u"{}".format(send_msg))


def imageGet(msg, cur, get_msg):
    global makeImage, autoMake
    if get_msg == "exit":
        makeImage = False
        autoMake = False
    elif get_msg == "help":
        msg.user.send("请输入订单好（MAxxxx）进行查询，或者输入exit退出查询")
    else:
        cur.execute("select name from web_product where name='{}'".format(get_msg))
        data = cur.fetchall()
        if data:
            image_name = "{}.png".format(get_msg)
            img = qrcode.make("http://trusme.imwork.net:82/web/detail/admin/")
            img.save(image_name)
            itchat.send_image(image_name, toUserName=msg.user.UserName)
        else:
            msg.user.send(u"没有这个单号")


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    global autoReply, snReply
    conn = MysqlData().getConne()
    cur = conn.cursor()
    get_msg = msg["Text"]
    if get_msg == "开启回复":
        autoReply = True
    elif get_msg == "关闭回复":
        autoReply = False
    if autoReply:
        if snReply:
            snSeatch(msg, cur, get_msg)
        elif makeImage:
            imageGet(msg, cur, get_msg)
        else:
            ret = getReceiveMsg(msg, cur, get_msg)
            if ret:
                conn.commit()
                conn.close()
                return ret
            conn.commit()
            conn.close()


@itchat.msg_register(['Picture', 'Recording', 'Attachment', 'Video'])
def download_files(msg):
    sn_list = []
    with open(msg['FileName'], 'rb') as f:
        for fd in f.read().split():
            sn_list.append(fd)
    data = json.dumps({msg.FileName: sn_list})
    urllib2.urlopen('http://192.168.1.57/product', data)


@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    if msg.isAt:
        global snReply
        conn = MysqlData().getConne()
        cur = conn.cursor()
        get_msg = msg["Text"].split(WECHA_NAME)[1].strip()
        if snReply:
            snSeatch(msg, cur, get_msg)
        else:
            ret = getReceiveMsg(msg, cur, get_msg)
            if ret:
                conn.commit()
                conn.close()
                return ret
            conn.commit()
            conn.close()


if __name__ == '__main__':
    itchat.auto_login(enableCmdQR=2, hotReload=True)
    autoReply, snReply, num, makeImage, autoMake = False, False, 0, False, False
    itchat.run()
    print("well done")