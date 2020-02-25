# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 18:14:28 2020

@author: zhang
"""

import requests
import json
import time
import re
import os

headers_raw="""Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,ja;q=0.8
Cache-Control: max-age=0
Connection: keep-alive
Cookie: _uuid=7C2EDDAA-B843-15E6-EFEE-DD0EA2F301B023443infoc; buvid3=E1815B06-1828-481F-BC84-498ABFD4F5EA155828infoc; LIVE_BUVID=AUTO4315670402248481; sid=lp8rpg6n; CURRENT_FNVAL=16; rpdid=|(J|)JkR|YR|0J'ulY~|R|k~u; UM_distinctid=16ce24c5cdd32-05def6882cc6ef-396a4605-1fa400-16ce24c5cde221; im_notify_type_1836737=0; stardustvideo=1; laboratory=1-1; INTVER=-1; pgv_pvi=9402613760; CURRENT_QUALITY=116; LIVE_PLAYER_TYPE=1; DedeUserID=1836737; DedeUserID__ckMd5=326caeb00bc9daa3; SESSDATA=68b4dc5a%2C1582691072%2C26581e11; bili_jct=c56310cc6de31f6e8728de07648983ec; flash_player_gray=false; html5_player_gray=false; bp_t_offset_1836737=359095747404222299; _dfcaptcha=d766283d73a7c658c29253faa4ab9077
Host: api.bilibili.com
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36"""

def get_headers(header_raw):
    return dict(line.split(": ", 1) for line in header_raw.split("\n"))
def get_url(url):
    while 1:
        try:
            r = requests.get(url,timeout = 10)
            return r
        except:
            time.sleep(1)
def get_stream(url):
    while 1:
        try:
            dheaders = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'}
            r = requests.get(url,headers=dheaders,timeout=10,stream=True)
            if r.status_code==200:
                return r
        except:
            pass
        print(r.status_code)
        time.sleep(1)
        
def getuids():
    f = open('/root/u/checked_fmid.txt')
    uids = f.read().splitlines()
    f.close()
    return uids
    
headers = get_headers(headers_raw)    
opath = input("路径：")
if not opath:
    opath = 'C:/Users/zhang/Desktop'
opath+='/bilidt'

rstr = r"[\/\\\:\*\?\"\<\>\|\- \n]"
uids = getuids()
if not os.path.exists('bilidt.txt'):
    f = open('bilidt.txt','w')
    f.close()
with open('bilidt.txt') as f:
    dtlist = f.read().splitlines()
for uid in uids:
    if uid in dtlist:
        print(uid,'跳过')
        continue
    url= 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?host_uid=10432972&offset_dynamic_id=0&need_top=1'
    while 1:
        name=''
        r = get_url(url)
        data=r.json()['data']
        r.close()
        hasmore = data['has_more']
        cards = data['cards']
        for i in cards:
            card_str = i['card']
            card = json.loads(card_str)
            if not name:
                try:
                    oname = card['owner']['name']
                except:
                    user = card['user']
                    if 'name' in user:
                        oname = user['name']
                    elif 'uname' in user:
                        oname = user['uname']
                    else:
                        print('昵称获取失败')
                        break
            name = re.sub(rstr,"_",oname)
            path = os.path.join(opath,name)
            if not os.path.exists(path):
                os.makedirs(path)
            try:
                item = card['item']
            except:
                continue
            try:
                description = item['description']
            except:
                description = item['content']
            if 'pictures' in item:
                pictures = item['pictures']
                upload_time = item['upload_time']
                ftime = time.strftime("%Y%m%d_%H%M%S",time.localtime(upload_time))
                print(f"\r\033[K{name}:({ftime})动态图片获取\n{description}")
                for pic in pictures:
                    img_src = pic['img_src']
                    filename = f"{name}-{ftime}-{img_src.split('/')[-1]}"
                    filepath = os.path.join(path,filename)
                    while 1:
                        try:
                            rr = get_stream(img_src)
                            with open(filepath,"wb") as f:
                                for chunk in rr.iter_content(chunk_size=8192):
                                    if chunk:
                                        f.write(chunk)
                            break
                        except:
                            rr.close()
                            time.sleep(0.5)
                    rr.close()
                    print(f"\r\033[K{filename}下载成功")
            if 'video_playurl' in item:
                upload_time=item['upload_time']
                ftime = time.strftime("%Y%m%d_%H%M%S",time.strptime(upload_time, "%Y-%m-%d %H:%M:%S"))
                print(f"\r\033[K{name}:({ftime})动态视频获取\n{description}")
                video_playurl = item['video_playurl']
                filename = f"{name}-{ftime}-{video_playurl.split('/')[-1].split('?')[0]}"
                filepath = os.path.join(path,filename)
                while 1:
                    try:
                        rr = get_stream(video_playurl)
                        with open(filepath,"wb") as f:
                            for chunk in rr.iter_content(chunk_size=8192):
                                if chunk:
                                    f.write(chunk)
                        break
                    except:
                        rr.close()
                        time.sleep(0.5)
                rr.close()
                print(f"\r\033[K{filename}下载成功")
        if hasmore:
            next_offset = data['next_offset']
            url = f'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?host_uid=10432972&offset_dynamic_id={next_offset}&need_top=1'
        else:
            break
    print(name,'动态下载完成')
    os.system(f"cd {path};mv * {opath}")
    f = open('bilidt.txt','a')
    f.write(f'{uid}\n')
    f.close()
