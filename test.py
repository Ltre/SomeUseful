#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

#import tracemalloc
#tracemalloc.start()
import os, sys,asyncio,concurrent,functools,shutil
#import uvloop
#asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
#os.system('cd /root/b/d;mv *.flv /root/b/d/bu/')
from os.path import split, join, exists, abspath, isdir, expanduser
import re
#import logging
import json
import threading
import urllib.request
import urllib.error
from urllib.request import urlopen#, Request
import time
import io
import socket
import subprocess
import argparse
import http.client
import configparser,traceback
from mail import send_mail
import toml
import aiohttp
import gc

password = input('password:')
testt = input('test?')
ROOMS = '';
USERS = '';
FILEDIR = '';
#DEBUGLEVEL = logging.INFO;
SCRIPT = '';
COMMAND = '';
INTERVAL = 5;
ipnum = 0;
recording = []
mvselect=1
cookies = {}
access_key = ''

sApi0 = 'http://space.bilibili.com/ajax/live/getLive?mid={}'
sApi1 = 'http://live.bilibili.com/api/player?id=cid:{}';
sApi2 = 'http://live.bilibili.com/live/getInfo?roomid={}';  # obsolete
sApi3 = 'http://live.bilibili.com/api/playurl?cid={}';      # obsolete
sAPI4 = 'https://api.live.bilibili.com/room/v1/Room/room_init?id={}'
sApi5 = 'http://api.live.bilibili.com/room/v1/Room/get_info?room_id={}'
sApi6 = 'http://api.live.bilibili.com/live_user/v1/UserInfo/get_anchor_in_room?roomid={}'
sApi7 = 'http://api.live.bilibili.com/api/playurl?cid={}&otype=json&quality=0&platform=web'
sApi8 = 'http://api.live.bilibili.com/room/v1/Room/playUrl?cid={}&otype=json&platform=web&qn=4'
headers={
        "Connection":"close",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
        "Accept":"*/*",
        "Referer":"https://space.bilibili.com/1836737/fans/follow",
        "Accept-Encoding":"gzip, deflate, br",
        "Accept-Language":"zh-CN,zh;q=0.9,ja;q=0.8",
        "Cookie":"buvid3=DF8F84B3-B90F-4D48-AF16-6ECF24C8BAA540777infoc; LIVE_BUVID=AUTO2015577399215380; sid=6znidvkl; DedeUserID=1836737; DedeUserID__ckMd5=326caeb00bc9daa3; SESSDATA=34f5f194%2C1560331941%2C35fcf151; bili_jct=9c0eebb9461bc14a8c855818a27b48c6; _dfcaptcha=b761810cd8d5d6835ab4d99a536ac018"
        }

aRooms = [];
sHome = '';
sSelfDir = '';
sLogDir = '';
log = None;
sleepEvent = None;
wait = None;
selectip = None

vfs=os.statvfs("/root")
available=vfs.f_bavail*vfs.f_bsize/(1024*1024*1024)

import requests
import random
ii=0


import ssl
from multiprocessing import Process, Value
upwork = Value("d",0)
sys.path.append('/root/u')
#from getip import *

ssl._create_default_https_context = ssl._create_unverified_context

#logging.basicConfig(format='    %(asctime)s %(levelname)-5s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S');
#log = logging.getLogger(__name__);
#log.setLevel(DEBUGLEVEL);
sleepEvent = threading.Event();
wait = sleepEvent.wait;


ss = requests.session()
ss.keep_alive = False


def delete_proxy(proxy):
    with requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy)) as r:
        print(r.text)

def get_proxy():
    while True:
        try:
            with ss.get("http://127.0.0.1:5010/get",timeout=20) as r:
                ip = r.json().get("proxy")
            return ip
        except:
            time.sleep(0.1)

proxyg={'http':get_proxy()}#getip('国内')
streamip = []
allips = []
def prepare(room,s=None):
    global sHome
    global sSelfDir
    global sLogDir
    global log
    global sleepEvent
    global wait
    
    global ii
    global ipnum

    '''
    config = configparser.ConfigParser()
    config.read(sys.path[0] + "/proxy.ini")
    try:
        sourceip = socket.gethostbyname(config.get('proxy','ip'))
        r = requests.get('http://%s:8765/?count=1000&protocol=1' % sourceip,timeout=10)
    except Exception as e:
        sourceip = "127.0.0.1"
        r = requests.get('http://%s:8765/?count=1000&protocol=1' % sourceip,timeout=10)
    try:
        ip_ports = json.loads(r.text)
    except Exception as e:
        print(e)
        time.sleep(0.1)
        prepare(room)
        return
    print("数量：")
    print(len(ip_ports))
    ipnum=int(len(ip_ports))
    try:
        ip = ip_ports[ii][0]
    except Exception as e:
        print(e)
        try:
            r = requests.get('http://%s:8765/?count=1000&protocol=1' % sourceip,timeout=10)
            ip = ip_ports[ii][0]
        except Exception as e:
            ii += 1
            if(ii>=ipnum):
                ii=0
            prepare(room)
            return
    port = ip_ports[ii][1]    
    proxies={'https':'%s:%s'%(ip,port)}
    print('取用第{}个IP地址：{}\n'.format(ii+1,proxies))
    ii += 1
    if(ii>=ipnum):
        ii=0
    '''
    
    while True:
    
        try:
            #r = ss.get('http://127.0.0.1:5010/get',timeout = 20)
            room.ip=ip = get_proxy()
            break
        except Exception as e:
            print(e)
            time.sleep(1)
    if s=='s':
        proxies={'https':ip}
    elif s =='国内':
        pass#proxies=getip(s)
    else:
        proxies = {'http':ip}#,'https':ip}
    #proxies=getip('s')
    print(proxies)
    proxy_support = urllib.request.ProxyHandler(proxies)
    
    sHome = expanduser('~')
    sSelfDir = split(__file__)[0];
    #sLogDir = join(sSelfDir, 'multilisten.log.d');
    #logging.basicConfig(format='    %(asctime)s %(levelname)-5s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S');
    #log = logging.getLogger(__name__);
    #log.setLevel(DEBUGLEVEL);
    sleepEvent = threading.Event();
    wait = sleepEvent.wait;
    opener = urllib.request.build_opener(proxy_support);
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36')];
    #urllib.request.install_opener(opener);
    room.urlopen=opener.open
    socket.setdefaulttimeout(30);
