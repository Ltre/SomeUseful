import os,random
import time
import re
import requests
import threading
from requests.exceptions import HTTPError
import json
import sys,configparser
from multiprocessing import Process
import aiohttp,asyncio
import nest_asyncio
nest_asyncio.apply()
proxies = {}
justone = 1
dRooms = []
hRooms = []
dpath = None

    
    
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
        os.system('ykdl www.{}.com/{} -o /root/b/d/huya'.format(c,m))
    except:
        pass
    
def youd(c,m):
    global dpath
    #while True:
    print('www.%s.com/%s -o %s' % (c,m,dpath))
    try:
        os.system('ykdl www.{}.com/{} -o {} -t 20'.format(c,m,dpath))
    except:
        pass
     #   finally:
     #       time.sleep(20)

            
def pandad(c,m):
    global dpath
    #while True:
    try:
        os.system('lulu www.{}.com/{} -o {}'.format(c,m,dpath))
    except:
        pass
    #    finally:
      #      time.sleep(20)
           
        
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

async def gethtml(room):
    headers = {
        'user-agent': 'Mozilla/5.0 (iPad; CPU OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B466 Safari/600.1.4'
    }
    async with aiohttp.ClientSession() as session:
        async with session.get("http://m.douyu.com/{}".format(room.nRoom),headers=headers,timeout = 10) as res:
            assert res.status == 200
            return await res.text()

async def huyastatus(room):
    if room.thread and room.thread.isAlive():
        return
    try:
        html = await gethtml(room)
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

async def douyustatus(room):
    global justone
    #print('run')
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

def main():
    global justone
    global dRooms
    global dpath
    global hRooms
    headers = {
        'user-agent': 'Mozilla/5.0 (iPad; CPU OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B466 Safari/600.1.4'
    }
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
            if datas[i]=='pandatv':
                for a in ms:
                    room = Room(a,datas[i])
                    pRooms.append(room)
                    
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
            i+=1
    for a in open("duser.txt","r").read().splitlines():
        room = Room(a,'douyu')
        dRooms.append(room)
        
    for b in open("huser.txt","r").read().splitlines():
        print(b)
        room = Room(b,'huya')
        hRooms.append(room)
    
    ck = threading.Thread(target=checkuser,name=("check"),daemon=True)
    ck.start()
    loop = asyncio.get_event_loop()
    while True:
        tasks1 = [douyustatus(room) for room in dRooms]
        tasks2 = [huyastatus(room) for room in hRooms]
        tasks = tasks1+tasks2
        #loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks)) 
        #loop.close()

        for room in pRooms:
            
            try:
                json_request_url ="http://www.panda.tv/api_room_v2?roomid={}&__plat=pc_web&_={}".format(room.nRoom, int(time.time()))
                html = requests.get(json_request_url,headers=headers,proxies=proxies,timeout = 10)
        
            except Exception as e:
                print(e)
                try:
                    raise aerror('172行熊猫信息出错\n')
                except aerror as e:
                    print(e)
                #proxies = getip()
                try:
                    json_request_url ="http://www.panda.tv/api_room_v2?roomid={}&__plat=pc_web&_={}".format(room.nRoom, int(time.time()))
                    html = requests.get(json_request_url,headers=headers,proxies=proxies,timeout = 10)    
                except Exception as e:
                    #proxies = getip()
                    continue
            try:
                api_json = json.loads(html.text)
                data = api_json["data"]
                status = data["videoinfo"]["status"]
            except Exception as e:
                print(e)
                try:
                    raise aerror('187行熊猫开播信息提取失败')
                except aerror as e:
                    print(e)
                continue
            
            
            if status is "2":                
                if room.thread and room.thread.isAlive():
                    continue
                else:
                    down = threading.Thread(target=youd,args=(room.nDomain,room.nRoom,),name=str(room.nRoom),daemon=True)
                    room.thread = down
                    down.start()
            else:
                pass
        time.sleep(random.randint(10,22))
    
if __name__ =="__main__":
    main()

