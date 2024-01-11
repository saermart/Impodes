#coding:utf-8

import requests
import urllib.parse
import execjs
import hmac
import json
import base64
import time
import copy
from hashlib import sha1
from zheye import zheye
from requests_toolbelt.multipart.encoder import MultipartEncoder

HOMEPAGE = 'https://www.zhihu.com/signin?next=%2F'
UDID = 'https://www.zhihu.com/udid'
CAPTCHA = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=cn'
LOGIN = 'https://www.zhihu.com/api/v3/oauth/sign_in'

JS_FILE = 'encrypt.js'
CAPTCHA_IMG = 'captcha.jpg'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
}

def get_signature(ts):
    a = hmac.new(b'd1b964811afb40118a12068ff74a12f4',digestmod=sha1)
    a.update(b'password')
    a.update(b'c3cef7c66a1843f8b3a9e6a1e3160e20')
    a.update(b'com.zhihu.web')
    a.update(str(ts).encode('utf-8'))
    signature = a.hexdigest()
    return signature

def exec_js_func(js_file,func,*params):
    with open(js_file,'r') as f:
        lines = f.readlines()
    js = ''.join(lines)
    js_context = execjs.compile(js)
    result = js_context.call(func,*params)
    return result

class Zhihu:

    def __init__(self,username,password):
        self.username = username
        self.password = password
        self.session = requests.session()
        self.ocr = zheye.zheye()
        self.captcha = ''
        self.get_cookies()

    def get_cookies(self):
        self.session.get(HOMEPAGE,headers=HEADERS)
        self.session.post(UDID,headers=HEADERS)

    def check_captcha(self):
        response = self.session.get(CAPTCHA,headers=HEADERS)
        ret = response.json()
        if ret.get('show_captcha'):
            print('获取验证码.')
            res = self.session.put(CAPTCHA,headers=HEADERS)
            img_base64 = res.json()['img_base64']
            with open(CAPTCHA_IMG,'wb') as f:
                f.write(base64.b64decode(img_base64))
            positions = self.ocr.Recognize(CAPTCHA_IMG)
            real_points = [[i[1] / 2, i[0] / 2] for i in positions]
            points = {"img_size":[200,44],"input_points":real_points}
            payload = MultipartEncoder(
                fields={
                    'input_text':json.dumps(points)
                }
            )
            headers = copy.deepcopy(HEADERS)
            headers.update({
                'content-type':payload.content_type
            })
            result = self.session.post(CAPTCHA,headers=headers,data=payload)
            _ret = result.json()
            if _ret.get('success'):
                print('验证码验证成功')
                self.captcha = str(points)
                return
            else:
                print('验证码验证失败.')
                self.check_captcha()
        else:
            print('无需验证码~')


    def login(self):
        self.check_captcha()
        timestamp = int(time.time()*1000)
        data = {
            'client_id': 'c3cef7c66a1843f8b3a9e6a1e3160e20',
            'grant_type': 'password',
            'timestamp':str(timestamp) ,
            'source': 'com.zhihu.web',
            'signature': get_signature(timestamp),
            'username': self.username,
            'password': self.password,
            'captcha': self.captcha,
            'lang': 'cn',
            'utm_source': '',
            'ref_source': 'other_https://www.zhihu.com/signin?next'
        }
        HEADERS.update({
            'x-zse-83': '3_2.0',
            'content-type': 'application/x-www-form-urlencoded',
        })
        paylaod = urllib.parse.urlencode(data)
        enrypted_data = exec_js_func(JS_FILE,'b',paylaod)
        print(enrypted_data)
        response = self.session.post(LOGIN,headers=HEADERS,data=enrypted_data)
        print(response.status_code)
        print(response.text)
        print(response.cookies)


if __name__ == '__main__':
    bot = Zhihu('+639664706948','test2020')
    bot.login()