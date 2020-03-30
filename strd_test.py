import os,random,asyncio,traceback
import uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
os.system("cd /root/b/d/d;mv *flv /root/b;cd /root/b/d/huya;mv *mp4 /root/b")
import time
import re
import requests
import threading
import sys
import json
import toml
from mail import send_mail
tryy = input('test?')
password = input('password:')
proxies = {}
justone = 1
dRooms = []
hRooms = []
hrecording = []
drecording = []
dpath = None
status = []
ss = requests.session()
ss.keep_alive = False
islogin = 0
sended = 0

dcookies_raw = '''Hm_lpvt_e99aee90ec1b2106afe7ec3b199020a7=1582781071; Hm_lvt_e99aee90ec1b2106afe7ec3b199020a7=1582775420,1582779677; dy_did=b3eabab7bce9386ba96de9c600071501; acf_did=b3eabab7bce9386ba96de9c600071501; dy_auth=4a4cul%2FxmwaKex3A3V6MNXtJUB5k%2F5LZFL6C%2FsRP%2B3Zwj9YVc0vxFlfKPgC28yw9uLDr2iEO2QigHH4jq0x033Oh2bwCMsfy7IdvA3eDswMb4sG%2B2ZjYDAdxmezB; smidV2=20200227120001377cbf560207cfb17d37a526a0cda3b200eb03c6acf42a4c0; wan_auth37wan=b3e8e47148393416M%2F2CXWe%2Fc%2Bku3LqGKSjs11iozVaXEwS9E%2B7aT4uiHjxM084feIbqA%2B3CFASdUphbSg4rvoYatahnsmdu%2FowXclxBsc8bOl2q; acf_auth=6c7fgcAk9TOh%2B5MzcmV13%2FL04O0%2BkSr3oQ4E3HRmgqQxpE1QZvVxQfvrsNOj7Hre8jRurM3QDXRMeEMbFJa9Ruth8o0K5h8sRoMrkzgp%2BBRA4EvHBfXHrs8vNbzD; acf_avatar=https%3A%2F%2Fapic.douyucdn.cn%2Fupload%2Favatar%2F005%2F55%2F00%2F12_avatar_; acf_biz=1; acf_ct=0; acf_groupid=1; acf_ltkid=45649582; acf_nickname=Miloxin; acf_own_room=0; acf_phonestatus=1; acf_stk=741d2e29fed30476; acf_uid=5550012; acf_username=auto_7NcKZj9sbL; PHPSESSID=ov73opef8fn6edi9n5n6bb9r55'''

def get_cookies(cookie_raw):
    return dict(line.split("=", 1) for line in cookie_raw.split("; "))
dcookies = get_cookies(dcookies_raw)
def get_headers(header_raw):
    return dict(line.split(": ", 1) for line in header_raw.split("\n"))
    
def delete_proxy(proxy):
    return ss.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

def get_proxy():
    return requests.get("http://127.0.0.1:5010/get").json().get("proxy")
class Room():
    def __init__(self,nRoom=None,nDomain =None):
        self.nRoom = int(nRoom or 0)
        self.nDomain = nDomain
        self.thread = None
        self.sameid = 1
        self.ex = 0

class aerror(Exception):
    pass
    
    
def huyad(c,m):
    try:
        if m in hrecording:
            return
        else:
            hrecording.append(m)
        os.system('ykdl www.{}.com/{} -o /root/b/d/huya'.format(c,m))
    except:
        pass
    finally:
        if m in hrecording:
            hrecording.remove(m)
    
def youd(c,m):
    global dpath
    #while True:
    print('www.%s.com/%s -o %s' % (c,m,dpath))
    try:
        if m in drecording:
            return
        else:
            drecording.append(m)
        os.system('ykdl www.{}.com/{} -o {} -t 20'.format(c,m,dpath))
    except:
        pass
    finally:
        if m in drecording:
            drecording.remove(m)
     #   finally:
     #       time.sleep(20)
           
        
def huod(c,m):
   # while True:
    try:
        os.system('lulu www.{}.com/{} -o /root/b/d/d'.format(c,m))
    except:
        pass
   #     finally:
  #          time.sleep(20)

def upload():
    print('上传进程开始')
    while True:
        os.system('cd /root/b;bash do.sh')
        time.sleep(10)

