import requests
from threading import Thread
import time
import os
import re
import shutil
import sys
import random
names = []
#url = 'https://webcast3-c.amemv.com/webcast/feed/?content_type=1&channel_id=37&version_code=8.8.0&pass-region=0&pass-route=0&js_sdk_version=1.32.1.0&webcast_sdk_version=1290&app_name=aweme&vid=D15D9459-8743-4CF5-968F-6A11A8EC5007&app_version=8.8.0&language=zh-Hans-CN&device_id=70047599612&channel=App%20Store&mcc_mnc=46001&aid=1128&effect_sdk_version=5.6.0&screen_width=375&openudid=e567d40a4e127e37e6c3212e5b44fd7cf0ebc60e&webcast_language=zh&os_api=18&ac=WIFI&os_version=13.3&webcast_locale=zh-Hans_CN&device_platform=iphone&build_number=88016&iid=93859058229&device_type=iPhone%208&idfa=1924B11C-5A94-45C2-874C-C5F82E0CB028&req_from=follow_live_skylight&action=refresh'
url = 'https://aweme.snssdk.com/aweme/v1/life/feed/?version_code=7.9.0&pass-region=1&pass-route=1&js_sdk_version=1.17.2.0&app_name=aweme&vid=399BCB11-BD3E-448A-8516-38E0C57BCC77&app_version=7.9.0&device_id=52100380665&channel=App%20Store&mcc_mnc=46001&aid=1128&screen_width=750&openudid=4d099f1840e190e9fe10224fcb657786a5c5ad70&os_api=18&ac=WIFI&os_version=12.4&device_platform=iphone&build_number=79025&device_type=iPhone10,4&iid=85477742411&idfa=1C721462-0A8F-4200-A60B-8A83373F5493&count=20&tab_type=2&cursor=0'
headers = {'x-Tt-Token': '00672d32b33297376720525b359fa480a56d0c1c4faa770ba298360f3af9e6efe6ed991c8e480162cdca840568ab23f0df18', 'sdk-version': '1', 'User-Agent': 'Aweme 8.8.0 rv",88016 (iPhone; iOS 13.3; zh_CN) Cronet', 'X-SS-DP': '1128', 'x-tt-trace-id': '00-0da39fe60a104f298bfcb57ab2390468-0da39fe60a104f29-01', 'Accept-Encoding': 'gzip, deflate', 'gzip, deflate': 'odin_tt=8678207ebdaab8fa7ca4498ba7403c3f7f3343df8bea47ccccd5d8a1907493954ac1c09bd8da59032a7761fbe0398724; d_ticket=532d4d53f7a7dde42caa683682efa31d3ebe8; msh=BcgAeBSrDJ-1SKaRh5dwL2yR7uE; sid_guard=672d32b33297376720525b359fa480a5%7C1576420921%7C5184000%7CThu%2C+13-Feb-2020+14%3A42%3A01+GMT; uid_tt=4d791e92ad3b9d9defff60015cc5a38a; sid_tt=672d32b33297376720525b359fa480a5; sessionid=672d32b33297376720525b359fa480a5; install_id=93859058229; ttreq=1$0ae16b1cc86d8a5582ed0521ffe9e2a244f1cbc0', 'X-Khronos': '1576481823', 'X-Gorgon': '830000002001ed51ef619456680e00155b86e3f3142c0ae331f2'}#{"x-Tt-Token":"009eb6296810343ae341cb7841294dabcad389438632df3ac5d994b75eca174b3ef10c25b328e36dc06be51d9cb0b604fc1a","sdk-version":"1","User-Agent":"Aweme 7.9.0 rv","x-tt-trace-id":"00-29feca87f033b1aa8144163a3366e0e4-29feca87f033b1aa-01","Accept-Encoding":"gzip, deflate","Cookie":"sid_guard=9eb6296810343ae341cb7841294dabca%7C1567870522%7C5184000%7CWed%2C+06-Nov-2019+15%3A35%3A22+GMT; uid_tt=b58f6ed0f43b1e3f100f44d55b36d672; sid_tt=9eb6296810343ae341cb7841294dabca; sessionid=9eb6296810343ae341cb7841294dabca; odin_tt=42f64d634c20908096376178a33edbc139450b81995e83eea22255b6b1f154da54bd9b1153717dfda3cb734f25dc4b9f; install_id=85477742411; ttreq=1$10179bfdd42fe841ad94af1bed38bbc1ef93ed34","X-Khronos":"1568269877","X-Gorgon":"830099902001e24feb1a2ca41a8de732caf9abbc62fa0ab4d63a"}
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
        #room_list = data.get('data')
        for sroom in room_list:
            nickname = sroom['owner']['nickname']
            #nickname = sroom['data']['owner']['nickname']
            rstr = r"[\/\\\:\*\?\"\<\>\|\- ]"
            nickname = re.sub(rstr,"_",nickname)
            if not nickname in names:
                names.append(nickname)
                a = room(nickname,sroom['stream_url']['rtmp_pull_url'])
                #a = room(nickname,sroom['data']['stream_url']['rtmp_pull_url'])
                s = Thread(target=download,args=(a,),name=(nickname))
                s.start()
    except Exception as e:
        print(e)
    time.sleep(random.randint(0,10))




