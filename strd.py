import os,random,functools,concurrent,uvloop,asyncio
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
os.system("cd /root/b/d/d;mv *flv /root/b;cd /root/b/d/huya;mv *mp4 /root/b")
import time
import re
import requests
import threading
import sys
import nest_asyncio
from mail import send_mail
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
dcookies = {"Cookie": "dy_did=8242408a3b65feb390623d6c00081501; smidV2=2019051418520294dca99b6773cfe1c2a03077977c1b0d007f7dac9e8893840; _dys_refer_action_code=init_page_author; Hm_lvt_e99aee90ec1b2106afe7ec3b199020a7=1565337319,1565345238,1565399909,1565402312; acf_auth=8098pNG6AjBMqfcS7TrkfX1dIKjpp6tT2kXdLka2ulVhCI%2BAruOEfMJ4Zpw6OVp2Pg2FpbL94ZTQzLxUhxCcQ0v08fp0uUnb6hVu75kGUUUA8yqaDDK0zMsmPAIW; wan_auth37wan=ad6d52926d1dGrpl5zqSwjb%2FLECNu1bdNqsNKPbIvAHpUDD4rNRgjZM8P1NFkubgW8qKTarSS68805tkxZ6EYboo3yWe5W%2FP822Op0BbDEJKtbJh; acf_uid=5550012; acf_username=auto_7NcKZj9sbL; acf_nickname=Miloxin; acf_own_room=0; acf_groupid=1; acf_phonestatus=1; acf_ct=0; acf_ltkid=46925293; acf_biz=1; acf_stk=a44a3deba8913c64; acf_did=8242408a3b65feb390623d6c00081501; LTP0=e2a80bQ27D8KOPuMC5Srmv%2BTxqRuLwfxlwiQKAA4ewn8CpS0pxkXMSdZgDFV6O0dwR%2FOChGNxyhAY1LV%2Fj%2FxPDm9cHmHQB8mhzSbykqF%2B6TYJOECK81CJb%2FkzuyTkGKeyL5dOxmk2L8aAPqHkVjEq5U0drFRQiQvw7mRcakxdoGeb7NR4Ter6jPNI0I6RgjRY%2FV9k;"}

def delete_proxy(proxy):
    return ss.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

def get_proxy():
    return requests.get("http://127.0.0.1:5010/get").text
    
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
    '''
    headers = {
        'user-agent': 'Mozilla/5.0 (iPad; CPU OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B466 Safari/600.1.4'
    }
    async with aiohttp.ClientSession() as session:
3        async with session.get("http://m.douyu.com/{}".format(room.nRoom),headers=headers,timeout = 10) as res:
            assert res.status == 200
            return await res.json()
    '''
    res = s.get(url,timeout=10)
    res.close()
    return res.json()
        
