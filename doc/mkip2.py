#!/usr/bin/env python
# _*_enconding:utf-8_*_
# TIME:2018/5/23 9:26
# FILE:mkip2.py

import paramiko
import time
import multiprocessing
def run(ip):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname=ip, password='admin123', username='root', timeout=1)
        print(ip)
    except Exception as e:
        pass
if __name__ == '__main__':
    start_time = time.time()
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    for i in xrange(51, 250):
        pool.apply_async(run, ('192.168.1.{}'.format(i),))
    pool.close()
    pool.join()
    end_time = time.time()
    print(end_time - start_time)

    # start_time = time.time()
    # pool = multiprocessing.Pool(multiprocessing.cpu_count())
    # for i in xrange(51, 250):
    #     pool.apply(run, ('192.168.1.{}'.format(i),))
    # pool.close()
    # pool.join()
    # end_time = time.time()
    # print(end_time - start_time)