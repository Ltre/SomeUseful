import requests
import re
import json
import time
from streamlink import Streamlink
import traceback
import shutil
from threading import Thread
import os
import sys
checking=[]
recording=[]
def get_real_url(rid):
    room_url = 'http://interface.yy.com/hls/new/get/{rid}/{rid}/1200?source=wapyy&callback=jsonp3'.format(rid=rid)
    headers = {
        'referer': 'http://wap.yy.com/mobileweb/{rid}'.format(rid=rid),
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
        }
    try:
        response = requests.get(url=room_url, headers=headers).text
        json_data = json.loads(re.findall(r'\(([\W\w]*)\)', response)[0])
        real_url = json_data.get('hls', 0)
        if not real_url:real_url=''
    except:
        real_url = ''
    return real_url


def download(rid):
    if rid in recording:
        return
    recording.append(rid)
    real_url = get_real_url(rid)
    if not real_url:
        return
    url = 'https://www.yy.com/'+rid
    res = requests.get(url)
    html = res.text
    title = re.findall(r'h1>(.*)<',html)[-1]
    rstr = r"[\/\\\:\*\?\"\<\>\|\- ]"
    title= re.sub(rstr,"_",title)
    nic = re.findall(r'h2>(.*)<',html)[-1]
    name = nic+'-'+time.strftime('%y%m%d_%H%M%S')+'-'+title+'.ts'
    filepath = '/root/b/d/yy/{}/{}'.format(nic,name)
    if not os.path.exists('/root/b/d/yy/{}'.format(nic)):
        os.makedirs('/root/b/d/yy/{}'.format(nic))
    os.system('cd /root/b/d/yy/{};mv *ts /root/b/d/yy'.format(nic))
    checking.append(nic)
    session = Streamlink()
    streams = session.streams("hlsvariant://{}".format(real_url))
    stream = streams['best']
    fd = stream.open()
    f = open(filepath,"wb")
    readbuffer=1024*8
    fs = 0
    while 1:
        try:
            fdata = fd.read(readbuffer)
            if fdata:
                f.write(fdata)
            else:
                f.close()
                break
        except:
            traceback.print_exc()
            break
    shutil.move(filepath,'/root/b/d/yy')
    if rid in recording:
        recording.remove(rid)
        checking.remove(nic)
while 1:
    rids = open('/root/u/yyuser.txt','r').read().splitlines()
    for rid in rids:
        if rid and rid not in recording:
            a = Thread(target=download,args=(rid,),name=rid,daemon=True)
            a.start()
    sys.stdout.write('\r\033[Konline:{}'.format(checking))
    time.sleep(2)
