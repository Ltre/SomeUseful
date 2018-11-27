import os
import time
import re
import requests
import threading
from requests.exceptions import HTTPError
import json
ii = 0
proxies = {}
def prepare():
    global ii , proxies
    r = requests.get('http://127.0.0.1:8765/?types=2&count=20&country=国内')
    ip_ports = json.loads(r.text)
    print(ip_ports)
    ip = ip_ports[ii][0]
    port = ip_ports[ii][1]
    ii += 1
    if(ii>=20):
        ii = 0
    proxies={'http':'%s:%s'%(ip,port)}
    print('取用的IP地址：{}\n'.format(proxies))
    
    
class Room():
    def __init__(self,nRoom=None,nDomain =None):
        self.nRoom = int(nRoom or 0)
        self.nDomain = nDomain
        self.thread = None
        
    
    
    
def youd(c,m):
    #while True:
    try:
        os.system('you-get www.{}.com/{} -o /root/b/d'.format(c,m))
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
            except HTTPError as e:
                print(e)
                prepare()
                try:
                    html = requests.get("http://www.douyu.com/{}".format(room.nRoom),headers=headers,proxies = proxies,timeout = 10)
                except HTTPError as e:
                    prepare()
                    continue
            status = re.findall(r"ROOM.show_status =\s+\d{1}",html.text)
            if re.match(r"ROOM.show_status = 1",status[0]):
            #特别---
                if room.nRoom == '533493' and re.findall(r"Title-headlineH2.*大自然",html.text):
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
                html = requests.get("http://www.pandatv.com/{}".format(room.nRoom),headers=headers,proxies = proxies,timeout = 10)
            except HTTPError as e:
                print(e)
                prepare()
                try:
                    html = requests.get("http://www.pandatv.com/{}".format(room.nRoom),headers=headers,proxies = proxies,timeout = 10)   
                except HTTPError as e:
                    prepare()
                    continue
            status = re.findall(r'"status":"\d{1}',html.text)
            if re.match(r'"status":"2',status[0]):                
                if room.thread and room.thread.isAlive():
                    continue
                else:
                    down = threading.Thread(target=huod,args=(room.nDomain,room.nRoom,),name=str(room.nRoom),daemon=True)
                    room.thread = down
                    down.start()
            else:
                pass
        time.sleep(20)
    
if __name__ =="__main__":
    main()
