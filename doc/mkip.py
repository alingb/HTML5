#!/usr/bin/env python
# _*_enconding:utf-8_*_
# TIME:2018/5/23 9:03
# FILE:mkip.py

import time
import paramiko
import threading
def run(ip):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname=ip,  port=22, password='admin123', username='root', timeout=0.5)
        print(ip)
    except Exception as e:
        pass
    finally:
        ssh.close()
if __name__ == '__main__':
    start_time = time.time()
    ret = []
    for i in xrange(51, 250):
        woker = threading.Thread(target=run, args=('192.168.1.{}'.format(i),))
        ret.append(woker)
        woker.start()
    for woker in ret:
        woker.join()
    end_time = time.time()
    print(end_time - start_time)
