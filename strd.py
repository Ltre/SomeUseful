import os
import time
import subprocess
from subprocess import *

sleep = time.sleep

def douyu(fullc):
    pass

def pandatv(fullc):
    while True:
        try:
            subprocess.check_call(fullc)
        except ValueError as e:
            print('{},等待重试。。。'.format(e))
        finally:
            sleep(20)
            
            
    print('测试成功{}'.format(fullc))

def main():
    aname,aid = input('输入平台和id，空格隔开：').split(' ')
    fullc='you-get www.{}.com/{} -o /root/b/d'.format(aname,aid)
    if aname == 'pandatv':
        pandatv(fullc)
    elif aname =='douyu':
        douyu(fullc)
        
        
if __name__ =="__main__":
    main()