#prepare();

#os.system("apt install -y yamdi ffmpeg libffi-dev libssl-dev")

def display(*args, **kargs):
    try:
        print(*args, **kargs);
    except UnicodeEncodeError as e:
        sEnc = sys.stdout.encoding;
        args = (str(x).encode(sEnc, 'replace').decode(sEnc) for x in args);
        print(*args, **kargs);

class Room():
    def __init__(self, nRoom=None, nUser=None,sUser=None,sTitle=None,sUrl=None):
        global log
        self.nRoom = int(nRoom or 0);
        self.nUser= int(nUser or 0);
        self.nId = int(nRoom or 0);
        self.aurl = None
        self.sUrl = sUrl;
        self.burl = None;
        self.curl = None;
        self.sTitle = sTitle;
        self.sUser = sUser;
        self.sStatus = None;
        self._stream = io.StringIO();
        self.thread = None;
        self.checkthread = None;
        self.ii = 1;
        self.sameid = 1;
        self.ex = 0;
        self.urlopen = None;
        self.ip = None
        #print({key: value for key, value in vars(self).items() if not key.startswith('_') and value});
    def getRoomByUser(self):
        assert self.nUser;
        try:
            res0 = self.urlopen(sApi0.format(self.nUser));
            sData = res0.read().decode('utf-8');
            assert sData;
            mData = json.loads(sData);
            if (mData['status']):
                self.nId = self.nRoom = int(mData['data']);
                return True;
            else:
                display('不存在的播主: ', self.nUser);
                return False;
        finally:
            if ('res0' in locals()): res0.close();
    def getRealId(self):
        global log
        try:
            #sUrl = 'http://live.bilibili.com/{}'.format(self.nRoom);
            #res = urlopen(sUrl);
            #bData = res.read(5000);
            #match = re.search(rb'var ROOMID = (\d+);', bData);
            #if (match):
            #    nId = int(match.group(1));
            #else:
            #    nId = self.nRoom;
            res1 = self.urlopen(sAPI4.format(self.nRoom));
            bData = res1.read();
            mData = json.loads(bData.decode());
            nId = mData['data']['room_id'];
        except urllib.error.HTTPError as e:
            if (e.code == 404):
                print('room {} not exists'.format(self.nRoom));
                return False
            else:
                delete_proxy(self.ip)
                raise
        else:
            self.nId = nId;
            return True
        finally:
            if ('res1' in locals()): res1.close();
    def getHost(self):
        if (self.sUser is None):
            try:
                print(self.nId,"getHost")
                f11 = self.urlopen(sApi6.format(self.nId));
                bData = f11.read();
                mData = json.loads(bData.decode());
                Username = mData['data']['info']['uname'];
                rstr = r"[\/\\\:\*\?\"\<\>\|\- ]"
                self.sUser = re.sub(rstr,"_",Username)
            except Exception as e:
                display('获取播主失败: ', e);
                prepare(self)
                self.getHost()
                #self.sUser = '';
            finally:
                if ('f11' in locals()): f11.close();
        rstr = r"[\/\\\:\*\?\"\<\>\|\- ]"
        self.sUser = re.sub(rstr,"_",self.sUser)
    def getInfo(self,g=None):
        global log
        global sApi5, sApi6  
        while True: 
            try:
                if (self.nId is None): self.getRealId();
                if not self.sTitle or g:
                    print(self.nId,"getInfo")
                    res2 = self.urlopen(sApi5.format(self.nId),timeout=10);
                    sRoomInfo = res2.read().decode('utf-8');
                    mData = json.loads(sRoomInfo);
                    self.sTitle = sTitle = mData['data']['title'];
                self.getHost();
                rstr = r"[\/\\\:\*\?\"\<\>\|\-\. ]"
                self.sTitle = re.sub(rstr,"_",self.sTitle)
                nStatus = 1#mData['data']['live_status'];
                _status = 'on' if nStatus == 1 else 'off';
                self.sStatus = _status;
            except Exception as e:
                print('failed to get room info: {}'.format(e));
                traceback.print_exc()
                
                prepare(self);
                #raise;
            else:
                return _status;
            finally:
                if ('res2' in locals()): res2.close();
    def getStream(self):
        #global sApi3
        #with urlopen(sApi3.format(self.nId)) as res:
        #    sData = res.read().decode('utf-8');
        #iMatches = re.finditer(r'<(?:b\d)?url><!\[CDATA\[(.+)\]\]><\/(?:b\d)?url>', sData);
        #aMatches = list(iMatches);
        #if (aMatches):
        #    self.aUrls = [x.group(1) for x in aMatches];
        #    sUrl = self.sUrl = self.aUrls[0];
        #    return sUrl;
        #else:
        #    return False;
        global sApi8#,selectip
        trytimes = 10
        if self.sUrl:
            return True
        else:
            print(self.nUser,"开始未能获得url，用备用方法获取")
        '''
        if self.nId == 151159:
            proxies = None
        else:
        '''
        def newip():
            print('streamip:',len(streamip))
            if not streamip:
                selectip = get_proxy()
            else:
                selectip = streamip[random.randint(0,len(streamip)-1)]
            proxies={'http':selectip,'https':selectip}#getip('国内')
            return selectip,proxies
        
        #print(self.nRoom,'getStream',proxies)
        while trytimes:
            selectip,proxies = newip()
            try:
                with requests.get(sApi8.format(self.nId),timeout=5,proxies=proxies) as res:
                    sData=res.json()
                    mData = sData['data']
                    if not mData['accept_quality']:
                        raise Exception("调用出错")
                    #mData = json.loads(sData);
                    durl = mData['durl']
                    for i in durl:
                        url = i['url']
                        if 'live-bvc' in url:
                            self.aurl = url
                        elif 'live-js' in url:
                            self.burl = url
                        elif 'live-txy' in url:
                            self.curl = url
                    self.ip = selectip
                        
                    print(self.sUser,"获取url成功")
                    if not selectip in streamip:
                        streamip.append(selectip)
                        print(streamip)
                    return 1;
                    #sData = res.read().decode('utf-8');
            except Exception as e:
                #delete_proxy(ip)
                if 'ss' in locals():
                    ss.close()
                print(self.sUser,'获取url失败')
                if selectip in streamip:
                    streamip.remove(selectip)
                #traceback.print_exc()
                trytimes -=1
                time.sleep(0.1)
                #prepare(self,'国内')
            #mData = json.loads(sData);
        return False
        

    def download(self, sPath, stream=sys.stdout, nVerbose=1):
        sDir = expanduser(FILEDIR) or sHome;
        def adaptName(sPath):
            if (os.path.exists(sPath)):
                sName, sExt = os.path.splitext(sPath)
                i = 1;
                sOutPath = '{}{}{}'.format(sName, i, sExt);
                while os.path.exists(sOutPath):
                    i += 1;
                    sOutPath = '{}{}{}'.format(sName, i, sExt);
            else:
                sOutPath = sPath;
            return sOutPath;
        def newName():
            sTime = time.strftime('%y%m%d_%H%M%S');
            sName = '{}-{}-{}.flv'.format(sTime, self.sUser, self.sTitle);
            sName = re.sub(r'[^\w_\-.()]', '_', sName);
            sPath = os.path.join(sDir,sName)
            return sPath
        proxyg = {};
        selectip = None
        def newdown(proxyg = proxyg,selectip=selectip,pro = 0):#pro:是否代理
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36', 'Referer': 'https://live.bilibili.com/{}'.format(self.nId)}
            if not proxyg and pro:
                proxyg['https']=selectip
                proxyg['http']=selectip
            #proxyg = {'http':'34.92.99.59:3247'}
            timeout = 10
            hasproxy = 0
            while 1:
                try:
                    if self.burl:
                        proxyg = 0
                        sUrl = self.sUrl = self.burl
                    elif self.aurl:
                        proxyg = {'http':self.ip}
                        sUrl = self.sUrl = self.aurl
                    elif self.curl:
                        if hasproxy:
                            proxyg = {'http':self.ip}
                        else:
                            proxyg = 0
                        sUrl = self.sUrl = self.curl
                    with requests.get(sUrl,stream = True,timeout = timeout,headers=headers,proxies=proxyg) as r:
                        if r.status_code == 200:
                            for chunk in r.iter_content(chunk_size=1024):
                                if chunk:
                                    yield chunk
                                else:
                                    yield None
                        elif r.status_code == 302:
                                self.burl = r.headers.get("Location")
                        elif r.status_code == 403 and not hasproxy:
                            hasproxy = 1
                            continue
                        else:
                            break
                except Exception as e:
                    if "timed" in str(e) or "refused" in str(e):
                        if not hasproxy:
                            hasproxy=1
                        else:
                            break
                    else:
                        print('newdown 的错误是',e)
                        break
            if not 'r' in locals():
                print('url 未接通')
                yield None
            if r.status_code !=200:
                print('url get error',r.status_code)
                yield None
            
        sUrl = self.sUrl;
        bBuffer = ''
        data = ''
        if True:
            try:
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'}
                raise Exception('403')
                req=urllib.request.Request(sUrl,headers=headers)
                r=urlopen(req)
                #r = urlopen(sUrl, timeout=4)
            except Exception as e:
                #print(self.sUser,e,'主线中断，切换备线\n')
                #aaaa=self.getStream()
                #if aaaa:
                #    sUrl = self.ssUrl
                #else:
                #    return False,sPath
                '''
                while True:
                    try:
                        r = urlopen(sUrl, timeout=20)
                    except Exception as e:
                        print(e)
                        if "403" in str(e):
                            print(self.sUser,'被拒，继续尝试')
                        else:
                            break
                '''
                try:
                    if '4' in str(e):
                        data = newdown()
                        if data:
                            bBuffer = data.__next__()
                        else:
                            return False,sPath
                    else:
                        r = urlopen(sUrl, timeout=5)
                except Exception as e:
                    traceback.print_exc();
                    print(self.sUser,e,'失败\n')
                    return False,sPath
                '''
                    sUrl = self.ssUrl
                    try:
                        r=urlopen(sUrl,timeout=5)
                    except Exception as e:
                        print(e)
                        return False,sPath
                '''
            except socket.timeout as e:
                print(e)
                return False,sPath
            else:
                pass
        sPath = newName();
        sPath = adaptName(sPath);
        #iUrls = iter(aUrl);
        #sUrl = next(iUrls);
        try:
            if bBuffer:
                f1 = open(sPath, 'wb');
                print('{} starting download from:\n{}\n    to:\n{}'.format(self.nId, self.sUrl, sPath));
            if (nVerbose):
                stream.write('\n');
            nSize = 0;
            n = 1024*1024;
            readbuffer = 1024*8
            tnumber = 0
            #vfs=os.statvfs("/root")
            #available=vfs.f_bavail*vfs.f_bsize/(1024*1024*1024)
            #stream.write('\r剩余空间%.2f\n' % (available))
            while bBuffer:
                nSize += f1.write(bBuffer);
                #f1.flush()
                #if (nVerbose):
                    #stream.write('\r{:<4.2f} MB downloaded'.format(nSize/n));
                #tnumber+=1               
                #if (tnumber>=200):
                    #break
                    #vfs=os.statvfs("/root")
                    #available=vfs.f_bavail*vfs.f_bsize/(1024*1024*1024)
                    #stream.write('剩余空间%.2f\n' % (available))
                    #tnumber = 0
                if (nSize/n >= 1024 and self.nId != 151159):
                    print('%s 大小到达限制，进行存储\n' % sPath)
                    if 'r' in locals():
                        print("关闭上一个链接")
                        r.close()
                    nSize = 0
                    f1.close()
                    upload(sPath)
                    '''
                    sTime = time.strftime('%y%m%d_%H%M%S');
                    sName = '{}-{}-{}.flv'.format(sTime, self.sUser, self.sTitle);
                    sName = re.sub(r'[^\w_\-.()]', '_', sName);
                    sPath = os.path.join(sDir,sName)
                    '''
                    sPath = newName()
                    f1 = open(sPath,'wb')
                    data = newdown()
                #if (self.ii == 0 and available>25):
                #    self.ii = 1
                #if (available<15 and (self.ii == 1 and self.nId !=151159)):
                #    self.ii = 0
                #    print('剩余空间不足，进行存储\n')
                #    stillrec = 1
                #    break
                if data:
                    bBuffer = data.__next__()
                else:
                    bBuffer = res.read(readbuffer);
                trytry=0
                waittime = 0.2
                '''
                while not bBuffer and trytry <2:
                    time.sleep(waittime)
                    try:
                        #res = urlopen(sUrl, timeout=25);
                        data=newdown()
                    except:
                        break
                    bBuffer = data.__next__()
                    #bBuffer = res.read(1024*128);
                    trytry+=1
                    waittime+=0.1
                '''

            #if (nVerbose):
                #stream.write('\n');
        except StopIteration:
            print('{} 数据流结束'.format(self.sUser))
        except socket.timeout as e:
            print('{} donwloading timeout'.format(self.nId));
        except ConnectionResetError as e:
            print('downloading reset: {}'.format(e));
        except http.client.IncompleteRead as e:
            print('downloading break:{}'.format(e));
        except:
            traceback.print_exc()
        finally:
            if ('res' in locals()): 
                res.close();
            if ('r' in locals()): 
                r.close();
            if ('f1' in locals()): f1.close();
            if (os.path.isfile(sPath) and os.path.getsize(sPath) < 1024*1024):
                os.remove(sPath);
                return False,None;
            return True,sPath;

