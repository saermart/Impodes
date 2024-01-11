#coding:utf-8

import requests
from sign import *

def get_user_followings(uid,cursor=0):
    headers = {
        'cookie': 'tt_scid=CONST',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
    }
    api = get_relation_api(uid,cursor=cursor)
    response = requests.get(api,headers=headers)
    print(response.json())

def get_user_fans(uid,cursor=0):
    headers = {
        'cookie': 'tt_scid=CONST',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
    }
    api = get_relation_api(uid,cursor=cursor,api=FANS_API)
    response = requests.get(api,headers=headers)
    print(response.json())

if __name__ == '__main__':
    uid = 5954781019
    get_user_fans(uid)