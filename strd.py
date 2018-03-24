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
    c,m=input('输入平台 room：').split(' ')
    ms = m.split(',')
    for room in ms:
        down = threading.Thread(target=youd,args=(room,))
        dowm.start()
if __name__ =="__main__":
    main()