def doCleanup(room, sPath, sScript=None, sCom=None, sLogFile=None):
    # execute external script
    # maybe in a new thread
    global COMMAND, SCRIPT
    global log
    global sSelfDir
    global sLogDir
    sScript = (sScript or SCRIPT or '').strip();
    sCom = (sCom or COMMAND or '').strip();
    sLogFile = '{}.log'.format(room.nId);
    if (sLogDir):
        if (not exists(sLogDir)):
            os.mkdir(sLogDir);
        if (isdir(sLogDir)):
            sLogFile = join(sLogDir, sLogFile);
        else:
            sLogFile = os.devnull;
    else:
        sLogFile = os.devnull;
    try:
        file = open(sLogFile, 'a');
        if (sScript):
            sScriptOri = sScript;
            if (not exists(sScript)):
                sScript = join(sSelfDir, sScriptOri);
            sScript = abspath(sScript);
            try:
                subprocess.Popen(
                        [sys.executable, sScript, sPath],
                        stdout=file,
                        stderr=subprocess.STDOUT
                );
            except FileNotFoundError as e:
                print('executing script {} failed: {}'.format(sScript, e));
            else:
                print(r'executing cleanup script "{}" with file "{}", logging to "{}"'
                        .format(sScript, sPath, sLogFile)
                );
        if (sCom):
            sCom = sCom.format(sPath);
            try:
                subprocess.Popen(
                        sCom,
                        stdout=file,
                        stderr=subprocess.STDOUT,
                        shell=True
                );
            except FileNotFoundError as e:
                print('executing command {} failed: {}'.format(sCom, e));
            else:
                print(r'execute cleanup command "{}", logging to "{}"'
                        .format(sCom, sLogFile)
                );
    finally:
        if ('file' in locals()): file.close();
    return True;


