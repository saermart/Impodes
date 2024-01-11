#coding:utf-8

import time,math,hashlib

def get_as_cp():
    i = math.floor(int(time.time()))
    e = hex(i).upper().replace('0X','')
    t = hashlib.md5(bytes(str(i),'utf-8')).hexdigest().upper()
    if 8 != len(e):
        return {
            'as': "479BB4B7254C150",
            'cp': "7E0AC8874BB0985"
        }
    a = ''
    r = ''
    o = t[:5]
    n = t[-5:]
    for s in range(5):
        a += o[s] + e[s]
    for c in range(5):
        r += e[c + 3] + n[c]
    return {
        'as': "A1" + a + e[-3:],
        'cp': e[:3] + r + "E1"
    }

if __name__ == '__main__':
    print(get_as_cp())
