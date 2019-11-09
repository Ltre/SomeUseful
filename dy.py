import requests
from threading import Thread
import time
import os
import re
import shutil
import sys
import random
names = []
url = 'https://aweme.snssdk.com/aweme/v1/life/feed/?version_code=7.9.0&pass-region=1&pass-route=1&js_sdk_version=1.17.2.0&app_name=aweme&vid=399BCB11-BD3E-448A-8516-38E0C57BCC77&app_version=7.9.0&device_id=52100380665&channel=App%20Store&mcc_mnc=46001&aid=1128&screen_width=750&openudid=4d099f1840e190e9fe10224fcb657786a5c5ad70&os_api=18&ac=WIFI&os_version=12.4&device_platform=iphone&build_number=79025&device_type=iPhone10,4&iid=85477742411&idfa=1C721462-0A8F-4200-A60B-8A83373F5493&count=20&tab_type=2&cursor=0'
headers = {"x-Tt-Token":"009eb6296810343ae341cb7841294dabcad389438632df3ac5d994b75eca174b3ef10c25b328e36dc06be51d9cb0b604fc1a","sdk-version":"1","User-Agent":"Aweme 7.9.0 rv","x-tt-trace-id":"00-29feca87f033b1aa8144163a3366e0e4-29feca87f033b1aa-01","Accept-Encoding":"gzip, deflate","Cookie":"sid_guard=9eb6296810343ae341cb7841294dabca%7C1567870522%7C5184000%7CWed%2C+06-Nov-2019+15%3A35%3A22+GMT; uid_tt=b58f6ed0f43b1e3f100f44d55b36d672; sid_tt=9eb6296810343ae341cb7841294dabca; sessionid=9eb6296810343ae341cb7841294dabca; odin_tt=42f64d634c20908096376178a33edbc139450b81995e83eea22255b6b1f154da54bd9b1153717dfda3cb734f25dc4b9f; install_id=85477742411; ttreq=1$10179bfdd42fe841ad94af1bed38bbc1ef93ed34","X-Khronos":"1568269877","X-Gorgon":"830099902001e24feb1a2ca41a8de732caf9abbc62fa0ab4d63a"}
if not os.path.exists('/root/b/d/dy'):
    os.makedirs('/root/b/d/dy')
else:
    os.system('cd /root/b/d/dy;mv *flv /root/b/d/bu')
class room():
    def __init__(self,nickname,url):
        self.nickname = nickname
        self.url = url
def download(room):
    filename = '{}-{}-_.flv'.format(time.strftime('%y%m%d_%H%M%S'),room.nickname)
    filepath = '/root/b/d/dy/'+filename
    f = open(filepath,'wb')
    try:
        r = requests.get(room.url,stream = True,timeout = 10)
        filesize = 0
        for chunk in r.iter_content(chunk_size = 1024*8):
            if chunk:
                filesize+=f.write(chunk)
                if filesize%(1024*512)==0:
                    sys.stdout.write('\r\033[K{}  {}M'.format(filename,filesize/(1024*1024)))
                if filesize/(1024*1024) >= 1024:
                    f.close()
                    shutil.move(filepath,'/root/b/d/bu/bt')
                    filename = '{}-{}-_.flv'.format(time.strftime('%y%m%d_%H%M%S'),room.nickname)
                    filepath = '/root/b/d/dy/'+filename
                    f = open(filepath,'wb')
    except Exception as e:
        print(e)
    finally:
        names.remove(room.nickname)
        if 'r' in locals():
            r.close()
        f.close()
        if (os.path.isfile(filepath) and os.path.getsize(filepath) < 1024*1024):
            os.remove(filepath);
        else:
            if os.path.isfile(filepath):
                shutil.move(filepath,'/root/b/d/bu/bt')
while True:
    try:
        r = requests.get(url,headers= headers,timeout = 10)
        data = r.json()
        r.close()
        room_list = data.get('room_list')
        for sroom in room_list:
            nickname = sroom['owner']['nickname']
            rstr = r"[\/\\\:\*\?\"\<\>\|\- ]"
            nickname = re.sub(rstr,"_",nickname)
            if not nickname in names:
                names.append(nickname)
                a = room(nickname,sroom['stream_url']['rtmp_pull_url'])
                s = Thread(target=download,args=(a,),name=(sroom['owner']['nickname']))
                s.start()
    except Exception as e:
        print(e)
    time.sleep(random.randint(2,5))




