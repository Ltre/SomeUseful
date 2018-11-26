import os
import time
import re
import requests
import threading
from requests.exceptions import HTTPError
import json
ii = 0

def prepare():
    global ii
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
    datas=input('输入平台 room：').split(' ')
    b = len(datas)
    prepare()
    while True:
        for i in range(b):
            if datas[i].isalpha():
                ms = datas[i+1].split(',')
                #if datas[i]=='huomao':
                #    for room in ms:
                #        down = threading.Thread(target=huod,args=(datas[i],room,))
                #        down.start()

                if datas[i]=='pandatv':
                    for room in ms:
                        try:
                            html = requests.get("http://www.pandatv.com/{}".format(room),headers=headers)
                        except HTTPError as e:
                            print(e)
                            prepare()
                            try:
                                html = requests.get("http://www.pandatv.com/{}".format(room),headers=headers)   
                            except HTTPError as e:
                                prepare()
                                continue
                        status = re.findall(r'"status":"\d{1}',html.text)
                        if re.match(r'"status":"2',status[0]):
                            down = threading.Thread(target=huod,args=(datas[i],room,),name=str(room))
                            if down.isAlive():
                                pass
                            else:
                                down.start()
                        else:
                            pass


                if datas[i]=='douyu':
                    for room in ms: 
                        try:
                            html = requests.get("http://www.douyu.com/{}".format(room),headers=headers,proxies = proxies,timeout = 10)
                        except HTTPError as e:
                            print(e)
                            prepare()
                            try:
                                html = requests.get("http://www.douyu.com/{}".format(room),headers=headers,proxies = proxies,timeout = 10)
                            except HTTPError as e:
                                prepare()
                                continue
                        status = re.findall(r"ROOM.show_status =\s+\d{1}",html.text)
                        if re.match(r"ROOM.show_status = 1",status[0]):
                            #特别---
                            if room == '533493' and re.findall(r"Title-headlineH2.*大自然",html.text):
                                print("Misa在聆听大自然")
                                continue
                            down = threading.Thread(target=youd,args=(datas[i],room,),name=str(room))
                            if down.isAlive():
                                pass
                            else:
                                down.start()
                        else:
                            pass


                else:
                    for room in ms:
                        down = threading.Thread(target=youd,args=(datas[i],room,))
                        down.start()
                i+=1
        time.sleep(20)            
    
if __name__ =="__main__":
    main()
