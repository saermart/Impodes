

import requests


url = 'https://www.toutiao.com/a6839822740380189187/'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
    'cookie':'__ac_nonce=05eec31d100bd8de8f75a; __ac_signature=_02B4Z6wo00f012H4tKwAAIBAeKZSmhJUS2Nh-bAAAIaae1',
}

ret = requests.get(url,headers=headers)

print(ret.text)