def upload(sPath):
    global mvselect
    
    if(not os.path.exists('/root/b/d/bu')):
        os.makedirs('/root/b/d/bu')
    if mvselect==1:
        shutil.move(sPath,'/root/b/d/bu')
        mvselect+=1
    elif mvselect==2:
        shutil.move(sPath,'/root/b/d/bu/bt')
        mvselect+=1
    elif mvselect>=3:
        shutil.move(sPath,'/root/b')
        mvselect=1
    #exit()
    '''
    jishu=0;
    change ='waitting'+sName
    cPath = os.path.join(sDir, change)
    #global upwork
    while upwork.value>1:
        time.sleep(random.randint(0,20))
    upwork.value += 1
    os.system('ffmpeg -i "{}" -y -vcodec copy -acodec copy "{}"'.format(sPath,cPath))
    os.system('rm -rf "{}"'.format(sPath))
    os.system('yamdi -i "{}" -o "{}"'.format(cPath,sPath))
    os.system('rm -rf "{}"'.format(cPath))
    #upwork.value -= 1
    while True:
        wait(0.5);
        if(not room.sUser):
            room.getHost()
            sPaths=re.split(r'[-]{2}',sPath)
            if(len(sPaths)==2):
                nPath=sPaths[0]+'-'+room.sUser+'-'+sPaths[1]
                os.system('mv "{}" "{}"'.format(sPath,nPath))
                sPath = nPath
        os.system('rclone move "{}" milo:milo/b/"{}"'.format(sPath,room.sUser));
        if(not exists(sPath)):
            print('{}存储成功..'.format(sName));
            if(room.ii == 0):
                room.ii = 1
            break;
        else:
            if(jishu>=10):
                print('重试多次失败，请手动检查');
                with open('/root/names.txt','a') as f:
                    f.writelines(sName);
                    f.write('\n')
                    f.close;
                    break;
            jishu+=1;
            print('存储失败，重新存储..\n')
            time.sleep(5)
    upwork.value -= 1
   ''' 