def huyastatus(hs,thread_pool=None):
    url = 'https://fw.huya.com/dispatch?do=subscribeList&uid=1199513272235&page=1&pageSize=1000'
    hcookies={
            'Cookie': 
            '__yaoldyyuid=1199513272235; _yasids=__rootsid%3DC8974FE151100001F5BC5CE021CE8530; undefined=undefined; udb_accdata=15671674441; udb_biztoken=AQAE1MwneVM1gFBX2rT5xIArj05wUcCZogFkV-0O2OC6AhRZjf420byWLTlZjtls3oBLTax_r1zlXgroGYC6mYMjkdYQ3jo2AE8Ejc2Zy7ifF_57kHxpHuZXikRyXdsXc-1i1rlehnzvDHo8YYkrpvwJLzZ6kr2ujdvfAY_ut8p2ZTxMkxJNdgeah-7ImxNPnAqSkfcx2-hjWJ9eIKjhRJNswE0sWoEJuRu9MFA19YwXRgUha0o9X39H_GVofCNEngnlC7tmbsPAmzfrDurUEqsPIlhTgujTNfdZLslXGlYX37Jo5enp_QnAZXw_UEPRMbmoDtbl5blUfme7dW9E_0oM; udb_origin=1; udb_other=%7B%22lt%22%3A%221567869658681%22%2C%22isRem%22%3A%221%22%7D; udb_passport=35184377273454hy; udb_status=1; udb_uid=1199513272235; udb_version=1.0; username=35184377273454hy; yyuid=1199513272235; Hm_lpvt_51700b6c722f5bb4cf39906a596ea41f=1567869606; Hm_lvt_51700b6c722f5bb4cf39906a596ea41f=1567264276,1567869606; __yasmid=0.16792272486884974; udb_passdata=3; PHPSESSID=afs88vfr8coe6led6cajbl67k7; first_username_flag=35184377273454hy_first_1; udb_guiddata=0bbad9f2e2cf4e1a991053879674cda8; __yamid_new=C8950E7EEEF00001BCF21A109C1F1A14; __yamid_tt1=0.16792272486884974'
            }
    hs.cookies.update(hcookies)
    try:
        #json = await loop.run_in_executor(thread_pool,functools.partial(gethtml,hs,url))
        json = gethtml(hs,url)
        data = json['result']
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
    except:
        try:
            if '未登录' in str(json):
                subject = '虎牙出错'
                contents='虎牙登录过期'
                send_mail(subject,contents,password)
                time.sleep(600)
            print(json)
        except:
            print('虎牙错误检测出错')
    finally:
        if "huya" in status:
            status.remove("huya")
        sys.stdout.write('\rhuya刷新\n')
    '''
    if room.thread and room.thread.isAlive():
        return
    try:
        json = await gethtml(room)
    except Exception as e:
        print(e)
        return
    status = re.findall(r"\"stream\": ({.+?})\s*};",html)
    if(status == []):
        return
    data = json.loads(status[0])
    if(data['status'] == 200):
        if room.thread and room.thread.isAlive():
            pass
        else:
            down = threading.Thread(target=huyad,args=(room.nDomain,room.nRoom,),name=str(room.nRoom),daemon=True)
            room.thread = down
            down.start()
    '''

