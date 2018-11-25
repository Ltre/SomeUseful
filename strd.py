import os
import time
import re
import requests
import threading


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
                        html = requests.get("http://www.pandatv.com/{}".format(room),headers=headers)
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
                        html = requests.get("http://www.douyu.com/{}".format(room),headers=headers)
                        status = re.findall(r"ROOM.show_status =\s+\d{1}",html.text)
                        if re.match(r"ROOM.show_status = 1",status[0]):
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