def doDownload(room):
    global mvselect
    global FILEDIR, sHome;
    global wait;
    global sLogDir;
    sDir = expanduser(FILEDIR) or sHome;
    sTime = time.strftime('%y%m%d_%H%M%S');
    sName = '{}-{}-{}.flv'.format(sTime, room.sUser, room.sTitle);
    sName = re.sub(r'[^\w_\-.()]', '_', sName);
    if (not exists(sDir)):
        os.makedirs(sDir);
    assert isdir(sDir);
    sPath = os.path.join(sDir, sName);
    isSuccess = room.getStream();
    if (isSuccess):
        isSuccess,sPath = room.download(sPath, room._stream)
        if (isSuccess):
            print('{} downloaded to {}'.format(room.nId, sPath));
            try:
                #downThread = threading.Thread(
                #          target=upload,
                #         name=str(room.nId),
                #         args=(room,sPath,sName,sDir,),
                #         daemon=True
                # );
                # downThread.start();
                '''
                p = Process(target=upload, args=(room,sPath,sName,sDir,upwork,))
                print('Child process will start.')
                p.start()
                '''
                if os.path.exists(sPath):
                    upload(sPath)
            except Exception as e:
                if (sLogDir):
                    if (not exists(sLogDir)):
                        os.mkdir(sLogDir);
                    if (isdir(sLogDir)):
                        sLogFile = 'threaderror.log'
                        sLogFile = join(sLogDir, sLogFile);
                        with open(sLogFile, 'a') as file:
                            file.write('\n{}:\n  {}\n'.format(time.ctime(), e));
                        print('error "{}" is logged to file "{}"'
                                .format(e, sLogFile)
                        );
                raise
        #wait(2);
    room._stream.seek(0);
    room._stream.truncate();
    print('{} download thread ended'.format(room.nId));
    #os.system('rclone move {} milo:milo/b'.format(sDir));

    return True;

def checkuser():
    global aRooms
    while True:
        #print('check run')
        for i in open("user.txt","r").read().splitlines():
            if(i):
                sameid = 0 
                for room in aRooms:
                    if(int(i) == room.nRoom):
                        sameid =1
                        room.ex = 1
                        #room.sameid = 1
                        break
                if(sameid == 1):
                    continue
                else:
                    print('find new id:%s.' % i)
                    room = Room(int(i));
                    room.sameid = 1
                    room.ex = 1
                    #room.getInfo();
                    aRooms.append(room)
        for room in aRooms:
            if(room.ex == 0):
                print("{}end".format(room.nRoom))
                aRooms.remove(room)
                room.sameid = 0
            room.ex = 0
        time.sleep(5)

def synMonitor(aIds=None, aUsers=None):
    global log
    global wait
    global aRooms;
    global INTERVAL;
    if (not aIds): aIds = [];
    if (not aUsers): aUsers = [];
    aRooms = [];
    if (not os.path.exists('user.txt')):
        with open("user.txt","a") as f:
            for sId in aIds:
                sId = sId.strip();
                if (sId):
                    f.writelines(sId)
                    f.write('\n')
            f.close
    else:
        for sId in aIds:
            sId = sId.strip();
            if (sId):
                sameid = 0
                for i in open("user.txt","r").read().splitlines():
                    if (i == sId):
                        sameid = 1
                        break
                if(sameid == 1):
                    continue
                else:
                    with open("user.txt","a") as r:
                        r.writelines(sId)
                        r.write('\n')
                        r.close
            
    for sId in open("user.txt","r").read().splitlines():
        sId = sId.strip();
        if (sId):
            room = Room(int(sId));
            #room.getInfo();
            aRooms.append(room);
    for sUser in aUsers:
        sUser = sUser.strip();
        if (sUser):
            room = Room(None, int(sUser));
            if (room.getRoomByUser()):
                room.getInfo();
                aRooms.append(room);
    #for room in aRooms:
        #display('id: {}\nUser: {}\nroom: {}\nstatus: {}\n'.format(room.nId, room.sUser, room.sTitle, room.sStatus))
    print('check interval: {}s'.format(INTERVAL));
    ck = threading.Thread(target=checkuser,name=("check"),daemon=True)
    ck.start()
    while True:
        for room in aRooms:
            if(room.checkthread and room.checkthread.is_alive()):
                pass
            else:
                print('new checkthread {} running'.format(room.nRoom))
                checkThread = threading.Thread(target=checkrun,
                                               name=str(room.sUser),
                                               args=(room,),
                                               daemon=True
                                              )
                room.checkthread=checkThread
                checkThread.start()                
        wait(INTERVAL);

def checkrun(room):
    if str(room.nRoom) in recording:
        return
    recording.append(str(room.nRoom))
    #x = 1
    prepare(room)
    isOn = (room.getInfo() == 'on');
    display('id: {}\nUser: {}\nroom: {}\nstatus: {}\n'.format(room.nId, room.sUser, room.sTitle, room.sStatus))
    '''
    if (room.thread and room.thread.is_alive()):
        sProcess = room._stream.getvalue();
        print('{} downloading process: {}'.format(room.nId, sProcess));
    '''
    if(room.sameid == 0):
        return
    #if(isOn and x==1):
    #    x=0
    #else:
    #    isOn = (room.getInfo() == 'on');
    if(isOn):
        print('{} starting download process...'.format(room.nId));
        '''
        downThread = threading.Thread(
                target=doDownload,
                name=str(room.nId),
                args=(room,),
                daemon=True
        );
        room.thread = downThread;
        downThread.start();
        '''
        doDownload(room)
        if str(room.nRoom) in recording:
            recording.remove(str(room.nRoom))
    else:
        if str(room.nRoom) in recording:
            recording.remove(str(room.nRoom))
        gc.collect()#pass

