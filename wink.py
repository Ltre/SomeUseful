
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 20:45:54 2020

@author: zhang
"""
import os
import re
import time
import requests
import json
import shutil
#import streamlink
import livestreamer
import random
import sys
from threading import Thread
from websocket import create_connection

def get_proxy():
    try:
        r = requests.get('http://127.0.0.1:5010/get/',timeout=10)
        proxy = r.json()['proxy']
        return proxy
    except:
        return

def download(user_id,code,sessKey):
    if user_id in recording:
        return
    recording.append(user_id)
    wsurl = 'ws://chat2.neolive.kr/socket.io/?EIO=3&transport=websocket'
    hello = '42["Init",{"site":"winktv","deviceType":"webPc","deviceVersion":"1.0.0","userAgent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36","sessKey":"'+sessKey+'","ReturnParam":true}]'
    #message = '42["Login",{"sessKey":"2f87bc6e722892ef9a985c71f7ccea122ea5c6f48bd11ffd3d9aebc024885054","id":"ao3jpr","ReturnParam":true}]'
    room = '42["WatchInfo",{"roomid":"'+code+'","action":"watch","ReturnParam":true}]'
    ws = create_connection(wsurl,http_proxy_host="34.92.3.74", http_proxy_port=3654)
    #ws.send(hello)
    while 1:
        res = ws.recv()
        #print(res)
        if res=='40':
            sys.stdout.write(f'{user_id}发送hello')
            ws.send(hello)
        elif 'Init' in res:
            ws.send(room)
        elif 'WatchInfo' in res:
            nres = re.findall(r'\[.*\]',res)[0]
            data = json.loads(nres)
            result = data[-1]
            isget = result['result']
            if not isget:
                if 'errorData' in result:
                    ecode = result['errorData']['code']
                    if 'needUnlimitItem' in ecode:
                        sys.stdout.write(f'\r\033[K{user_id}满，重试')
                        ws.close()
                        time.sleep(1)
                        ws = create_connection(wsurl,http_proxy_host="34.92.3.74", http_proxy_port=3654)
                        continue
                    else:
                        print(ecode)
                        ws.close()
            break
        elif 'error' in res:
            ws.close()
            break
    #if 'WatchInfo' in res:
    if isget:
        #nres = re.findall(r'\[.*\]',res)[0]
        #data = json.loads(nres)
        #result = data[-1]
        #isget = result['result']
 
        media = result['media']
        playlist = result['PlayList']
        user_nick = media['userNick']
        user_id = media['userId']
        title = media['title']
        hls = playlist['hls']
        streamurl = hls[0]['url']
        #session = streamlink.Streamlink()
        session = livestreamer.Livestreamer()
        if threads:
            session.set_option('hls-segment-threads',int(threads))
        if trytimes:
            session.set_option('hls-segment-attempts',int(trytimes))
        session.set_option('hls-live-edge',9999)
        try:
            streams = session.streams('hlsvariant://'+streamurl)
            stream = streams['best']
        except:
            print(user_id,streams)
            if user_id in recording:
                recording.remove(user_id)
            return
        filename = f"{user_id}-{time.strftime('%y%m%d_%H%M%S')}-{user_nick}-{title}.ts"
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
            try:
                f = open(filepath,'wb')
            except:
                title = '_'
                filename = f"{user_id}-{time.strftime('%y%m%d_%H%M%S')}-{user_nick}-{title}.ts"
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
                        filename = f"{user_id}-{time.strftime('%y%m%d_%H%M%S')}-{user_nick}-{title}.ts"
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
    else:
        try:
            print(f"\r\033[K{user_id} {user_nick} recording end")
            files = os.listdir(path)
            if not files:
                os.rmdir(path)
        except:
            pass
        if user_id in recording:
            recording.remove(user_id)

def checklogin(sessKey):
    dlist = [
{
    "_i3nY6v7ot9WIAugPuZ6Pj3WlOU":"UXTHn1wARzfIPweF5cRopzGLoQKtqw7PTgWS7c65ob6onyWoODKayxnNGcNtWb7s4ZPhu1igSxotvtVIv2TLrQmkSzEU92rBvtA9Y_ChOsWVbDEVClcJWpUM8CEgqSWN8IcDzjrMvtVInZTLbSNprEhxikWw7pVInyTLrQlpbDGavmWS4c9so1PlNSLxbE8FfmrR7dQMIcTpnyVku2JePkYU4dNAocP67SPZrDig9ksPvo9LobTAaynhB26DTmrSTtHQ8cDcNtlN8IGDD3uthl",
    "Yt40SkS4eFP1sNLe4Dna":"1581831342",
    "AYohuyc98ugPuZ6Pj3WlOU":"73e182930a30e01cb66ac6a444d4aacb1d35f5d86131b504fce516d02915824b",
    "yQv1sB81otLfILAZU_XYXoaA":"abe3c9b81d61a3a557018f042ad62b8addbdb3a5a2b9ac01703fd8dec88d2438",
    "o3GVexFtLZADj4Idn1w0S34Bzo":"36d0886e3f3772c151d0f6a0082a2f0e79af9ffdecef1327790fa1674b74260e",
    "YtK1kkS4aBf-Yxfc4Dna":"webMobile",
    "y6RycBO1oZLfADX_9tKZXoaA":"1.0.0"
}
 
]
    #proxy = get_proxy()
    #proxies = {'http':proxy}
    d = random.choice(dlist)
    while 1:
        try:
            r = s.post(checkurl,data=d,proxies=proxies,timeout=10)
            data = r.json()
            break
        except Exception as e:
            if 'time' in str(e):
                time.sleep(1)
            else:
                return 0,sessKey
    r.close()
    isLogin = data['data']['userInfo']['isLogin']
    sessKey = data['sessKey']
    return isLogin,sessKey

def login(sessKey):
    isLogin,sessKey = checklogin(sessKey)
    if not isLogin:
        logind={
            "29X__Q4yowex4Bzo":"ao3jpr",
            "2wqZ_Q4yowex4Bzo":"o1gnub!!",
            "AYUcv2W9f-yi4dNLpZWlOU":"on",
            "o36w9w_N3d85AZ_Q4yowex4Bzo":"03AOLTBLSwdxaA5L_kJjiCpoUuRFaBYAw6VLIe_4F8XOzucTd0UqsnMxKXUpvfPwre53v_-XKRbBBnvplvTRPKFVYhXbjmRVpHN9jFIhdlsKGXBmwIKtxaZWlyt8RJ9BKn3IbBB3pgSIrGFvOLwcOj0YdhI9_aUlzzNawZhOqcvONjH_N3TjJlK9BoVClRsQknorPXAAdSlD9IWFXf_pUOhCUN8olTr7MM84THBkH9dogZRP3InkzWW4RLj2BiRLOpmQImBHChojOcpPQQhY4UFCKpTk-24p5UTGt5qPGcq7JfIvqw1oOoqYKSYNWkHTvmICiPAIn90n5zMmcOy_OuYiw0a6eCDD4DpSw7GmdAgpJZ89pgH5rAlwcLm3Kn3j9WSSjZOkOY8sZF1rFjYY_GplICZQt3M80ZNyLDC6RpZabgMZnMZYt_M58",
    "_i3nY6v7ot9WIAugPuZ6Pj3WlOU":"UXTHn1wARzfIPweF5cRopzGLoQKtqw7PTgWS7c65ob6onyWoODKayxnNGcNtWb7s4ZPhu1igSxotvtVIv2TLrQmkSzEU92rBvtA9Y_ChOsWVbDEVClcJWpUM8CEgqSWN8IcDzjrMvtVInZTLbSNprEhxikWw7pVInyTLrQlpbDGavmWS4c9so1PlNSLxbE8FfmrR7dQMIcTpnyVku2JePkYU4dNAocP67SPZrDig9ksPvo9LobTAaynhB26DTmrSTtHQ8cDcNtlN8IGDD3uthl",
    "Yt40SkS4eFP1sNLe4Dna":"1581831342",
    "AYohuyc98ugPuZ6Pj3WlOU":"73e182930a30e01cb66ac6a444d4aacb1d35f5d86131b504fce516d02915824b",
    "yQv1sB81otLfILAZU_XYXoaA":"abe3c9b81d61a3a557018f042ad62b8addbdb3a5a2b9ac01703fd8dec88d2438",
    "o3GVexFtLZADj4Idn1w0S34Bzo":"36d0886e3f3772c151d0f6a0082a2f0e79af9ffdecef1327790fa1674b74260e",
    "YtK1kkS4aBf-Yxfc4Dna":"webMobile",
    "y6RycBO1oZLfADX_9tKZXoaA":"1.0.0"
}

        r = s.post(loginurl,data=logind,proxies=proxies,timeout=10)
        data=r.json()
        message = data['message']
        if message == '로그인되셨습니다.':
            print("\r\033[K登录成功")
            sessKey = data['sessKey']
        else:
            print('\r\033[K登录失败')
            print(data)
            return 0
    else:
        sys.stdout.write('\r\033[K已是登录状态')
    return sessKey
proxies = {'http':'34.92.3.74:3654'}
recording = []
trytimes = input('重试次数')
threads = input('线程数')
firsturl = 'http://www.winktv.co.kr/'
checkurl = 'http://api.winktv.co.kr/member/loginInfo'
loginurl = 'http://api.winktv.co.kr/member/login'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'}
cookies={
    "userReferer":"http%3A%2F%2Fm.winktv.co.kr%2F",
    "3be3f8e358abbf54cec643229de77fc9e4f3f0bbc9b171580d45d13aaa374c16":"cbBdywJQMNHin%2FURMhawoC6M9EXUorlB2J2YgAAFgfMoWUGXOMFQf1Xjrh6FRI5HwTXUBYwjOmm6jPly81XpIWFp5rw4IMcjo5ME445Nd%2FlJ0LAbS45z0e2OMHFbeix75eeXylarfAsutBPT9qrmWYTEceVmvpir6CLD5ugE4EQg1qpouvB62l%2F0lH6iOf5y",
    "userLoginSaveYN":"Y",
    "userLoginYN":"Y",
    "userLoginIdx":"10949389",
    "partner":"winktv",
    "sessKey":"abe3c9b81d61a3a557018f042ad62b8addbdb3a5a2b9ac01703fd8dec88d2438"
}

s = requests.session()
s.cookies.update(cookies)
s.headers.update(headers)
r = s.get(firsturl,timeout=10)
r.close()
sessKey=s.cookies['sessKey']
test = input('测试？\n')
while 1:
    sessKey = login(sessKey)
    if sessKey:
        break
    time.sleep(random.randint(1,5))
searchd = {
    "Y6K2VQRw0MfwbPfZ4Dna":"117",
    "AYNUR1c5v-yi4dNLpZWlOU":"78",
    "AYUcvzSBe-yi4dNLpZWlOU":"",
    "_i3nY6v7ot9WIAugPuZ6Pj3WlOU":"UXTHn1wARzfIPweF5cRopzGLoQKtqw7PTgWS7c65ob6onyWoODKayxnNGcNtWb7s4ZPhu1igSxotvtVIv2TLrQmkSzEU92rBvtA9Y_ChOsWVbDEVClcJWpUM8CEgqSWN8IcDzjrMvtVInZTLbSNprEhxikWw7pVInyTLrQlpbDGavmWS4c9so1PlNSLxbE8FfmrR7dQMIcTpnyVku2JePkYU4dNAocP67SPZrDig9ksPvo9LobTAaynhB26DTmrSTtHQ8cDcNtlN8IGDD3uthl",
    "Yt40SkS4eFP1sNLe4Dna":"1581831342",
    "AYohuyc98ugPuZ6Pj3WlOU":"73e182930a30e01cb66ac6a444d4aacb1d35f5d86131b504fce516d02915824b",
    "yQv1sB81otLfILAZU_XYXoaA":"abe3c9b81d61a3a557018f042ad62b8addbdb3a5a2b9ac01703fd8dec88d2438",
    "o3GVexFtLZADj4Idn1w0S34Bzo":"36d0886e3f3772c151d0f6a0082a2f0e79af9ffdecef1327790fa1674b74260e",
    "YtK1kkS4aBf-Yxfc4Dna":"webMobile",
    "y6RycBO1oZLfADX_9tKZXoaA":"1.0.0"
}

searchurl = 'http://api.winktv.co.kr/live/bookmark'
while 1:
    try:
        r = s.post(searchurl,data=searchd,proxies=proxies,timeout=10)
        data=r.json()
    except Exception as e:
        print(e)
        continue#exit(1)
    try:
        roomlist = data['list']
    except:
        print('获取列表失败')
        sessKey = login(sessKey)
        continue
    page = data['page']
    limit = page['limit']
    total = page['total']
    for i in roomlist:
        user_id = i['userId']
        if not 'media' in i:
            continue
        media=i['media']
        code = media['code']
        isLive = media['isLive']
        isGuestLive = media['isGuestLive']
        _type = media['type']
        if (_type == 'free' or user_id == 'deer9898') and user_id not in recording:
            if test:
                download(user_id,code,sessKey)
            else:
                a = Thread(target=download,args=(user_id,code,sessKey,),name=user_id,daemon = True)
                a.start()
    sys.stdout.write(f"\r\033[K正在录制{len(recording)}")
    isLogin,sessKey = checklogin(sessKey)
    time.sleep(random.choice(range(5,10)))
