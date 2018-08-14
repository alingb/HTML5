#!/usr/bin/env python
# _*_encoding:utf-8_*_
# TIME:2018/5/6:21:40
# NAME:reset_nginx.py


import os
import time


def searchHttpNumber():
    http_number = os.popen('netstat -na | find /C ":80"')
    if http_number:
        http_number = http_number.read()
        return http_number
    else:
        print("HTTP service is unopened")
        return False


def resetHttp():
    while 1:
        number = searchHttpNumber()
        if number:
            if int(number) > 3800:
                print("Nginx service will stop")
                time.sleep(1)
                os.system('taskkill /f /im nginx.exe ')
                print("Nginx service will start")
                time.sleep(1)
                os.system('start nginx')
            else:
                print("number of HTTP connetions: {}".format(number))
                time.sleep(3)
                continue
        else:
            print("start Nginx service")
            time.sleep(1)
            os.system('start nginx')


if __name__ == '__main__':
    resetHttp()