def newgetonline():
    global cookies
    count = 0
    firstnew=1
    s=requests.session()
    s.keep_alive = False
    headers={"APP-KEY": "iphone","Accept": "*/*","Accept-Encoding": "gzip","Accept-Language": "zh-cn","Buvid": "a3ed675c322d0d658f8a0e69711fb011","Display-ID": "1836737-1562074723","ENV": "prod","User-Agent": "bili-universal/8680 CFNetwork/976 Darwin/18.2.0",}
    '''
    headers={
            "Connection":"close",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
            "Accept":"*/*",
            "Referer":"https://space.bilibili.com/1836737/fans/follow",
            "Accept-Encoding":"gzip, deflate, br",
            "Accept-Language":"zh-CN,zh;q=0.9,ja;q=0.8"}

    cookies={
            "Cookie": "DedeUserID=1836737; DedeUserID__ckMd5=326caeb00bc9daa3; SESSDATA=20accd85%2C1566356211%2C0d93fe71; bili_jct=f10fa7a864b930767ec42e4f42968c4a; sid=4hbm9tko; Buvid=a3ed675c322d0d658f8a0e69711fb011; LIVE_BUVID=AUTO1915506501046439; buvid3=FC7A064A-214F-42CD-A34B-E62B8E670B1248780infoc; finger=50e304e7; Hm_lvt_8a6e55dbd2870f0f5bc9194cddf32a02=1557239028"
            }
    '''
    s.headers.update(headers)
    s.cookies.update(cookies)
    #proxies = None#getip('国内')
    while not streamip:
        time.sleep(1)

    ip = streamip[random.randint(0,len(streamip) - 1)]
    proxies = {'https':ip,'http':ip}
    print("getrec",proxies)
    while True:
        xx = time.time()
        try:
            t=1
            #url = 'http://api.live.bilibili.com/relation/v1/feed/feed_list?page={}&pagesize=30'.format(t)
            #url = f"https://api.live.bilibili.com/xlive/app-interface/v1/relation/liveAnchor?access_key={access_key}&&build=8680&device=phone&device_name=iPhone%208&filterRule=0&mobi_app=iphone&platform=ios&qn=0&sign=9f94e7fbbcbbdb375d75d631512ad5ba&sortRule=1&statistics=%7B%22appId%22%3A1%2C%22version%22%3A%225.44.1%22%2C%22abtest%22%3A%22716%22%2C%22platform%22%3A1%7D&ts=1562074989"
            url = f"http://api.live.bilibili.com/xlive/app-interface/v1/relation/liveAnchor?access_key={access_key}&actionKey=appkey&appkey=27eb53fc9058f8c3&build=8910&device=phone&device_name=iPhone%208&filterRule=0&mobi_app=iphone&platform=ios&qn=0&sign=0f9c9e3978d6bde09f2621d03c51269e&sortRule=1&statistics=%7B%22appId%22%3A1%2C%22version%22%3A%225.48.2%22%2C%22abtest%22%3A%22890_886_519%22%2C%22platform%22%3A1%7D&ts={int(time.time())}"#1562074989"
            with s.get(url,proxies=proxies,timeout=3) as req:
                res=req.json()
            data=res.get('data')
            online= []
            infos={}
            if not data:
                contents = 'bilibili cookies 失效'
                print(res)
                subject = 'bilibili'
                send_mail(subject,contents,password)
                time.sleep(60)
            
            else:
                online.extend(str(m['roomid']) for m in data['rooms'])
                for m in data['rooms']:
                    infos.update({str(m['roomid']):{'uname':m['uname'],'title':m['title'],'playurl':m['playurl']}})
            '''
            while data.get('list'):
                #online.extend([str(m['roomid']) if str(m['roomid']) == m['link'].split('/')[-1] else m['link'].split('/')[-1] for m in data['list']])
                #online.extend([m['link'].split('/')[-1] for m in data['list']])
                online.extend(str(m['roomid']) for m in data['list'])
                for m in data['list']:
                    infos.update({str(m['roomid']):{'uname':m['uname'],'title':m['title']}})
                t+=1
                url = 'http://api.live.bilibili.com/relation/v1/feed/feed_list?page={}&pagesize=30'.format(t)
                data = s.get(url,proxies=proxies,timeout=10).json().get('data')
            ''' 
            f=open('/root/u/user.txt','r')
            uids=list(set(f.read().splitlines()))
            wanted = [m for m in list(set(online)) if (m in uids and m not in recording)]
            if len(wanted):
                if firstnew:
                    print('rec 更新')
                    firstnew=0
                    continue
                sys.stdout.write("\033[K")
                print('rec',len(wanted),wanted)
                for user in wanted:
                    room = Room(int(user),sUser=infos[user]['uname'],sTitle=infos[user]['title'],sUrl=None)#infos[user]['playurl'])
                    thread = threading.Thread(target = checkrun,name=infos[user]['uname'],args = (room,),daemon = True)
                    thread.start()
                    if testt == '1':
                        thread.join()
            f.close()
        except Exception as e:
            print(e)
            if streamip:
                ip = streamip[random.randint(0,len(streamip) - 1)]
            else:
                ip = allips.pop(0)
                allips.append(ip)
            proxies = {'https':ip,'http':ip} 
            #print(req)
            print("getrec",proxies)
            if '403' in str(e):
                getcookies()
        yy = time.time()
        if 'f' in locals():
            f.close()

        print('')
        sys.stdout.write('\033[K')
        sys.stdout.write('\033[F')
        print('\nrec updated',yy-xx,'s')
        '''
        if count<=0:
            count=5
            snapshot = tracemalloc.take_snapshot()
            top_stats = snapshot.statistics('lineno')
            for stat in top_stats[:2]:
                    sys.stdout.write('\033[K')
                    print(stat)
            sys.stdout.write('\033[2A')
        else:
            count-=1
        '''
        sys.stdout.write('\033[F')
        sys.stdout.write('\033[F')
        time.sleep(2)
