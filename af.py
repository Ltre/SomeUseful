# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 20:45:54 2020

@author: zhang
"""
import os,time
import streamlink
import json
import re
import shutil
import sys
from threading import Thread
import random
from streamlink.stream import HLSStream
def login(username,password):
    
    data = {
                "szWork": "login",
                "szType": "json",
                "szUid": username,
                "szPassword": password,
                "isSaveId": "true",
                "isSavePw": "false",
                "isSaveJoin": "false"
    }
    res = session.http.post(login_url, data=data)
    res = res.json()
    if res["RESULT"] == 1:
        return True
    else:
        return False

def get_channel_info(user_id):
        data = {
            "bid": user_id,
            "bno":broad_no,
            "type":"live",
            "pwd":"",
            "stream_type":"common",
            "quality":"HD",
            "mode": "landing",
            "player_type": "html5"
        }
        hls_key_url = f'http://live.afreecatv.com/afreeca/player_live_api.php?bjid={user_id}'
        res = session.http.post(hls_key_url,data=data,timeout=10)
        rjson = res.json()
        res.close()
        return rjson['CHANNEL']

def get_hls_key(user_id,broad_no):
    data={
        "bid":user_id,
        "bno":broad_no,
        "type":"aid",
        "pwd":"",
        "player_type":"html5",
        "stream_type":"common",
        "quality":"original",
        "mode":"landing"
    }
    hls_key_url = f'http://live.afreecatv.com/afreeca/player_live_api.php?bjid={user_id}'
    res = session.http.post(hls_key_url,data=data,timeout=10)
    return res.json()

def get_stream_info(broad_no,cdn,rmd):
    params = {
        "return_type": cdn,
        "broad_key": f"{broad_no}-flash-original-hls"
    }
    stream_info_url = f"{rmd}/broad_stream_assign.html"
    res = session.http.get(stream_info_url,params=params,timeout=10)
    rjson = res.json()
    res.close()
    return rjson

def get_hls_streams(user_id,broad_no,cdn,rmd):
    keyjson = get_hls_key(user_id,broad_no)
    if keyjson['CHANNEL']['RESULT'] != 1:
        return
    key = keyjson['CHANNEL']['AID']
    info = get_stream_info(broad_no, cdn, rmd)
    if "view_url" in info:
        return HLSStream(session, info["view_url"], params=dict(aid=key))

def get_streams(user_id,broad_no):
    channel = get_channel_info(user_id)
    if channel.get("BPWD") == "Y":
        print("Stream is Password-Protected")
        return
    elif channel.get("RESULT") == -6:
        print("Login required")
        return
    elif channel.get("RESULT") != 1:
        return
    (rmd, cdn) = (channel["RMD"], channel["CDN"])
    if not (rmd and cdn):
        print('')
        return
    hls_stream = get_hls_streams(user_id,broad_no,cdn,rmd)
    if hls_stream:
        return hls_stream

def download(user_id,broad_no,user_nick):
    if user_id in recording:
        return
    recording.append(user_id)
    #session = streamlink.Streamlink()
    session.get_plugins()
    if threads:
        session.set_option('hls-segment-threads',int(threads))
    if trytimes:
        session.set_option('hls-segment-attempts',int(trytimes))
    session.set_option('hls-live-edge',9999)
    session.set_option('http-timeout',10.0)
    session.set_loglevel('error')
    userurl = f'http://play.afreecatv.com/{user_id}/{broad_no}'
    #print(user_id,userurl)
    streams = session.streams(userurl)
    try:
        stream = streams['best']
        #fd = stream.open()
    except:
        stream = get_streams(user_id,broad_no)
        '''
        filename = f"{user_id}-{time.strftime('%y%m%d_%H%M%S')}-{user_nick}-{broad_no}.ts"
        path = f"/root/b/d/kr/{user_id}"
        if not os.path.exists(path):
            os.makedirs(path)
        filepath = os.path.join(path,filename)
        os.system(f'streamlink "{userurl}" best -o {filepath} --afreeca-username danyulh --afreeca-password zongqian12345')
        shutil.move(filepath,"/root/b/d/kr")
        #print(user_id,streams)
        if user_id in recording:
            recording.remove(user_id)
        return
        '''
    filename = f"{user_id}-{time.strftime('%y%m%d_%H%M%S')}-{user_nick}-{broad_no}.ts"
    opath = "/root/b/d/kr"
    path = f"/root/b/d/kr/{user_id}"
    try:
        fd = stream.open()
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            files = os.listdir(path)
            for file in files:
                fp = os.path.join(path,file)
                shutil.move(fp,opath)
        filepath = os.path.join(path,filename)
        f = open(filepath,'wb')
        readsize = 1024*8
        limitsize = 1024*1024*1024
        fs = 0
        print(f"\r\033[K{user_id} {user_nick} start recording")
        while 1:
            data = fd.read(readsize)
            if data:
                fs+=f.write(data)
                if fs>=limitsize:
                    f.close()
                    shutil.move(filepath,opath)
                    filename = f"{user_id}-{time.strftime('%y%m%d_%H%M%S')}-{user_nick}-{broad_no}.ts"
                    filepath = os.path.join(path,filename)
                    f = open(filepath,'wb')
                    fs = 0
            else:
                break
    except Exception as e:
        print(f"\r\033[K{e}")
    finally:
        print(f"\r\033[K{user_id} {user_nick} recording end")
        if 'f' in locals():
            f.close()
        if 'fd' in locals():
            fd.close()
        if user_id in recording:
            recording.remove(user_id)
        files = os.listdir(path)
        if not files:
            os.rmdir(path)
recording = []
passwordlist= []
trytimes = input('重试次数')
threads = input('线程数')
url='http://live.afreecatv.com/afreeca/favorite_list_api.php?callback=jQuery1102022963313071578284_1581209013959&szPlatformType=main&nFixBroadCnt=6&szFrom=webk&szClub=y&lang=zh_CN&_=1581209013963'
#headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36","Accept":"*/*","Referer":"http//vod.afreecatv.com/PLAYER/STATION/52807259","Accept-Encoding":"gzip, deflate","Accept-Language":"zh-CN,zh;q=0.9,ja;q=0.8","Cookie":"_ga=GA1.2.1950263840.1580971200; _au=0x68facd496a942393; OAX=IlwDSl478IoADU3Q; _gid=GA1.2.1741676268.1581074348; _lang=zh_CN; NextChangePwd=1; UserClipToolTip=off; PdboxTicket=.A32.7bbT56vyHM9fKZk.L7Wmc_lCQVxGEjJgS8bL9DW181YoaVEWSL3ShiwS8uYuHnw9EkvxkCeOkYFLqhmC2fnBFWx8uMdND1AhLoTZrb6AyiB8YF2sQcNUjpR9PvwmKwfLCMl7kQLFT4Fe14WKu_du0kNvGfEeW-pxre07w0TWIOkENX5pMs26TjDy_osnLd5mLaX_bP8McHPWw-6O9pF3kbaEUSEbISke0dqcnSXr9gr9MsG_hkNLVwB88sMHfWLpV8-cDVL4zV9k52FjQDn5yXhgXVkzPMjgqMQfvV8VQf9HHr9_smx2S9XCEMpFE8gdHA3ykhczroP-WaAEqeh0ltDFnpZqPEabeNpAVqJm8TSZvi-YmAYBGFXHs9fYz3KCKcoLyD65d1nctCUyROjo822IU9hRuVTy6gwT_dwlUq3lsqkXnndJq_NVE6jxhYCJhaCCAoyEI8gvRscEURrimzIK6Gb2-Fon5c-ZP2Ik1LzccOcbmTGVOH_3DGj9Jd6D4XMWvnTVVOvCyn2r; PdboxBbs=danyulh; PdboxUser=uid%3Ddanyulh%26uno%3D37845633%26age%3D25%26sex%3DA%26A%3DAAD%26B%3DBACF%26unick%3Ddanyulh%26apply_date%3D1482400106%26name_chk%3D1%26sess_adult_chk%3D1%26broad_name_chk%3D1%26change_password%3D1; isBbs=1; RDB=c803000000000000000000000000000000000000000000000100000019190000000000000001; PdboxSaveTicket=.A32.7bbT56vyHM9fKZk.rtMRUg95LfpIBehpPnGVWw; _csk=%uC784%uC9C0%uAE08%0C%uC730%uB315%0C%uB9C8%uC131%uC758%uC0AC%uC2B4%0C%uB3C4%uBCF5%uC21C%0C%uAE40%uC774%uBE0C; bjStationHistory=921345%023364971%0220790211%02848340%0213679665%0217007600%0219909393%0221026876%0214941146%0219784724; AbroadChk=OK; AbroadVod=OK; _ausb=0x9fd5d7ba; XSRF-TOKEN=gQ1MC8GDbnAwYthNWS7LHOa8oCCwqXA2YdtPJLeu; laravel_session=cuSrfTzqM60vKcHkRVyxMbNNVAbThejOBsOZ0WrT; _ausa=0x35818914"}
login_url = "https://member.afreecatv.com:8111/login/LoginAction.php"
session = streamlink.Streamlink()
session.http.headers['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0"
username='danyulh'#input('username')
password = 'zongqian12345'#input('password')
if login(username,password):
    print('success')
else:
    print('error')
while 1:
    try:
        r = session.http.get(url,timeout=10)
    except Exception as e:
        print(e)
        time.sleep(1)
        continue
    r.encording = r.apparent_encoding
    cont = r.text
    rex=re.compile(r'\w+[(]{1}(.*)[)]{1}')
    try:
        s=rex.findall(cont)[0]
    except:
        continue
    s=s.replace('ON_AIR_FAVORITE_BROAD_TOTAL_CNT','"ON_AIR_FAVORITE_BROAD_TOTAL_CNT"')
    s=s.replace('FAVORITE_ALL_TOTAL_CNT','"FAVORITE_ALL_TOTAL_CNT"')
    s=s.replace("\&#039;","_")
    try:
        data=json.loads(s)
    except Exception as e:
        with open('/root/aftest.txt','w') as f:
            f.writelines(s)
        print(e)
        continue
    channel = data['CHANNEL']
    onair = channel['ON_AIR_FAVORITE_BROAD']
    templist = []
    for i in onair:
        user_id = i['user_id']
        user_nick = i['user_nick']
        broad_no = i['broad_no']
        is_password = i['is_password']
        if is_password !="N":
            if user_id not in passwordlist:
                #print(f"\r\033[K{user_id} 有密码")
                #print(i)
                passwordlist.append(user_id)
                templist.append(user_id)
        else:
            if not user_id in templist:
                if user_id in passwordlist:
                    #print(f'{user_id} 没有密码，删除')
                    #print(i)
                    passwordlist.remove(user_id)
                if not user_id in recording:
                    a = Thread(target=download,args=(user_id,broad_no,user_nick,),name=user_id,daemon=True)
                    a.start()
    sys.stdout.write(f"\r\033[K正在录制{len(recording)}")
    time.sleep(random.choice(range(5,6)))
    

