import requests
import os
import time
import sys
import shutil
import json
from threading import Thread as Th
#from requests.cookies import RequestsCookieJar

def get_headers(header_raw):
    return dict(line.split(": ", 1) for line in header_raw.split("\n"))

def change(i,nick_name=None):
    uid = i['uid']
    if uid in uidlist:
        nick_name2 = nick_name = i['nick_name']
    else:
        nick_name2 = i['nick_name']
        if os.path.exists(f'/home/milo4/b/pic/{nick_name2}'):
            files = os.listdir(f'/home/milo4/b/pic/{nick_name2}')
            if files:
                for file in files:
                    newfile = nick_name+'-'+file.split('-')[-1]
                    print(f'\r\033[K移动{file}到{nick_name}/{newfile}')
                    os.system(f'cd /home/milo4/b/pic/{nick_name2};mv "{file}" /home/milo4/b/pic/{nick_name}/{newfile}')
            files = os.listdir(f'/home/milo4/b/pic/{nick_name2}')
            if not files:
                print(f'\r\033[K{nick_name2}文件夹空，删除')
                os.system(f'rm -rf /home/milo4/b/pic/{nick_name2}')

def download(i,nick_name=None):
    feed_id = i['feed_id_str']
    uid = i['safe_uid']
    if uid in uidlist:
        nick_name2 = nick_name = i['nick_name']
        if not uid in nicklist:
            nicklist[uid] = nick_name
    else:
        nick_name2 = i['nick_name']
    imglist = i['imglist']
    source_id = i['source_id']
    if source_id:
        source_feed = i['source_feed']
        if source_feed:
            download(source_feed,nick_name)    
    if feed_id in piclist:
        sys.stdout.write(f'\r\033[K{feed_id}跳过')
        return feed_id
    #video = i['video']
    path = '/root/b/d/pic/{}'.format(nick_name)
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        files = os.listdir(path)
        if files:
            os.system('cd {};mv * /root/b/d/pic'.format(path))
    while imglist:
        iurl = imglist.pop()['url']
        if '.1440x0' in iurl:
            part = iurl.split('.1440x0')
            newurl = part[0].split('_forb')[0]+part[-1]
            name = nick_name+'-'+part[0].split('/')[-1]+part[-1].split('?')[0]
        elif '.0x1440' in iurl:
            part = iurl.split('.0x1440')
            newurl = part[0].split('_forb')[0]+part[-1]
            name = nick_name+'-'+part[0].split('/')[-1]+part[-1].split('?')[0]
        else:
            newurl =iurl
            name =nick_name+'-'+iurl.split('/')[-1].split('?')[0]
        if nick_name == nick_name2:
            print('\r\033[K下载',name)
        else:
            print(f'\r\033[K下载{nick_name}的粉丝{nick_name2}',name)
        filepath = os.path.join(path,name)
        f = open(filepath,'wb')
        with requests.get(newurl,stream = True) as r:
            for chunk in r.iter_content(chunk_size = 1024):
                if chunk:
                    f.write(chunk)
                    f.flush
        f.close()
        try:
            shutil.move(filepath,'/root/b/d/pic')
        except Exception as e:
            print('\r\033[K',e)
            #os.system(f'mv "{filepath}" /root/b/d/pic')
    f2.write(feed_id)
    f2.write('\n')
    piclist.append(feed_id)
    return feed_id

def maxdl():
    while 1:
        while uidlist2:
            uid = uidlist2.pop(0)
            nick_name = nicklist[uid]
            print('\r\033[K深度下载',uid)
            page = 1
            #url = f'https://mapi-yuba.douyu.com/wb/v3/user/feedlist?page={page}&pagesize=20&uid={uid}&v=1'
            url = f'https://yuba.douyu.com/wbapi/web/user/feedlist?page={page}&pagesize=20&uid={uid}'
            #headers = {"Accept": "application/vnd.mapi-yuba.douyu.com.4.0+json","Accept-Encoding": "gzip, deflate, br","Accept-Language": "zh-Hans-MO;q=1","Connection": "keep-alive","Content-Type": "application/x-www-form-urlencoded","Cookie": "acf_did=29ffb0d2ff4681c4f2b6583b00001521","Host": "mapi-yuba.douyu.com","Token": "5550012_11_474a1bf958ff19d4_2_45649578","User-Agent": "DYZB/6.030 (iPhone; iOS 13.3; Scale/2.00)","auth": "125a9c627b2399d49d5a5db653678f0e","client": "ios","dy-app-aname": "","dy-app-pname": "tv.douyu.live","dy-device-devtype": "0","dy-device-h": "667","dy-device-id": "29ffb0d2ff4681c4f2b6583b00001521","dy-device-idfa": "1924B11C-5A94-45C2-874C-C5F82E0CB028","dy-device-mac": "020000000000","dy-device-model": "iPhone 8 (A1905)","dy-device-nt": "1","dy-device-op": "2","dy-device-w": "375","phone_model": "iPhone10,4","phone_system": "13.3","timestamp": "1580200646","version": "603","x-dy-traceid": "23dc046c790480d5:23dc046c790480d5:0:018508",}
            while 1:
                print('\r\033[K',page)
                r = requests.get(url,headers=headers)#,cookies=cookies)
                data = r.json()['data']
                pages = data['totalPage']
                dlist = data['list']
                for i in dlist:
                    if ischange == 'y':
                        change(i,nick_name)
                    else:
                        download(i,nick_name)
                if page < pages:
                    page+=1
                    #url = f'https://mapi-yuba.douyu.com/wb/v3/user/feedlist?page={page}&pagesize=20&uid={uid}&v=1'
                    url = f'https://yuba.douyu.com/wbapi/web/user/feedlist?page={page}&pagesize=20&uid={uid}'
                else:
                    break
        time.sleep(5)
