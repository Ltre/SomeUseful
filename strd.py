import os
import time

import threading


def youd(c,m):
    while True:
        try:
            os.system('you-get www.{}.com/{} -o /root/b/d'.format(c,m))
        except:
            pass
        finally:
            time.sleep(20)


def main():
    ms = []
    datas = []
    datas=input('输入平台 room：').split(' ')
    b = len(datas)
    for i in range(b):
        if datas[i].isalpha():
            ms = datas[i+1].split(',')
            for room in ms:
                down = threading.Thread(target=youd,args=(datas[i],room,))
                dowm.start() 
            i+=1
            
    
if __name__ =="__main__":
    main()
