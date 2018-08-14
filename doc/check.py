#!/usr/bin/env python

import MySQLdb
import paramiko
from multi import Pool
import json
import urllib, urllib2
import datetime


def serverInfo(sn, sn_1):
    con = MySQLdb.connect('192.168.6.120', 'trusme', '6286280300', 'cmdb')
    cur = con.cursor()
    cur.execute('select * from web_host where sn="%s"' % sn)
    data = cur.fetchall()
    if data:
        num = len(data)
        if num == 1:
            data = data[0]
        else:
            cur.execute('select * from web_host where sn_1="%s"' % sn_1)
            data = cur.fetchall()[0]
    else:
        cur.execute('select * from web_host where sn_1="%s"' % sn)
        data = cur.fetchall()
        if data:
            num = len(data)
            if num == 1:
                data = data[0]
            else:
                cur.execute('select * from web_host where sn_1="%s"' % sn_1)
                data = cur.fetchall()[0]
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


def info():
    dic = {}
    con = MySQLdb.connect('192.168.6.120', 'trusme', '6286280300', 'cmdb')
    cur = con.cursor()
    cur.execute('select * from web_stat')
    data = cur.fetchall()
    with open('/usr/local/src/ip.log', 'wb') as fd:
        for i in data:
            k, v = i[1], i[2]
            cur.execute('select * from web_stat where id = %d' % i[0])
            data = cur.fetchall()
            for dat in data:
                dic[dat[1]] = dat[2:]
                fd.write(dat[1] + '\n')
    return dic


def check(ip, info):
    sn_1 = ''
    sn = info[0].split(',')[0][1:].strip('\'')
    if len(info[0].split(',')) > 1:
        sn_1 = info[0].split(',')[1][1:][:-1].strip('\'')
    if "]" in sn:
        sn = info[0][2:][:-2]
    erro = {}
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, 22, 'root', 'admin123', timeout=8)
    except:
        erro['ip'] = ip
        erro['sn'] = info[0]
        erro['cpu'] = info[2]
        erro['mem'] = info[3]
        erro['hostname'] = info[4]
        if 'OS off' in info[1]:
            erro['status'] = info[1]
        else:
            erro.update({'status': 'OS off %s' % datetime.datetime.now().strftime('%Y-%m-%d %H:%M')})
    ssh.close()
    if erro:
        data = json.dumps(erro)
        urllib2.urlopen('http://192.168.6.120/status/', data)
        data = serverInfo(sn, sn_1)
        info = json.dumps(data)
        urllib2.urlopen('http://192.168.6.120/web/collect/', info)


if __name__ == '__main__':
    data = info()
    if data:
        pool = Pool(processes=20)
        for ip, info in data.items():
            pool.apply_async(check, (ip, info,))
        pool.close()
        pool.join()
