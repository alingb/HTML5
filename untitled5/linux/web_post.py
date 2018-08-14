#!/usr/bin/env python
# _*_enconding:utf-8_*_
# TIME:2018/7/30 10:13
# FILE:web_post.py

import requests
import json

data = {'/dev/sdl': {'status': 'OK', 'slot': '21', 'off': '0', 'UUID': 'ab17e250-d6c2-4ca4-94aa-5c4d26caeba3'}, '/dev/sdj': {'status': 'OK', 'slot': '17', 'off': '0', 'UUID': '02648200-ddb5-4d09-ad04-5fdf8a4b7d80'}, '/dev/sdk': {'status': 'OK', 'slot': '20', 'off': '0', 'UUID': '0bb8fff3-7883-41e8-bc9b-3e6a51a1398e'}, '/dev/sdh': {'status': 'OK', 'slot': '13', 'off':'0', 'UUID': '532a79ce-27e8-4d74-920e-1e509d99dea7'}, '/dev/sdi': {'status': 'OK', 'slot': '16', 'off': '0', 'UUID': 'ca217eaa-93e4-42a6-a121-04b957438689'}, '/dev/sdf': {'status': 'OK', 'slot': '9', 'off': '0', 'UUID': '513a56b8-51f2-45ef-bcfe-a288bad55de7'}, '/dev/sdg': {'status': 'OK', 'slot': '12', 'off': '0', 'UUID': 'fe2e8c01-8d61-4500-a3e2-cafca288adb6'}, '/dev/sdd': {'status': 'OK', 'slot': '5', 'off': '0', 'UUID': '454996b0-7bf3-47c2-b66b-4b34df0db6ee'}, '/dev/sde': {'status': 'OK', 'slot': '8', 'off': '0', 'UUID': 'ec1f464b-b4c6-41e6-8510-e288cfa95dbb'}, '/dev/sda': {'status': 'OK', 'slot': '1', 'off': '0', 'UUID': ''}}

url = "http://127.0.0.1:8000/index.heml"

requests.post(url, data=json.dumps(data))