def getfollow():
    global cookies
    headers ={
            "Connection":"close",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
            "Accept":"*/*",
            "Referer":"https://space.bilibili.com/1836737/fans/follow",
            "Accept-Encoding":"gzip, deflate, br",
            "Accept-Language":"zh-CN,zh;q=0.9,ja;q=0.8"}
    '''
    cookies={
            "Cookie": "DedeUserID=1836737; DedeUserID__ckMd5=326caeb00bc9daa3; SESSDATA=20accd85%2C1566356211%2C0d93fe71; bili_jct=f10fa7a864b930767ec42e4f42968c4a; sid=4hbm9tko; Buvid=a3ed675c322d0d658f8a0e69711fb011; LIVE_BUVID=AUTO1915506501046439; buvid3=FC7A064A-214F-42CD-A34B-E62B8E670B1248780infoc; finger=50e304e7; Hm_lvt_8a6e55dbd2870f0f5bc9194cddf32a02=1557239028"
            }
    '''
    s = requests.session()
    s.keep_alive = False
    s.headers.update(headers)
    s.cookies.update(cookies)
    proxies = None
    while True:
        try:
            curl='http://api.bilibili.com/x/relation/tags'
            with s.get(curl,proxies=proxies,timeout=10) as r:
                cdata = r.json()['data']
            flist = [m['tagid'] for m in cdata if (m['name'] =='直播' or m['name']=='舞蹈')]
            break
        except:
            print('get tags error,use old')
            flist = [96907,114130]
            break
            time.sleep(10)
    
    while True:
        x=time.time()
        fmid=[]
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=10)
        _process_pool = concurrent.futures.ThreadPoolExecutor(max_workers=10)
        atasks = []
        try:
            for i in flist:
                t=1
                furl = 'http://api.bilibili.com/x/relation/tag?mid=1836737&tagid={}&pn={}&ps=50'.format(i,t)
                with s.get(furl,proxies=proxies,timeout=10) as res:
                    fdata = res.json()
                fdata = fdata['data']
                while fdata:
                    fmid.extend([m['mid'] for m in fdata])
                    t+=1
                    furl = 'http://api.bilibili.com/x/relation/tag?mid=1836737&tagid={}&pn={}&ps=50'.format(i,t)
                    with s.get(furl,proxies=proxies,timeout=10) as res:
                        fdata = res.json()['data']
            fmid = list(set(fmid))
            with open('/root/u/checked_fmid.txt','a+') as f:
                f.seek(0)
                checked_fmid = f.read().splitlines()
            f2 = open ('/root/u/user.txt','r+')
            uids=list(set(f2.read().splitlines()))
            for i in fmid:
                if str(i) not in checked_fmid:
                    atasks.append(get_spider(i,loop,thread_pool,f2,uids,_process_pool,s))
            if atasks:
                loop.run_until_complete(asyncio.wait(atasks))
            y=time.time()
            sys.stdout.write('\033[K')
            print('follow update',y-x,'s')
            sys.stdout.write('\033[F')
        except Exception as e:
            print(fdata)
            traceback.print_exc()
            proxies ={'https':get_proxy()}#getip('国内')
            #print(e)
            print('getfollow',proxies)
        if 'f2' in locals():
            f2.close()
        loop.close()
        thread_pool.shutdown()
        _process_pool.shutdown()
        time.sleep(3)

async def get_spider(i,loop,thread_pool,f2,uids,_process_pool,s):
    rurl = 'http://api.live.bilibili.com/room/v1/Room/getRoomInfoOld?mid={}'.format(i)
    data = await loop.run_in_executor(thread_pool,functools.partial(_request,rurl,s))
    await loop.run_in_executor(_process_pool,functools.partial(get_header,data,f2,uids,i))
    
def _request(rurl,s):
    proxyg = {}
    t = 10
    while t:
        try:
            with s.get(rurl,proxies=proxyg,allow_redirects=False,timeout=10) as res:
                return res.json()['data']
        except Exception:
            ip = get_proxy()
            proxyg={'https':ip,'http':ip}#getip('国内')
            sys.stdout.write('\rget loopreq '+ip)
            sys.stdout.flush()
    return None



def get_header(data,f2,uids,i):
    if data:
        roomid = str(data['roomid'])
    else:
        roomid = None
    #live = 'https://live.bilibili.com/'+roomid
    '''
    live = sAPI4.format(oroomid)
    fake = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36' }
    try:
        jsons= requests.get(live,headers=fake,allow_redirects=False).json()
        rdata=jsons['data']
    #if rheader.get('Location'):
    #    roomid = rheader['Location'].split('/')[-1]
        roomid = str(rdata['short_id'] if rdata['short_id'] else rdata['room_id'])
    except:
        print(oroomid,jsons)
        return
    '''
    if roomid:
        if roomid not in uids:
            with open ('/root/u/user.txt','a') as f2:
                f2.write(roomid +'\n')
        with open ('/root/u/checked_fmid.txt','a+') as ff:
            ff.seek(0)
            if str(i) not in ff.read().splitlines():
                print(i,'写入')
                ff.write(str(i)+'\n')

