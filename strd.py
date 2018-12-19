import os
import time
import re
import requests
import threading
from requests.exceptions import HTTPError
import json
import sys,configparser
ii = 0
proxies = {}
justone = 1
def prepare():
    global ii , proxies
    config = configparser.ConfigParser()
    config.read(sys.path[0] + "/proxy.ini")
    sourceip = config.get('proxy','ip')
    try:
        r = requests.get('http://%s:8765/?types=2&count=20&country=国内' % sourceip,timeout = 10)
    except Exception as e:
        print(e)
        try:
            r = requests.get('http://127.0.0.1:8765/?types=2&count=20&country=国内',timeout = 10)
        except Exception as e:
            print(e)
            try:
                raise aerror("22行获取代理ip错误\n")
            except aerror as e:
                print(e)
    ip_ports = json.loads(r.text)
    print(ip_ports)
    try:
        ip = ip_ports[ii][0]
    except Exception as e:
        print(e)
        try:
            raise aerror("32行ip列表错误\n")
        except aerror as e:
            print(e)
        try:
            r = requests.get('http://%s:8765/?types=2&count=20&country=国内' % sourceip,timeout=10)
            ip = ip_ports[ii][0]
        except Exception as e:
            ii += 1
            if(ii>=20):
                ii=0
            prepare()
            return
    port = ip_ports[ii][1]
    ii += 1
    if(ii>=15):
        ii = 0
    proxies={'http':'%s:%s'%(ip,port)}
    print('取用的IP地址：{}\n'.format(proxies))
    
    
class Room():
    def __init__(self,nRoom=None,nDomain =None):
        self.nRoom = int(nRoom or 0)
        self.nDomain = nDomain
        self.thread = None

class aerror(Exception):
    pass
    
    
    
def youd(c,m):
    #while True:
    try:
        os.system('you-get www.{}.com/{} -o /root/b/d --debug'.format(c,m))
    except:
        pass
     #   finally:
     #       time.sleep(20)

            
def pandad(c,m):
    #while True:
    try:
        os.system('lulu www.{}.com/{} -o /root/b/d'.format(c,m))
    except:
        pass
    #    finally:
      #      time.sleep(20)
           
        
def huod(c,m):
   # while True:
    try:
        os.system('lulu www.{}.com/{} -o /root/b/d'.format(c,m))
    except:
        pass
   #     finally:
  #          time.sleep(20)

def main():
    global justone
    headers = {
        'user-agent': 'Mozilla/5.0 (iPad; CPU OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B466 Safari/600.1.4'
    }
    ms = []
    datas = []
    pRooms = []
    dRooms = []
    datas=input('输入平台 room：').split(' ')
    b = len(datas)
    prepare()
    for i in range(b):
        if datas[i].isalpha():
            ms = datas[i+1].split(',')
                #if datas[i]=='huomao':
                #    for room in ms:
                #        down = threading.Thread(target=huod,args=(datas[i],room,))
                #        down.start()

            if datas[i]=='pandatv':
                for a in ms:
                    room = Room(a,datas[i])
                    pRooms.append(room)
            if datas[i]=='douyu':
                for a in ms:
                    room = Room(a,datas[i])
                    dRooms.append(room)
            i+=1
    while True:
        for room in dRooms:
            try:
                html = requests.get("http://www.douyu.com/{}".format(room.nRoom),headers=headers,proxies = proxies,timeout = 10)
            except Exception as e:
                print(e)
                try:
                    raise aerror('128行斗鱼页面获取错误\n')
                except aerror as e:
                    print(e)
                prepare()
                try:
                    html = requests.get("http://www.douyu.com/{}".format(room.nRoom),headers=headers,proxies = proxies,timeout = 10)
                except Exception as e:
                    prepare()
                    continue
            status = re.findall(r"ROOM.show_status =\s+\d{1}",html.text)
            try:
                ison = re.match(r"ROOM.show_status = 1",status[0])
            except Exception as e:
                print(e)
                try:
                    raise aerror('143行直播间信息寻找失败\n')
                except aerror as e:
                    print(e)
                prepare()
                
                continue
            if ison:
                #特别---
                if room.nRoom == 533493 and re.findall(r"Title-headlineH2.*?大\s*自\s*然",html.text):
                    if justone == 1:
                        justone = 0
                        print("Misa在聆听大自然")
                    continue
            #-------
                if room.thread and room.thread.isAlive():
                    continue
                else:
                    down = threading.Thread(target=youd,args=(room.nDomain,room.nRoom,),name=str(room.nRoom),daemon=True)
                    room.thread = down
                    down.start()
            else:
                pass

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
                prepare()
                try:
                    json_request_url ="http://www.panda.tv/api_room_v2?roomid={}&__plat=pc_web&_={}".format(room.nRoom, int(time.time()))
                    html = requests.get(json_request_url,headers=headers,proxies=proxies,timeout = 10)    
                except Exception as e:
                    prepare()
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
        time.sleep(20)
    
if __name__ =="__main__":
    main()
