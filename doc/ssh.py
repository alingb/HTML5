#!/usr/bin/env python
import MySQLdb
import paramiko
import urllib2
import json
from multi import Pool


def mysqlConn(cmd):
    con = MySQLdb.Connect("192.168.6.120", "trusme", "6286280300", "cmdb")
    cur = con.cursor()
    cur.execute(cmd)
    msg = cur.fetchall()
    cur.close()
    con.close()
    return msg


def sshConn(ip, cmd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, 22, 'root', 'admin123', timeout=5)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    msg = stdout.read()
    ssh.close()
    return msg


def getIp():
    cmd = 'select * from cmdb.web_stat'
    data = mysqlConn(cmd)
    dic = {}
    for i in data:
        dic[i[1]] = (i[2:])
    msg = {}
    for k, v in dic.items():
        if v[1] != 'running' and 'OS off' not in v[1]:
            msg[k] = (v[0], v[2], v[3], v[4], v[1])
    return msg


def run(ip):
    cmd = 'nohup sh /usr/local/src/ptutest &>/dev/null &'
    sshConn(ip, cmd)


def stopTest(info):
    ip, data = info
    dic = {}
    cmd = 'nohup sh /usr/local/src/kill &>/dev/null &'
    sshConn(ip, cmd)
    dic['ip'] = ip
    dic['status'] = 'stop'
    dic['sn'] = data[0]
    dic['cpu'] = data[1]
    dic['mem'] = data[2]
    dic['hostname'] = data[3]
    return dic


def mysqlCheck(fn):
    dic = {}
    cmd = 'select * from web_group_stat'
    data = mysqlConn(cmd)
    for i in data:
        key, value = i[1], i[2]  # type: (object, object)
        cmd = 'select * from web_group where id = 1'
        name = mysqlConn(cmd)
        if name[0][1] == fn:
            cmd = 'select * from web_stat where id = %d' % value
            data = mysqlConn(cmd)
            for dat in data:
                dic[dat[1]] = (dat[2], dat[4], dat[5], dat[6])
    return dic


def check(info):
    dic = {}
    ip, data = info
    run_ip = getIp()
    if ip in run_ip:
        try:
            sshConn(ip, '')
        except Exception:
            dic['ip'] = ip
            dic['status'] = data[4]
            dic['sn'] = data[0]
            dic['cpu'] = data[1]
            dic['mem'] = data[2]
            dic['hostname'] = data[3]
            return dic
        cmd = 'ps aux|egrep "intel|cpuburn|ptugen"|grep -v grep|wc -l'
        number = sshConn(ip, cmd)
        dic['sn'] = data[0]
        dic['cpu'] = data[1]
        dic['mem'] = data[2]
        dic['hostname'] = data[3]
        dic['ip'] = ip
        if int(number) > 7:
            dic['status'] = 'running'
        else:
            dic['status'] = 'check'
            run(ip)
        return dic
    else:
        dic['ip'] = ip
        dic['status'] = data[4]
        dic['sn'] = data[0]
        dic['cpu'] = data[1]
        dic['mem'] = data[2]
        dic['hostname'] = data[3]
        return dic


def powerOff(info):
    ip, data = info
    dic = {}
    cmd = 'poweroff'
    sshConn(ip, cmd)
    dic['ip'] = ip
    dic['status'] = 'poweroff'
    dic['sn'] = data[0]
    dic['cpu'] = data[1]
    dic['mem'] = data[2]
    dic['hostname'] = data[3]
    return dic


def bmcClear(info):
    ip, data = info
    dic = {}
    cmd = '/usr/local/bin/ipmitool sel clear'
    sshConn(ip, cmd)
    dic['ip'] = ip
    dic['status'] = data[4]
    dic['sn'] = data[0]
    dic['cpu'] = data[1]
    dic['mem'] = data[2]
    dic['hostname'] = data[3]
    return dic


def execRun(info):
    ip, data = info
    dic = {}
    if float(data[1][:-1]) < 90:
        cmd = 'nohup sh /usr/local/src/ptutest &>/dev/null &'
        sshConn(ip, cmd)
    dic['ip'] = ip
    dic['status'] = data[4]
    dic['sn'] = data[0]
    dic['cpu'] = data[1]
    dic['mem'] = data[2]
    dic['hostname'] = data[3]
    return dic


def put(data):
    info = json.dumps(data)
    msg = urllib2.urlopen('http://192.168.6.120/status/', info)
    return msg


if __name__ == '__main__':
    paramiko.util.log_to_file("filename.log")
    pool = Pool(processes=20)
    ip = getIp()
    if ip:
        pool = Pool(processes=20)
        for i in ip.items():
            pool.apply_async(check, (i,), callback=put)
        pool.close()
        pool.join()

    running = {}
    if mysqlCheck('run'):
        pool = Pool(processes=20)
        running.update(mysqlCheck('run'))
        for i in running.items():
            pool.apply_async(execRun, (i,), callback=put)
        pool.close()
        pool.join()
    stop = {}
    if mysqlCheck('stop'):
        pool = Pool(processes=20)
        stop.update(mysqlCheck('stop'))
        for i in stop.items():
            pool.apply_async(stopTest, (i,), callback=put)
        pool.close()
        pool.join()

    poweroff = {}
    if mysqlCheck('poweroff'):
        pool = Pool(processes=20)
        poweroff.update(mysqlCheck('poweroff'))
        for i in poweroff.items():
            pool.apply_async(powerOff, (i,), callback=put)
        pool.close()
        pool.join()

    clear = {}
    if mysqlCheck('bmcLogClear'):
        pool = Pool(processes=20)
        poweroff.update(mysqlCheck('bmcLogClear'))
        for i in poweroff.items():
            pool.apply_async(bmcClear, (i,), callback=put)
        pool.close()
        pool.join()