def douyustatus(ds,thread_pool=None):
    global dRooms
    global justone
    global dcookies
    #print('run')
    #url = 'https://www.douyu.com/wgapi/livenc/liveweb/followlist/0?sort=0&cid1=0'
    url = "https://www.douyu.com/wgapi/livenc/liveweb/follow/list?sort=0&cid1=0" 
    ds.cookies.update(dcookies)
    try:
        #json = await loop.run_in_executor(thread_pool,functools.partial(gethtml,ds,url))
        json = gethtml(ds,url)
        data = json['data']
        dlist = data['list']
        for i in dlist:
            if i['show_status'] == 1:
                if i['room_id'] not in drecording:
                    down = threading.Thread(target=youd,args=('douyu',i['room_id'],),name=str(i['nickname']),daemon=True)
                    down.start()
    except:
        try:
            dcookies = {"Cookie": "dy_did=8242408a3b65feb390623d6c00081501; smidV2=2019051418520294dca99b6773cfe1c2a03077977c1b0d007f7dac9e8893840; _dys_refer_action_code=init_page_author; Hm_lvt_e99aee90ec1b2106afe7ec3b199020a7=1565337319,1565345238,1565399909,1565402312; acf_auth=8098pNG6AjBMqfcS7TrkfX1dIKjpp6tT2kXdLka2ulVhCI%2BAruOEfMJ4Zpw6OVp2Pg2FpbL94ZTQzLxUhxCcQ0v08fp0uUnb6hVu75kGUUUA8yqaDDK0zMsmPAIW; wan_auth37wan=ad6d52926d1dGrpl5zqSwjb%2FLECNu1bdNqsNKPbIvAHpUDD4rNRgjZM8P1NFkubgW8qKTarSS68805tkxZ6EYboo3yWe5W%2FP822Op0BbDEJKtbJh; acf_uid=5550012; acf_username=auto_7NcKZj9sbL; acf_nickname=Miloxin; acf_own_room=0; acf_groupid=1; acf_phonestatus=1; acf_ct=0; acf_ltkid=46925293; acf_biz=1; acf_stk=a44a3deba8913c64; acf_did=8242408a3b65feb390623d6c00081501; LTP0=e2a80bQ27D8KOPuMC5Srmv%2BTxqRuLwfxlwiQKAA4ewn8CpS0pxkXMSdZgDFV6O0dwR%2FOChGNxyhAY1LV%2Fj%2FxPDm9cHmHQB8mhzSbykqF%2B6TYJOECK81CJb%2FkzuyTkGKeyL5dOxmk2L8aAPqHkVjEq5U0drFRQiQvw7mRcakxdoGeb7NR4Ter6jPNI0I6RgjRY%2FV9k;"}
            s = requests.session()
            s.keep_alive=False
            print(json)
            headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36","Referer":"https://www.douyu.com/directory/myFollow"}
            url = 'https://passport.douyu.com/lapi/passport/iframe/safeAuth?client_id=1&t={t}&_={t}'.format(t=int(time.time()*1000))
            res = requests.get(url,headers=headers,cookies=dcookies,allow_redirects=False)
            if res.headers.get('Set-Cookie'):
                dcookies={"Cookie":"{}".format(dcookies['Cookie'].split("LTP0")[0]+res.headers['Set-Cookie'])}
            print(dcookies)
            if res.headers.get('Location'):
                url = 'https:'+res.headers['Location']
                res = s.get(url,headers=headers,cookies=dcookies,allow_redirects=False)
                ds.cookies=dcookies = s.cookies
                print(dcookies)
                douyustatus(ds)
            elif '过期' in str(json):
                subject = '斗鱼出错'
                contents = '斗鱼登录过期'
                send_mail(subject,contents,password)
                time.sleep(20)
            
        except:
            pass
    if "douyu" in status:
        status.remove("douyu")
    
    sys.stdout.write("\rdouyustatus")
    """
    if room.thread and room.thread.isAlive():
        return
    try:
        html = await gethtml(room)    
    except Exception as e:
        print(e)
        print('128行斗鱼页面获取错误\n')
        try:
            html = await gethtml(room)
        except Exception as e:
            #proxies = getip()
            return 
    #status = re.findall(r"ROOM.show_status\s*=\s*\d{1}",html)
    status = re.findall(r"isLive\":\d{1}",html)
    #print(status)
    try:
        #ison = re.match(r"ROOM.show_status\s*=\s*1",status[0])
        ison = re.match(r"isLive\":1",status[0])
    except Exception as e:
        print(e)
        print('143行直播间信息寻找失败\n')
        #proxies = getip()
        return
    if ison:
        #特别---
        if room.nRoom == 533493 and re.findall(r"Title-headlineH2.*?大\s*自\s*然",html):
            if justone == 1:
                justone = 0
                print("Misa在聆听大自然")
            return
    #-------
        if room.thread and room.thread.isAlive():
            pass
        else:
            down = threading.Thread(target=youd,args=(room.nDomain,room.nRoom,),name=str(room.nRoom),daemon=True)
            room.thread = down
            down.start()
    else:
        pass
    """

