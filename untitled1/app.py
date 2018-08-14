#!/usr/bin/env python
# _*_enconding:utf-8_*_
# TIME:2018/5/21 10:04
# FILE:app.py
import codecs

import qrcode


img = qrcode.make("http://trusme.imwork.net:82/technology/web/Host/detail/4035/")
print()

with codecs.open('test.png', 'r') as img:
    print(img)


