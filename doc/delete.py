#!/usr/bin/env python

import MySQLdb
import paramiko
from multi import Pool
import json
import urllib2
import datetime


def mysqlConn(cmd):
    mysql_config = {
        'host': '192.168.6.120',
        'user': 'trusme',
        'password': '6286280300',
        'database': 'cmdb'
    }
    con = MySQLdb.connect(**mysql_config)
    cur = con.cursor()
    try:
        cur.execute(cmd)
        msg = cur.fetchall()
    except Exception:
        msg = ''
    finally:
        cur.close()
        con.close()
    return msg


def sshConn(ip):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, 22, 'root', 'admin123', timeout=5)
    except Exception:
        return False
    ssh.close()
    return True


def info():
    dic = {}
    cmd = 'select * from web_stat'
    data = mysqlConn(cmd)
    for i in data:
        cmd = 'select * from web_stat where id = {:d}'.format(i[0])
        data = mysqlConn(cmd)
        for dat in data:
            dic[dat[1]] = dat[2:]
    return dic


def serverInfo(sn, sn_1):
    cmd = 'select * from web_host where sn="{}"'.format(sn)
    data = mysqlConn(cmd)
    if data:
        num = len(data)
        if num == 1:
            data = data[0]
        else:
            cmd = 'select * from web_host where sn_1="{}"'.format(sn_1)
            func = lambda x: x[0] if x else False
            data = func(mysqlConn(cmd))
    else:
        cmd = 'select * from web_host where sn_1="{}"'.format(sn)
        data = mysqlConn(cmd)
        if data:
            num = len(data)
            if num == 1:
                data = data[0]
            else:
                cmd = 'select * from web_host where sn_1="{}"'.format(sn_1)
                func = lambda x: x[0] if x else False
                data = func(mysqlConn(cmd))
    if data:
        dic = {}
        dic['memory'] = data[0]
        dic['raid'] = data[1]
        dic['cpu'] = data[2]
        dic['disk_num'] = data[3]
        dic['sn'] = data[4]
        dic['sn_1'] = data[5]
        dic['time'] = data[7].strftime('%Y-%m-%d')
        dic['name'] = data[8]
        dic['family'] = data[9]
        dic['bios'] = data[10]
        dic['bmc'] = data[11]
        dic['message'] = data[12]
        dic['disk'] = data[13]
        dic['mac'] = data[14]
        dic['network'] = data[15]
        dic['sel'] = data[16]
        dic['fru'] = data[17]
        dic['hostname'] = data[18]
        if data[6] == 'pass':
            dic['status'] = 'complete'
        else:
            dic['status'] = data[6]
        dic['name1'] = data[20]
        if 'OS off' in data[19]:
            dic['stress_test'] = data[19]
        else:
            dic['stress_test'] = 'OS off %s' % datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        dic['mac_addr'] = data[21]
        dic['boot_time'] = data[22]
        dic['smart_info'] = data[24]
        dic['enclosure'] = data[25]
        dic['ip'] = data[26]
    return dic


def check(ip, info):
    sn, sn_1, error = '', '', {}
    sn = info[0].split(',')[0][1:].strip('\'')
    if len(info[0].split(',')) > 1:
        sn_1 = info[0].split(',')[1][:-1].strip('\'')
    if "]" in sn:
        sn = info[0][2:][:-2]
    try:
        sshConn(ip)
    except Exception:
        error['ip'] = ip
        error['sn'] = info[0]
        error['cpu'] = info[2]
        error['mem'] = info[3]
        error['hostname'] = info[4]
        if 'OS off' in info[1]:
            error['status'] = info[1]
        else:
            error.update({'status': 'OS off %s' % datetime.datetime.now().strftime('%Y-%m-%d %H:%M')})
    return ip, sn, sn_1, error


def checkMysqlMsgPut(ip, sn, sn_1, error):
    data = json.dumps(error)
    urllib2.urlopen('http://192.168.6.120/status/', data)
    data = serverInfo(sn, sn_1)
    info = json.dumps(data)
    urllib2.urlopen('http://192.168.6.120/web/collect/', info)


def deleteMysqlMsg(ip, sn, sn_1, error):
    cmd = 'select * from web_stat where ip="{}"'.format(ip)
    data = mysqlConn(cmd)
    id = data[0][0]
    cmd = 'delete from web_group_stat where stat_id="{}"'.format(id)
    try:
        mysqlConn(cmd)
    finally:
        cmd = 'delete from web_stat where ip="{}"'.format(ip)
        mysqlConn(cmd)
        data = serverInfo(sn, sn_1)
        info = json.dumps(data)
        msg = urllib2.urlopen('http://192.168.6.120/web/collect/', info)
        return msg


if __name__ == '__main__':
    data = info()
    import sys
    msg = sys.argv[1]
    if data:
        if msg == 'check':
            pool = Pool(processes=20)
            for ip, info in data.items():
                pool.apply_async(check, (ip, info,), callback=deleteMysqlMsg)
            pool.close()
            pool.join()
        elif msg == 'delete':
            pool = Pool(processes=20)
            for ip, info in data.items():
                pool.apply_async(check, (ip, info,), callback=checkMysqlMsgPut())
            pool.close()
            pool.join()
