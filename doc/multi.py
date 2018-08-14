#!/usr/bin/env python
# _*_enconding:utf-8_*_
# TIME:2018/5/23 14:09
# FILE:multi.py

import time
import paramiko
import threading
class Woker(threading.Thread):
    def __init__(self, ip):
        super(Woker, self).__init__()
        self.ip = ip
    def run(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(hostname=self.ip, password='admin123', username='root', timeout=1)
            print(self.ip)
        except Exception as e:
            pass
        finally:
            ssh.close()
if __name__ == '__main__':
    start_time = time.time()
    ip = ['192.168.1.{}'.format(i) for i in xrange(51, 250)]
    ret = []
    for i in ip:
        woke = Woker(i)
        ret.append(woke)
        woke.start()
    for i in ret:
        i.join()
    end_time = time.time()
    print(end_time - start_time)