def checkuser():
    global dRooms
    global hRooms
    while True:
        #print('check run')
        for i in open("duser.txt","r").read().splitlines():
            if(i):
                sameid = 0 
                for room in dRooms:
                    if(int(i) == room.nRoom):
                        sameid =1
                        room.ex = 1
                        #room.sameid = 1
                        break
                if(sameid == 1):
                    continue
                else:
                    print('find new id:%s.' % i)
                    room = Room(int(i),'douyu');
                    room.sameid = 1
                    room.ex = 1
                    #room.getInfo();
                    dRooms.append(room)
        for room in dRooms:
            if(room.ex == 0):
                print("{}end".format(room.nRoom))
                dRooms.remove(room)
                room.sameid = 0
            room.ex = 0
            
        for i in open("huser.txt","r").read().splitlines():
            if(i):
                sameid = 0 
                for room in hRooms:
                    if(int(i) == room.nRoom):
                        sameid =1
                        room.ex = 1
                        #room.sameid = 1
                        break
                if(sameid == 1):
                    continue
                else:
                    print('find new id:%s.' % i)
                    room = Room(int(i),'huya');
                    room.sameid = 1
                    room.ex = 1
                    #room.getInfo();
                    hRooms.append(room)
        for room in hRooms:
            if(room.ex == 0):
                print("{}end".format(room.nRoom))
                hRooms.remove(room)
                room.sameid = 0
            room.ex = 0
        time.sleep(5)

def gethtml(s,url):
    res = s.get(url,timeout=(5,6))
    data = res.json()
    res.close()
    return data
        
def huyastatus(hs,thread_pool=None):
    global islogin
    global sended
    check_url = 'http://i.huya.com/udb_web/udbport2.php?m=HuyaHome&do=checkLogin'
    searchurl = 'https://fw.huya.com/dispatch?do=subscribeList&uid=1199513272235&page=1&pageSize=1000'
    runtime = 1
    while 1:
        try:
            if runtime > 0:
                data = gethtml(hs,check_url)
                check = data['isLogined']
                runtime = -2
            if check:
                try:
                    rjson = gethtml(hs,searchurl)
                    if rjson.get('result'):
                        data = rjson['result']	
                        dlist = data['list']	
                        liveCount = data['liveCount']	
                        livecheck = 0
                        for i in dlist:	
                            if i['isLive']:	
                                livecheck+=1	
                                if i['profileRoom'] not in hrecording:	
                                    down = threading.Thread(target=huyad,args=('huya',i['profileRoom'],),name=str(i['nick']),daemon=True)
                                    down.start()
                                if livecheck>=liveCount:
                                    break
                    else:
                        print('huya no result',rjson)
                except:
                    check = 0
            else:
                sys.stdout.write(f"\r\033[K虎牙未登录")
                hcookies_raw = toml.load("/root/u/huya.conf")['hcookies_raw']
                hcookies=get_cookies(hcookies_raw)
                temp_s = requests.session()
                hs.cookies = temp_s.cookies
                hs.cookies.update(hcookies)
                f = open('huser.txt')
                namelist = f.read().splitlines()
                f.close()
                for name in namelist:
                    if name not in hrecording:
                        url = 'https://www.huya.com/'+name
                        try:
                            with hs.get(url,timeout=10) as r:
                                html = r.text
                                if '哎呀，虎牙君找不到这个主播' in html:
                                    print(name,'不存在')
                                else:
                                    isOn = re.findall(r'\"isOn\":(.+?),',html)[0]
                                    if isOn == 'true':
                                        if name not in hrecording:
                                            down = threading.Thread(target=huyad,args=('huya',name,),name=name+'record',daemon=True)
                                            down.start()
                        except:
                            traceback.print_exc()
                            islogin = 0
                            print(name,'出错')
            runtime+=1
        except Exception as e:
            print("huya Error:",e)
            traceback.print_exc()
        sys.stdout.write(f'\r\033[Khuyastatus')
        time.sleep(random.randint(5,10))