def get_cookies():
    with open("/root/u/dscookies.txt", "r") as fp:
        cookies = json.load(fp)
    lurl = 'https://passport.douyu.com/lapi/passport/iframe/safeAuth?callback=jQuery11130874597182652241_1582781156133&client_id=5&did=&t=1582781157458&_=1582781156134'
    s = requests.session()
    r = s.get(lurl,headers=headers,cookies=cookies,timeout=10)
    scookies = requests.utils.dict_from_cookiejar(s.cookies)
    r.close()
    for cookie in scookies:
        cookies[cookie] = scookies[cookie]
    return cookies

ctime = int(input('循环时间：'))
ischange = input('是否转移文件？y/n\n')
uidlist = []
uidlist2 = []
nicklist = {}
#ourl = 'https://mapi-yuba.douyu.com/wb/v3/followfeed?last_id='
ourl = 'https://yuba.douyu.com/wbapi/web/followfeed?last_id='
num = '0'
url = ourl+str(num)
#headers={"Accept": "application/vnd.mapi-yuba.douyu.com.4.0+json","Accept-Encoding": "gzip, deflate","Accept-Language": "zh-Hans-MO;q=1","Connection": "keep-alive","Content-Type": "application/x-www-form-urlencoded","Cookie": "acf_did=29ffb0d2ff4681c4f2b6583b00001521","Host": "mapi-yuba.douyu.com","Token": "5550012_11_6c9e16f31162c9d6_2_45649578","User-Agent": "DYZB/6.030 (iPhone; iOS 13.3.1; Scale/2.00)","auth": "ea4f9837c485e484fed710f9f2c7f83b","client": "ios","dy-app-aname": "","dy-app-pname": "tv.douyu.live","dy-device-devtype": "0","dy-device-h": "667","dy-device-id": "29ffb0d2ff4681c4f2b6583b00001521","dy-device-idfa": "1924B11C-5A94-45C2-874C-C5F82E0CB028","dy-device-mac": "020000000000","dy-device-model": "iPhone 8 (A1905)","dy-device-nt": "1","dy-device-op": "2","dy-device-w": "375","phone_model": "iPhone10,4","phone_system": "13.3.1","timestamp": "1582603682","version": "603","x-dy-traceid": "6a021a76dfbb38f5:6a021a76dfbb38f5:0:018404",}
headers_raw='''accept: */*
accept-encoding: gzip, deflate, br
user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Safari/605.1.15
accept-language: zh-cn
referer: https://yuba.douyu.com/homepage/main'''
headers = get_headers(headers_raw)
cookies= get_cookies()
hasmore=True
runmax = 1
ah = Th(target=maxdl,daemon = True)
ah.start()
while hasmore:
    sys.stdout.write('\r\033[K'+num)
    try:
        r = requests.get(url,headers=headers,cookies=cookies,timeout=10)
        data = r.json()['data']
    except Exception as e:
        print('\r\033[K',e)
        time.sleep(5)
        cookies= get_cookies()
        continue
    unreadnum = data['unreadnum']
    hasmore = data['hasMore']
    dlist = data['list']
    #i = dlist[1]
    if not os.path.exists('/root/u/dypic.txt'):
        ff=open('/root/u/dypic.txt','w')
        ff.close()
    f2 = open('/root/u/dypic.txt','a+')
    piclist = open('/root/u/dypic.txt').read().splitlines()
    for i in dlist:  
        uid = i['safe_uid']
        if uid not in uidlist:
            uidlist.append(uid)
            uidlist2.append(uid)
        feed_id = download(i)     
    if hasmore:
        num=feed_id
        url = ourl+str(num)
    else:
        print('end\033[A')
        num='0'
        url = ourl+str(num)
        hasmore=True
        if ctime:
            time.sleep(ctime)
        else:
            time.sleep(10)
        
