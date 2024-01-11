#coding:utf-8

import re
import os
import requests
import execjs
from w3lib import url as wurl
from bs4 import BeautifulSoup as bs

HOST = 'http://www.dm5.com'
ROOT = '漫画'

def safe_string(_string):
    return re.sub('[:,.\'&%$@!~*；‘：&……%￥#]','_',_string)

def get_comic_list():
    api = 'http://www.dm5.com/dm5.ashx?'
    headers = {'User-Agent': 'okhttp/3.8.0'}
    current_page = 1
    while 1:
        print(f'------------------>Index :{current_page}')
        data = {
            'pagesize': '68',
            'pageindex': current_page,
            'tagid': '0',
            'areaid': '0',
            'status': '0',
            'usergroup': '0',
            'pay': '-1',
            'char': '',
            'sort': '10',
            'action': 'getclasscomics'
        }

        response = requests.post(api,
                        data=data,
                        headers=headers)
        result = response.json()
        UpdateComicItems = result['UpdateComicItems']
        if not UpdateComicItems:
            return
        for i in UpdateComicItems:
            comic_url = f'{HOST}/{i["UrlKey"]}'
            comic_name = i['Title']
            try:
                download_comic(comic_url,comic_name)
            except Exception as e:
                print(f'<{comic_name}> 章节调整 中,链接：{comic_url}')
        current_page+=1


def download_comic(comic_url,comic_name,*args,**kwargs)->None:
    _path_1 = os.sep.join([ROOT,safe_string(comic_name)])
    if not os.path.exists(_path_1):
        os.makedirs(_path_1)
    response = requests.get(comic_url)
    dom = bs(response.text,'lxml')
    div = dom('div',id='chapterlistload')[0]
    li_list = div.ul('li')
    print(f'--> 开始下载漫画《{comic_name}》')
    for li in li_list:
        chapter_url = f'{HOST}{li.a["href"]}'
        chapter_name = re.sub('[ ]','',li.text)
        try:
            download_chapter(chapter_url,chapter_name,_path_1)
        except Exception as e:
            print(f'章节<{chapter_name}> 下载出错：{e}')

def download_chapter(chapter_url,chapter_name,path,*args,**kwargs)->None:
    _path_2 = os.sep.join([path,chapter_name])
    if not os.path.exists(_path_2):
        os.makedirs(_path_2)
    response = requests.get(chapter_url)
    text = response.text
    cid = re.findall('var DM5_CID=(.+?);',text)[0].strip()
    mid = re.findall('var DM5_MID=(.+?);',text)[0].strip()
    dt = re.findall('var DM5_VIEWSIGN_DT="(.+?)";',text)[0].strip()
    sign = re.findall('var DM5_VIEWSIGN="(.+?)";',text)[0].strip()
    page_count = int(re.findall('var DM5_IMAGE_COUNT=(.+?);',text)[0].strip())
    page = 1
    while page <= page_count:
        js_api = f'{chapter_url}chapterfun.ashx?cid={cid}&page={page}&key=&language=1&gtk=6&_cid={cid}&_mid={mid}&_dt={dt}&_sign={sign}'
        headers = {
            'referer':HOST
        }
        ret = requests.get(js_api,headers=headers)
        js_code = ret.text
        image_urls = execjs.eval(js_code)
        img_url = image_urls[0]
        img_name = wurl.parse_url(img_url).path.split('/')[-1]
        try:
            download_picture(img_url,img_name,_path_2)
        except Exception as e:
            print(f'章节 <{chapter_name}> 图片 {img_name} 下载失败：{e}')
        page+=1
    print(f'章节 《{chapter_name}》 下载成功！')

def download_picture(img_url,img_name,path,*args,**kwargs)->None:
    save_path  = os.sep.join([path,img_name])
    if os.path.exists(save_path):
        return
    response = requests.get(img_url)
    with open(save_path,'wb') as f:
        f.write(response.content)
        print(f'<{img_name}> 下载成功~')



if __name__ == '__main__':
    get_comic_list()