def douyustatus(ds,thread_pool=None):
    global dRooms
    global justone
    global dcookies
    #print('run')
    #url = 'https://www.douyu.com/wgapi/livenc/liveweb/followlist/0?sort=0&cid1=0'
    url = "https://www.douyu.com/wgapi/livenc/liveweb/follow/list?sort=0&cid1=0"
    cookies = requests.utils.dict_from_cookiejar(ds.cookies)
    with open("/root/u/dscookies.txt", "w") as fp:
        json.dump(cookies, fp)
    while 1:
        try:
            #json = await loop.run_in_executor(thread_pool,functools.partial(gethtml,ds,url))
            rjson = gethtml(ds,url)
            data = rjson['data']
            dlist = data['list']
            for i in dlist:
                if i['show_status'] == 1:
                    if i['room_id'] not in drecording:
                        print(f"开始下载{i['room_id']},{i['nickname']}")
                        down = threading.Thread(target=youd,args=('douyu',i['room_id'],),name=str(i['nickname']),daemon=True)
                        down.start()
        except Exception as e:
            if 'time' in str(e):
            	print('获取json超时,重试')
            	continue
            print("获取json失败",e)
            try:
                if tryy:
                    print('douyu开始重登录')
                #dcookies = {"Cookie": "dy_did=8242408a3b65feb390623d6c00081501; smidV2=2019051418520294dca99b6773cfe1c2a03077977c1b0d007f7dac9e8893840; acf_did=8242408a3b65feb390623d6c00081501; PHPSESSID=tgvun5c1ci6c3ltnt7s1okkgc4; acf_auth=a3ecVlfGOE71GvSS26fxTjpC0g2rpMvwCuyrPEAy%2BfoWUaTL6sDxmROq3AFY3NzP5hPaMctHzoVucMxtZwx1I2vjdCExw7r7IzfyTMh8VGMldrKDfVhJVfseCuuM; wan_auth37wan=e055eff5b144Id8mxDNxZ5PDOrybYQkr8CSHWmP92V%2FtpUNgjRRfcXeR4YInW2os3cNzjH04cZNauAFh9dyNkHcfE1HV%2FKP64R05tCA8uXzxrIZz; acf_uid=5550012; acf_username=auto_7NcKZj9sbL; acf_nickname=Miloxin; acf_own_room=0; acf_groupid=1; acf_phonestatus=1; acf_avatar=https%3A%2F%2Fapic.douyucdn.cn%2Fupload%2Favatar%2F005%2F55%2F00%2F12_avatar_; acf_ct=0; acf_ltkid=45649574; acf_biz=1; acf_stk=68f690a62d404465; Hm_lvt_e99aee90ec1b2106afe7ec3b199020a7=1569768125,1569768354,1570418236,1570418291; Hm_lpvt_e99aee90ec1b2106afe7ec3b199020a7=1570418291; LTP0=f59ad3EDaPuUGY1EQxElM%2BObWmUwxNR09ZsFcIg980X5xWYI3rNT6FiIYMerOsRDHPowpPivNRJ7vPzLQY4mHZHRMlJ5u0nk87P8NcX6xcwgEdL1Ygb8EpANCS6wWAQ4BFfimXYD5ZNNsyjdaGE4xoyb%2BNzKKLB3kiIeEhjpwM2zWlOz2NjBBMMx1m3VRJ7AQuKGk"}
                #dcookies = {"cookie":"Hm_lpvt_e99aee90ec1b2106afe7ec3b199020a7=1582781071; Hm_lvt_e99aee90ec1b2106afe7ec3b199020a7=1582775420,1582779677; dy_did=b3eabab7bce9386ba96de9c600071501; acf_did=b3eabab7bce9386ba96de9c600071501; dy_auth=4a4cul%2FxmwaKex3A3V6MNXtJUB5k%2F5LZFL6C%2FsRP%2B3Zwj9YVc0vxFlfKPgC28yw9uLDr2iEO2QigHH4jq0x033Oh2bwCMsfy7IdvA3eDswMb4sG%2B2ZjYDAdxmezB; smidV2=20200227120001377cbf560207cfb17d37a526a0cda3b200eb03c6acf42a4c0; wan_auth37wan=b3e8e47148393416M%2F2CXWe%2Fc%2Bku3LqGKSjs11iozVaXEwS9E%2B7aT4uiHjxM084feIbqA%2B3CFASdUphbSg4rvoYatahnsmdu%2FowXclxBsc8bOl2q; acf_auth=6c7fgcAk9TOh%2B5MzcmV13%2FL04O0%2BkSr3oQ4E3HRmgqQxpE1QZvVxQfvrsNOj7Hre8jRurM3QDXRMeEMbFJa9Ruth8o0K5h8sRoMrkzgp%2BBRA4EvHBfXHrs8vNbzD; acf_avatar=https%3A%2F%2Fapic.douyucdn.cn%2Fupload%2Favatar%2F005%2F55%2F00%2F12_avatar_; acf_biz=1; acf_ct=0; acf_groupid=1; acf_ltkid=45649582; acf_nickname=Miloxin; acf_own_room=0; acf_phonestatus=1; acf_stk=741d2e29fed30476; acf_uid=5550012; acf_username=auto_7NcKZj9sbL; PHPSESSID=ov73opef8fn6edi9n5n6bb9r55; LTP0=19a2f2nryMtCpWOL6pDrO%2Fm37T6NLODoRXAYpRxJLNdou63Swu%2B1by5BsUKnX%2Fs8BrrmduuGLyX0VEwaysZo1lO7twpphl1AIFAOPTPLRnZQ%2BbtuCNDhvew4ZsZodHVGuWZuFGJyJpa9ThhFFFg%2BaLMXKj96Qmma2yml9%2Brjq4%2BdNVD5lZ9sc%2B97WLweNaiyRqSOs;"}
                dcookies['LTP0'] = '19a2f2nryMtCpWOL6pDrO%2Fm37T6NLODoRXAYpRxJLNdou63Swu%2B1by5BsUKnX%2Fs8BrrmduuGLyX0VEwaysZo1lO7twpphl1AIFAOPTPLRnZQ%2BbtuCNDhvew4ZsZodHVGuWZuFGJyJpa9ThhFFFg%2BaLMXKj96Qmma2yml9%2Brjq4%2BdNVD5lZ9sc%2B97WLweNaiyRqSOs'
                s = requests.session()
                s.keep_alive=False
                #print(rjson)
                #headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36","Referer":"https://www.douyu.com/directory/myFollow"}
                headers=ds.headers
                lurl = 'https://passport.douyu.com/lapi/passport/iframe/safeAuth?client_id=1&t={t}&_={t}'.format(t=int(time.time()*1000))
                res = requests.get(lurl,headers=headers,cookies=dcookies,allow_redirects=False)
                if res.headers.get('Set-Cookie'):
                    #dcookies={"Cookie":"{}".format(dcookies['Cookie'].split("LTP0")[0]+res.headers['Set-Cookie'])}
                    dcookies['LTP0'] =res.headers['Set-Cookie'].split('=')[-1]
                if tryy:
                    print(dcookies)
                if res.headers.get('Location'):
                    llurl = 'https:'+res.headers['Location']
                    #s.cookies.update(dcookies)
                    res = s.get(llurl,headers=headers,cookies=dcookies,allow_redirects=False)
                    cookies = requests.utils.dict_from_cookiejar(s.cookies)
                    for cookie in cookies:
                        dcookies[cookie] = cookies[cookie]
                    print('登录后cookies',dcookies)
                    ds.cookies.update(dcookies)
                    if tryy:
                        print(res.headers)
                    #douyustatus(ds)
                elif '过期' in str(json):
                    subject = '斗鱼出错'
                    contents = '斗鱼登录过期'
                    send_mail(subject,contents,password)
                    time.sleep(20)
                cookies = requests.utils.dict_from_cookiejar(ds.cookies)
                with open("/root/u/dscookies.txt", "w") as fp:
                    json.dump(cookies, fp)
                
            except Exception as e:
                print(e)
        #if "douyu" in status:
        #   status.remove("douyu")
        
        sys.stdout.write("\r\033[Kdouyustatus")
        time.sleep(random.randint(0,5))

