#coding:utf-8

import requests
from sign import get_signed_api

def get_user_articles(uid,max_behot_time=0):
    url = get_signed_api(uid,max_behot_time)
    headers = {
        'cookie':'tt_scid=CONST',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
    }
    response = requests.get(url,headers=headers,allow_redirects=False)
    next_url = response.headers['Location']
    ret = requests.get(next_url, headers=headers,)
    print(ret.json())


if __name__ == '__main__':
    uid = 5954781019
    get_user_articles(uid,1592119458)