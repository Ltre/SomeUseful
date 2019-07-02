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
    res = s.get(url)
    res.close()
    return res.json()
        
def huyastatus(hs,thread_pool=None):
    url = 'https://fw.huya.com/dispatch?do=subscribeList&uid=1199513272235&page=1&pageSize=1000'
    hcookies={
            "Cookie":"SoundValue=0.50; alphaValue=0.80; guid=b73e698cbb9bde5c8cecb6feb7fe2c4e; __yamid_tt1=0.5630173980060627; __yamid_new=C8736F6698800001A3314BF01CD08350; udb_guiddata=4d0af64ce63b43f29a7a5975d914b205; udb_accdata=15671674441; first_username_flag=35184377273454hy_first_1; isInLiveRoom=; PHPSESSID=cr8rh0j89b8unuckhi91pbm8d4; __yasmid=0.5630173980060627; _yasids=__rootsid%3DC87F7C7E48B0000133EA13D01B00D4B0; Hm_lvt_51700b6c722f5bb4cf39906a596ea41f=1560257308,1560510903,1560867442,1561473648; Hm_lpvt_51700b6c722f5bb4cf39906a596ea41f=1561473648; udb_passdata=3; udb_biztoken=AQArObe2qzTZ3gwbqCneNlhWN17v4CzAsxU_pqNqhzyi2q32FHN_Cf1QOMbGCZGtTHHo9Z01C_3H8hbD39LFNmSuRHbRI6kTAOz4JDC-c2DTIQ74CYVoZW30IxMCoPGstuTkbSFZ7yIENSsXWJTGrEuPnMRRf8lBJzfJzBGkozxIZj6j5PF3PwiHNneraHjT4EuBlO1Qb0YAjsbN8ao2WUXS7wVeBrGXqKWJZU0zhrbZ2S4OGdbdC_IRJngW4vq5VzteDMTs1kzgnItoYWDFVgJzoYGBsT83fPYx2TXeIKRKV_gOI-O5QHBqDHoijATRV4hj-5idhlxKnZYkRVpueQ1j; udb_origin=1; udb_other=%7B%22lt%22%3A%221561473656125%22%2C%22isRem%22%3A%221%22%7D; udb_passport=35184377273454hy; udb_status=1; udb_uid=1199513272235; udb_version=1.0; username=35184377273454hy; yyuid=1199513272235"
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
        if '未登录' in str(json):
            subject = '虎牙出错'
            contents='虎牙登录过期'
            send_mail(subject,contents,password)
            time.sleep(600)
        print(json)
    finally:
        if "huya" in status:
            status.remove("huya")
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
    #print('run')
    url = 'https://www.douyu.com/wgapi/livenc/liveweb/followlist/0?sort=0'
    dcookies = {
        "Cookie":"dy_did=8242408a3b65feb390623d6c00081501; acf_did=8242408a3b65feb390623d6c00081501; smidV2=2019051418520294dca99b6773cfe1c2a03077977c1b0d007f7dac9e8893840; acf_uid=5550012; acf_username=auto_7NcKZj9sbL; acf_nickname=Miloxin; acf_ltkid=46925279; PHPSESSID=g6urt56t68qgutnupnd6amqmd4; acf_auth=8622NUs7s4JahBtZpeWC4TqzgHxFQuTHoKTh96G%2FVA%2B2tu9lR3dBAMGaWqDtnoMyp7z%2FkCb%2BYkDEBFfF%2BUvezEquvqkQbZxDbfh4cNhpRmBodd94jCzhHiOedrcQ; wan_auth37wan=12b171a92387xF2aRZmGQrHLDydxOfk4AzwqMSQJbsE1FZvUijqqAnSQ%2FGF8kPK0Q2GxAydUAcukUkMxIBl09Yj%2BEp2J%2F3mdQlG5RInnl%2F8aTtgO; acf_own_room=0; acf_groupid=1; acf_phonestatus=1; acf_avatar=https%3A%2F%2Fapic.douyucdn.cn%2Fupload%2Favatar%2F005%2F55%2F00%2F12_avatar_; acf_ct=0; acf_biz=1; acf_stk=d78e94dbf40f8055; Hm_lvt_e99aee90ec1b2106afe7ec3b199020a7=1560485262,1560676567,1561024467,1561637166; Hm_lpvt_e99aee90ec1b2106afe7ec3b199020a7=1561637173"
    }
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
        print(json)
        if '过期' in str(json):
            subject = '斗鱼出错'
            contents = '斗鱼登录过期'
            send_mail(subject,contents,password)
            time.sleep(300)
    if "douyu" in status:
        status.remove("douyu")
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
        "Connection":"keep-alive",
        "Accept":"application/json, text/plain, */*",
        "X-Requested-With":"XMLHttpRequest",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
        "Referer":"https://www.douyu.com/directory/myFollow",
        "Accept-Encoding":"gzip, deflate, br",
        "Accept-Language":"zh-CN,zh;q=0.9,ja;q=0.8"}
    dcookies = {
        "Cookie":"dy_did=8242408a3b65feb390623d6c00081501; acf_did=8242408a3b65feb390623d6c00081501; smidV2=2019051418520294dca99b6773cfe1c2a03077977c1b0d007f7dac9e8893840; acf_uid=5550012; acf_username=auto_7NcKZj9sbL; acf_nickname=Miloxin; acf_ltkid=46925279; Hm_lvt_e99aee90ec1b2106afe7ec3b199020a7=1559207358,1559227739,1559660016,1559880272; PHPSESSID=mnnem0ue05omdjbqeb78q9iom4; acf_auth=003eR9kvW%2BNvRYbl7%2BXACtwgMvYQGFsSTSvhQCGatEKh%2FKu0P3S6futLH4%2FbTE%2B5QxCtRqbKfpw07%2F7pKL1LuJ9KHkYJm9OIokntB6uUi5Dp7KDiIqsnYo6nsS7%2B; wan_auth37wan=94a404c18776LUbCMataxj0xTDmbt%2BWfcQSDzRH7zTYunn7%2BRLSyXVAb1T119GldXIgR7WRGUOUMdIefQQKCNWK1ucPsX2e7NjizQGDhc5k5bShv; acf_own_room=0; acf_groupid=1; acf_phonestatus=1; acf_avatar=https%3A%2F%2Fapic.douyucdn.cn%2Fupload%2Favatar%2F005%2F55%2F00%2F12_avatar_; acf_ct=0; acf_biz=1; acf_stk=095445fbd245e9bd; Hm_lpvt_e99aee90ec1b2106afe7ec3b199020a7=1559880283; acf_ccn=6a01bc6bb5edafd7b97186eb216e8048"
    }
    ds = requests.session()
    ds.headers.update(dheaders)
    ds.cookies.update(dcookies)
    hheaders={
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

