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
#import tracemalloc
#tracemalloc.start()
os.system('bash t.sh')
namelist = []
streaming = []
def is_streaming(names):
    if names in namelist:
        return
    namelist.append(names)
    url = 'https://www.youtube.com/{}'.format(names)
    while 1:
        try:
            with requests.get(url,timeout = 10) as r:
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
            print_exc()
        finally:
            if 'title' in locals() and title in streaming:
                streaming.remove(title)
                del title
            if names in namelist:
                namelist.remove(names)
            sleep(randint(0,5))
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
        with open('youtube_names.txt','r') as f:
            for name in f.read().splitlines():
                if name:
                    if name not in namelist:
                        a = Thread(target = is_streaming,name = str(name),args = (name,))
                        a.start()
            sys.stdout.write('\r正在追踪的频道：{}\r\n'.format(len(namelist)))
            sys.stdout.write('\r正在直播的频道：{}\r\n'.format(streaming))
            #snapshot = tracemalloc.take_snapshot()
            #top_stats = snapshot.statistics('lineno')
            #for stat in top_stats[:5]:
            #        print(stat)
            gc.collect()
            sys.stdout.write('\033[2A')
        sys.stdout.flush()
        sleep(5)
    

if __name__ == '__main__':
    main();