def main():
    global justone
    global dRooms
    global dpath
    global hRooms
    ms = []
    datas = []
    dRooms = []
    datas=input('输入平台 room：').split(' ')
    b = len(datas)
    for i in range(b):
        if datas[i].isalpha():
            ms = datas[i+1].split(',')

            if datas[i]=='d':
                dpath=datas[i+1]
                if (not os.path.exists(dpath)):
                    os.makedirs(dpath)
            i+=1
    dheaders_raw='''accept: application/json, text/plain, */*
x-dy-traceid: 4ccba279366641e3:4ccba279366641e3:0:008828
accept-language: zh-cn
x-requested-with: XMLHttpRequest
user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Safari/605.1.15
referer: https://www.douyu.com/directory/myFollow
accept-encoding: gzip, deflate'''
    dheaders=get_headers(dheaders_raw)
    ds = requests.session()
    ds.headers.update(dheaders)
    ds.cookies.update(dcookies)
    hheaders={
            "Connection":"close",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            "Accept":"*/*",
            "Referer":"https://i.huya.com/",
            "Accept-Encoding":"gzip, deflate, br",
            "Accept-Language":"zh-CN,zh;q=0.9,ja;q=0.8"}
    hcookies_raw = toml.load("/root/u/huya.conf")['hcookies_raw']
    hcookies=get_cookies(hcookies_raw)
    hs = requests.session()
    hs.headers.update(hheaders)
    hs.cookies.update(hcookies)
    if tryy:
        if tryy =='d':
            douyustatus(ds)
        elif tryy =='h':
            huyastatus(hs)
        sys.exit(1)
    while True:
        if 'douyu' not in status:
            status.append("douyu")
            douyu_status = threading.Thread(target=douyustatus,args=(ds,),name='douyustatus',daemon=True)
            douyu_status.start()
        if 'huya' not in status:
            status.append("huya")
            huya_status = threading.Thread(target=huyastatus,args=(hs,),name='huyastatus',daemon=True)
            huya_status.start()
        sys.stdout.write("\r\033[Kupdate") 
        time.sleep(random.randint(0,5))
    
if __name__ =="__main__":
    main()