def check_useful():
    global allips
    print('检查可用ip')
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    sem = asyncio.Semaphore(10)
    while True:
        ips = None
        while not ips:
            try:
                with requests.get("http://127.0.0.1:5010/get_all/",timeout = 5) as res:
                    ips = res.json()
            except:
                time.sleep(0.1)
        allips = ips
        tasks = [test(sem,ip.get('proxy')) for ip in ips]
        loop.run_until_complete(asyncio.wait(tasks))
        sys.stdout.write("\r\033[K有效ip:"+str(len(streamip))+" 总量:"+str(len(allips)))
        time.sleep(20)
async def test(sem,ip):
    proxy = 'http://' +ip
    url = 'http://api.live.bilibili.com/room/v1/Room/playUrl?cid=279430&otype=json&platform=web&qn=4'
    try:
        async with sem:
            async with aiohttp.ClientSession() as session:
                async with session.get(url,proxy = proxy,timeout = 5) as r:
                        nogood = 1
                        if r.status == 200:
                            rjson = await r.json()
                            if rjson['data']['accept_quality']:
                                nogood = 0
                                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36', 'Referer': 'https://live.bilibili.com/279430'}
                                durl = rjson['data']['durl']
                                for i in durl:
                                    uurl = i['url']
                                    if 'live-bvc' in uurl:
                                        aurl = uurl
                                    elif 'live-js' in uurl:
                                        burl = uurl
                                    elif 'live-txy' in uurl:
                                        curl = uurl 
                                if aurl:
                                    surl = aurl
                                    if r.status ==302:
                                        proxy = 0
                                    else:
                                        proxy = 'http://'+ ip
                                    aurl = 0
                                elif curl:
                                    surl = curl
                                    curl = 0
                                    proxy = 'http://' + ip
                                elif burl:
                                    surl = burl
                                    proxy = 0
                                else:
                                    return
                                nogood = 0
                                '''
                                try:
                                    async with session.get(surl,headers=headers,proxy=proxy,timeout = 5) as r:
                                        if r.status == 200 or r.status ==302:
                                            nogood = 0
                                        else:
                                            nogood = 1
                                except Exception as e:
                                    #print(e)
                                    nogood = 1
                                '''
                        if nogood:
                            if ip in streamip:
                                streamip.remove(ip)
                        else:
                            if not ip in streamip:
                                streamip.append(ip)
    except Exception as e:
        #print(e)
        if ip in streamip:
            streamip.remove(ip)
    finally:
        if 'r' in locals():
            r.close()

def run():
    global ROOMS
    global USERS
    sIds = ROOMS or '';
    aIds = sIds.split(',');
    sUsers = USERS or '';
    aUsers = sUsers.split(',');
    #synMonitor(aIds, aUsers);
    #gf = threading.Thread(target=getfollow,name = "getfollow",daemon=True)
    #gf.start()
    ch_us = threading.Thread(target=check_useful,name="checkip",daemon=True)
    ch_us.start()
    ch_us.join()
    ##newgetonline()

def parseArg():
    global ROOMS, USERS, FILEDIR, DEBUGLEVEL, SCRIPT, COMMAND, INTERVAL
    global log
    parser = argparse.ArgumentParser(description='simultaneously monitor status of plural rooms at live.bilibili.com, and download streaming ones');
    parser.add_argument('-r', '--room',
            help='IDs of rooms to listen, separated by comma'
    );
    parser.add_argument('-u', '--user',
            help='IDs of users who host the rooms to listen, separated by comma'
    );
    parser.add_argument('-d', '--dir',
            help='directory to be downloaded into'
    );
    parser.add_argument('-v', '--verbose',
            action='store_true',
            help='show verbose debug information'
    );
    parser.add_argument('-s', '--script',
            help='python scripts to be executed after a successful download; the downloaded file path will be passed as the first script argument ( sys.argv[1] )'
    );
    parser.add_argument('-c', '--command',
            help='the command to be executed after a successful download; the downloaded file path will replace "{0}" within the command, using format syntax ( COMMAND.format(FILEPATH) )'
    );
    parser.add_argument('-i', '--interval',
            type=int,
            help='the interval, in seconds, between each status poll round'
    );
    args = parser.parse_args();
    ROOMS = '{},{}'.format(ROOMS or '', args.room or '');
    USERS = '{},{}'.format(USERS or '', args.user or '');
    FILEDIR = args.dir or FILEDIR or '';
    #if (args.verbose):
    #    DEBUGLEVEL = logging.DEBUG;
    #else:
    #    DEBUGLEVEL = logging.INFO; 
    #log.setLevel(DEBUGLEVEL);
    SCRIPT = args.script or SCRIPT or '';
    COMMAND = args.command or COMMAND or '';
    INTERVAL = args.interval or INTERVAL or 20;
    print('passed command line arguments: {}'.format(
        {key: value for (key, value) in vars(args).items() if value is not None}
    ));
    return True;

def getcookies():
    global cookies
    global access_key
    while 1:
        try:
            os.system("python3 bilibili.py")
            try:
                config = toml.load('config.toml')
            except:
                print("无法加载config")
                return
            line = config['user']['account'].splitlines()[0]
            pairs={}
            for pair in line.strip(";").split(";"):
                if len(pair.split("=")) == 2:
                    key, value = pair.split("=")
                    pairs[key] = value
            cookie = all(key in pairs for key in ["bili_jct", "DedeUserID", "DedeUserID__ckMd5", "sid", "SESSDATA"])
            cookies={'cookie':";".join(f"{key}={value}" for key, value in pairs.items() if key in ["bili_jct", "DedeUserID", "DedeUserID__ckMd5", "sid", "SESSDATA"])}
            access_key = pairs['access_token']
            return cookies
        except:
            pass


def main():
    try:
        parseArg();
        getcookies()
        run();
    except KeyboardInterrupt as e:
        display('\nexiting...');

if __name__ == '__main__':
    main();
