from streamlink import streams,Streamlink
from threading import Thread
from time import sleep
from random import randint
import time
import sys
import os
from multiprocessing import Process
import requests,re,shutil
from traceback import print_exc
import subprocess
import gc
import random
#import tracemalloc
#tracemalloc.start()
os.system('bash t.sh')
namelist = []
streaming = []
iplist = []
def getip():
    r = requests.get("http://127.0.0.1:5010/get_all/")
    data = r.json()
    for i in data:
        iplist.append(i.get("proxy"))
def delete_proxy(proxy):
        requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))
def is_streaming(names):
    if names in namelist:
        return
    namelist.append(names)
    proxy = iplist[random.randint(0,len(iplist) - 1)]
    proxies = {'https':proxy}
    url = 'https://www.youtube.com/{}'.format(names)
    try:
        with requests.get(url,proxies = proxies,timeout = 5) as r:
            if 'Live now' in r.text:
                title = re.findall(r'og:title" content="(.+)"',r.text)[0]
                rstr = r"[\/\\\:\*\?\"\<\>\| ]"
                title = re.sub(rstr, "_", title)
                data = re.findall('live-promo" href="(.+)" ',r.text)
                if data:
                    data = data[0]
                r.close()
                if title not in streaming:
                    streaming.append(title)
                else:
                    del r,title,data
                    return
                po = Process(target = stream_download,args=(names,title,data))
                po.start()
                po.join()
                del r,data
            else:
                r.close()
                del r
    except Exception as e:
        #print_exc()\
        #print(e)
        if proxy in iplist:
            iplist.remove(proxy)
    finally:
        if 'title' in locals() and title in streaming:
            streaming.remove(title)
            del title
        if names in namelist:
            namelist.remove(names)
def stream_download(names,title,data):
    name=names.split('/')[-1]
    try:
        
        s = Streamlink()
        s.set_option('hls-live-restart',True)
        s.set_option('--hls-segment-threads',5)
        
        if data:
            url = 'https://www.youtube.com'+data
        else:
            url = "https://www.youtube.com/{}".format(names)
        astreams = s.streams(url)
        stream = astreams['best']
        fd = stream.open()
        
        filename = title + '-'+time.strftime('%y%m%d_%H%M%S')+'_.ts'
        sPath = '/root/b/d/youtube/{}/'.format(title)
        if not os.path.exists(sPath):
            os.makedirs(sPath)
        #subprocess.run(['newstreamlink','--hls-live-restart','-o','{}'.format(sPath+filename),url,'best'])
        
        f = open(sPath+filename,'wb+')
        sums = 0
        normal = 1024*1024*1024
        while 1:
            data = fd.read(1024*8)
            if data:
                sums += f.write(data)
                #if sums >= normal:
            else:
                break
        
    except Exception as e:
        print_exc()
        #print('发生错误',e)
    finally:
        shutil.move(sPath+filename,'/root/b/d/youtube/')
        del url,filename,sPath
        '''
        if 'f' in locals():
            f.close()
            shutil.move(sPath+filename,'/root/b/d/youtube/')
        if 'fd' in locals():
            fd.close()
        '''


def main():
    while 1:
        if len(iplist) <10:
            getip()
        with open('youtube_names.txt','r') as f:
            for name in f.read().splitlines():
                if name:
                    if name not in namelist:
                        a = Thread(target = is_streaming,name = str(name),args = (name,),daemon = True)
                        a.start()
            sys.stdout.write('\r\033[K正在追踪的频道：{}\r\n'.format(len(namelist)))
            sys.stdout.write('\r\033[K正在直播的频道：{}\r\n'.format(streaming))
            #snapshot = tracemalloc.take_snapshot()
            #top_stats = snapshot.statistics('lineno')
            #for stat in top_stats[:5]:
            #        print(stat)
            gc.collect()
            sys.stdout.write('\033[2A')
        sys.stdout.write('{}'.format(len(iplist)))
        sys.stdout.flush()
        sleep(5)
    

if __name__ == '__main__':
    main();