def main():
    global justone
    global dRooms
    global dpath
    global hRooms
    ms = []
    datas = []
    pRooms = []
    dRooms = []
    datas=input('输入平台 room：').split(' ')
    b = len(datas)
    for i in range(b):
        if datas[i].isalpha():
            ms = datas[i+1].split(',')
                #if datas[i]=='huomao':
                #    for room in ms:
                #        down = threading.Thread(target=huod,args=(datas[i],room,))
                #        down.start()

            if datas[i]=='d':
                dpath=datas[i+1]
                if (not os.path.exists(dpath)):
                    os.makedirs(dpath)
            '''        
            if datas[i]=='huya':
                if (not os.path.exists('huser.txt')):
                    with open("huser.txt","a") as f:
                        for a in ms:
                            a = a.strip();
                            if (a):
                                f.writelines(a)
                                f.write('\n')
                        f.close
                else:
                    for a in ms:
                        a=a.strip()
                        if(a):
                            sameid = 0
                            for k in open("huser.txt","r").read().splitlines():
                                if (k == a):
                                    sameid = 1
                                    break
                            if(sameid == 1):
                                continue
                            else:
                                with open("huser.txt","a") as r:
                                    r.writelines(a)
                                    r.write('\n')
                                    r.close
                                    
            if datas[i]=='douyu':
                if (not os.path.exists('duser.txt')):
                    with open("duser.txt","a") as f:
                        for a in ms:
                            a = a.strip();
                            if (a):
                                f.writelines(a)
                                f.write('\n')
                        f.close
                else:
                    for a in ms:
                        a=a.strip()
                        if(a):
                            sameid = 0
                            for k in open("duser.txt","r").read().splitlines():
                                if (k == a):
                                    sameid = 1
                                    break
                            if(sameid == 1):
                                continue
                            else:
                                with open("duser.txt","a") as r:
                                    r.writelines(a)
                                    r.write('\n')
                                    r.close
            '''
            i+=1
    #for a in open("duser.txt","r").read().splitlines():
    #    room = Room(a,'douyu')
    #    dRooms.append(room)
        
    #for b in open("huser.txt","r").read().splitlines():
    #    print(b)
    #    room = Room(b,'huya')
    #    hRooms.append(room)
    
    #ck = threading.Thread(target=checkuser,name=("check"),daemon=True)
    #ck.start()
    #loop = asyncio.get_event_loop()
    #thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=10)
    dheaders = {
        "Connection":"close",
        "Accept":"application/json, text/plain, */*",
        "X-Requested-With":"XMLHttpRequest",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        "Referer":"https://www.douyu.com/directory/myFollow",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-CN,zh;q=0.9,ja;q=0.8"} 
    ds = requests.session()
    ds.headers.update(dheaders)
    hheaders={
            "Connection":"close",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            "Accept":"*/*",
            "Referer":"https://i.huya.com/",
            "Accept-Encoding":"gzip, deflate, br",
            "Accept-Language":"zh-CN,zh;q=0.9,ja;q=0.8"}
    hcookies={
            "Cookie":"SoundValue=0.50; alphaValue=0.80; guid=b73e698cbb9bde5c8cecb6feb7fe2c4e; __yamid_tt1=0.5630173980060627; __yamid_new=C8736F6698800001A3314BF01CD08350; udb_guiddata=4d0af64ce63b43f29a7a5975d914b205; udb_accdata=15671674441; first_username_flag=35184377273454hy_first_1; isInLiveRoom=; udb_passdata=3; Hm_lvt_51700b6c722f5bb4cf39906a596ea41f=1558668913,1558670658,1559283009; __yasmid=0.5630173980060627; udb_biztoken=AQCJARLtnsnP3PrH59ttEGNJcFNQWHXM60rdexui6uY15DqTy_9w6RwZB_4FNE9su_CduneY4h6rnHLNCYIGaWLpSxh27iqOVX-6kMLoUufzAFAcqVzRafv1luobNTOH6CzcQ8mIi3CkCclEqL0-d-fJU6XsQun6AR6ma4h9E3545oKbts_GtoPnhJavygUqbPhIpFPjxZrEUtsMF6nJW0kaW9TtP-eETlNp7gxNKKUdEnc9ut1dkDbGTRjkS-In5J1hlP1rCzh6XS0gNuMOSFaimsjcahEvS7l1-yAbTrQyturDRz5wg2phI0x76XQ4Tinph0M1HSeqQXGvLuxRHd1u; udb_origin=1; udb_other=%7B%22lt%22%3A%221559283011660%22%2C%22isRem%22%3A%220%22%7D; udb_passport=35184377273454hy; udb_status=1; udb_uid=1199513272235; udb_version=1.0; username=35184377273454hy; yyuid=1199513272235; __yaoldyyuid=1199513272235; _yasids=__rootsid%3DC87753586C700001D59E121A1297BF40; PHPSESSID=b7oilpt3r24it479t0mkkeacj7; undefined=undefined; h_unt=1559283066; Hm_lpvt_51700b6c722f5bb4cf39906a596ea41f=1559283072"
            }
    hs = requests.session()
    hs.headers.update(hheaders)
    hs.cookies.update(hcookies)
    while True:
        #tasks1 = [douyustatus(loop,ds,thread_pool)]
        #tasks2 = [huyastatus(loop,hs,thread_pool)]
        #tasks = tasks1+tasks2
        #loop.run_until_complete(asyncio.wait(tasks)) 
        if 'douyu' not in status:
            status.append("douyu")
            douyu_status = threading.Thread(target=douyustatus,args=(ds,),name=douyustatus)
            douyu_status.start()
        if 'huya' not in status:
            status.append("huya")
            huya_status = threading.Thread(target=huyastatus,args=(hs,),name=huyastatus)
            huya_status.start()
        sys.stdout.write("\r  update") 
        time.sleep(random.randint(0,5))
    
if __name__ =="__main__":
    main()

