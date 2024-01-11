#coding:utf-8
import os
from as_cp import get_as_cp

ARTICLE_API = "https://www.toutiao.com/toutiao/c/user/article/?page_type=1&user_id={uid}&max_behot_time={mbt}&count=20&as={_as}&cp={_cp}"
FOLLOWING_API = "https://www.toutiao.com/toutiao/c/user/following/?user_id={uid}&cursor={cursor}&count=20"
FANS_API = "https://www.toutiao.com/toutiao/c/user/followed/?user_id={uid}&cursor={cursor}&count=20"

def get_signed_api(uid,behot_time=0):
    ascp = get_as_cp()
    _as = ascp['as']
    _cp = ascp['cp']
    api = ARTICLE_API.format(
        uid=uid,
        mbt=behot_time,
        _as=_as,
        _cp=_cp
    )
    ret = os.popen('node sign.js "' + api + '"')
    sign = ret.readlines()[0].strip()
    url = f'{api}&_signature={sign}'
    return url

def get_relation_api(uid,cursor=0,api=FOLLOWING_API):
    url = api.format(
        uid=uid,
        cursor=cursor,
    )
    ret = os.popen('node sign.js "' + url + '"')
    sign = ret.readlines()[0].strip()
    url = f'{url}&_signature={sign}'
    return url


if __name__ == '__main__':
    get_signed_api('5954781019')