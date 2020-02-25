import requests,re,subprocess,os,time,random,shutil,traceback,sys
from threading import Thread,Timer
from websocket import create_connection
import json
from datetime import datetime
from requests.utils import dict_from_cookiejar
import http.cookiejar as cj
from streamlink import Streamlink
from livestreamer import Livestreamer
if not os.path.exists('/root/b/d/fc2'):
    os.makedirs('/root/b/d/fc2')
os.system('cd /root/u;bash fct.sh')
trytimes = input('重试次数')
threads = input('线程数')
users = []
recording = []
class FC2():
    url_login = 'https://secure.id.fc2.com/index.php?mode=login&switch_language=en'
    url_member_api = 'https://live.fc2.com/api/memberApi.php'
    url_server = 'https://live.fc2.com/api/getControlServer.php'
    
    count = 0
    count_ping = 0
    host_data = ''
    channel_data=''
    profile_data=''
    host_found = False
    def __init__(self,userid,session):
        self.user_id = userid
        self.thread=None
        self.session=session
        self.url = 'https://live.fc2.com/'+str(userid)+'/'
        self.sameid = 1
        self.ex = 1
        self.end = False

    def login(self,relogin = 0):
        if os.path.exists('cookies.txt') and not relogin:
            self.session.cookies = cj.LWPCookieJar(filename='cookies.txt')
            self.session.cookies.load(filename='cookies.txt', ignore_discard=True)
        else:
            self.session.cookies = cj.LWPCookieJar()
            self.session.get(self.url)
            data = {
                'email':'48161925@qq.com',
                'pass':'aa678678',
                'done':'livechat',
                'keep_login': 1
            }
            self.session.post(self.url_login,data=data)
            self.session.cookies.save(filename='cookies.txt', ignore_discard=True, ignore_expires=True)
            #cookies_list = self.save_cookies()
        return 1#self.cmp_cookies_list(cookies_list)
    
    def cmp_cookies_list(self,cookies_list):
        required_cookies = [
            'FCSID', 'fcu', 'fgcv', 'glgd_val',
            'login_status', 'PHPSESSID', 'secure_check_fc2',
        ]
        c_count = 0
        for c in required_cookies:
            if c in cookies_list:
                c_count += 1
        return (c_count == len(required_cookies))
    
    def get_version(self, user_id):
        data = {
            'user': 1,
            'channel': 1,
            'profile': 1,
            'streamid': int(user_id)
        }
        sys.stdout.write('\r\033[K'+str(user_id)+' get version')
        res = self.session.post(self.url_member_api, data=data,timeout=10)
        #print('\r\033[K',res.text)
        #time.sleep(100)
        try:
            res_data = res.json()
        except Exception as e:
            print (e)
            return False
        self.profile_data = res_data['data']['profile_data']
        channel_data = self.channel_data = res_data['data']['channel_data']
        user_data = res_data['data']['user_data']

        if (channel_data['login_only'] != 0 and user_data['is_login'] != 1):
            sys.stdout.write(f'\r\033[K{self.user_id}A login is required for this stream.')
            return 'login'

        if channel_data['fee'] != 0:
            sys.stdout.write('\rOnly streams without a fee are supported.'+str(self.user_id))
            return False

        version = channel_data['version']
        if (version):
            if user_data['is_login']:
                sys.stdout.write('\rLogged in as {0}'.format(user_data['name']))
            #print(channel_data['channelid'],' Found version: {0}'.format(version))
        return version
    
    def get_ws_url(self, user_id, version):
        sys.stdout.write('\r_get_ws_url ...')
        #orz = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJvcnoiOiJkYjQzNzVmYTM4NmY1NDdiOTI5OGMxNTE0NjJkNmFjMDZjZGIyMDQ2In0.ofWxZb9_CNUbpOsi3OCfj_0cMEaUO7S7VLWIIL0vO4s'
        data = {
            'channel_id': user_id,
            'channel_version': version,
            'client_type': 'pc',
            'client_app': 'browser_hls',
            'client_version':'1.6.3%0A+%5B1%5D',
            'orz':'',
            'mode':'play'
        }

        res = self.session.post(self.url_server, data=data)
        w_data = res.json()
        if w_data['status'] == 11:
            sys.stdout.write('\rThe broadcaster is currently not available')
            return None

        ws_url = '{0}?control_token={1}'.format(
            w_data['url'], w_data['control_token'])
        #print('WS URL: {0}'.format(ws_url))
        return ws_url
    
    def payload_msg(self, name):
        ''' Format the WebSocket message '''
        self.count_ping += 1
        payload = json.dumps(
            {
                'name': str(name),
                'arguments': {},
                'id': int(self.count_ping)
            }
        )
        return payload
    
    def get_ws_data(self, ws_url):
        ws = create_connection(ws_url)
        ws.send(self.payload_msg('get_hls_information'))
        #ws.send(self.payload_msg('get_media_server_information'))

        def ws_ping():
            ''' ping the WebSocket '''
            if ws.connected is True:
                try:
                    t1 = Timer(30.0, ws_ping)
                    t1.daemon = True
                    t1.start()
                    ws.send(self.payload_msg('heartbeat'))
                except:
                    pass

        def ws_recv():
            ''' print WebSocket messages '''
            while True:
                self.count += 1
                try:
                    rdata = ws.recv()
                    data = json.loads(rdata)
                except:
                    print('\r\033[K',rdata)
                    break
                #time_utc = datetime.utcnow().strftime('%H:%M:%S UTC')
                #if data['name'] not in ['comment', 'ng_commentq',
                #                        'user_count', 'ng_comment']:
                #    print('{0} - {1} - {2}'.format(
                #        time_utc, self.count, data['name']))
                if self.end:
                    break
                if (data['name'] == '_response_'
                        and data['arguments'].get('playlists')):
                    sys.stdout.write('\rFound host data')
                    self.host_data = data
                    self.host_found = True
                elif data['name'] == 'media_connection':
                    sys.stdout.write('\rsuccessfully opened stream')
                elif data['name'] == 'control_disconnection':
                    if self.count <= 30:
                        # User with points restricted program being broadcasted
                        self.count = 30
                        break
                    if data.get('arguments').get('code') == 4512:
                        sys.stdout.write('\rDisconnected from Server')
                        break
                elif data['name'] == 'publish_stop':
                    print('\r\033[K',f'{self.user_id}Stream ended')
                    break
                elif data['name'] == 'channel_information':
                    if data['arguments'].get('fee') != 0:
                        print(f'\r\033[K{self.user_id}Stream requires a fee now.')
                        time.sleep(5)
                        break
                elif data['name'] == 'media_disconnection':
                    if data.get('arguments').get('code') == 104:
                        print('\r\033[K','Disconnected. '
                                    'Multiple connections has been detected.')
                        break
                    elif data.get('arguments').get('code'):
                        print('\r\033[K','error code {0}'.format(
                            data['arguments']['code']))
                        break

            ws.close()

        # WebSocket background process
        try:
            ws_ping()
        except:
            print('\r\033[K',f'{self.user_id}ws_ping 出错')
        t2 = Thread(target=ws_recv,daemon=True)
        t2.daemon = True
        t2.start()

        # wait for the WebSocket
        host_timeout = False
        while self.host_found is False:
            if self.host_found is True:
                break
            if self.count >= 30:
                host_timeout = True
                break
            time.sleep(3)

        sys.stdout.write('\rhost_timeout is {0}'.format(host_timeout))
        if host_timeout:
            return False
        return True
    
    def get_rtmp(self, data):

        app = '{0}?media_token={1}'.format(
            data['application'], data['media_token'])
        host = data['host']

        params = {
            'app': app,
            'flashVer': 'WIN 29,0,0,140',
            'swfUrl': 'https://live.fc2.com/swf/liveVideo.swf',
            'tcUrl': 'rtmp://{0}/{1}'.format(host, app),
            'live': 'yes',
            'pageUrl': self.url,
            'playpath': data['play_rtmp_stream'],
            'host': host,
        }
        yield 'live', RTMPStream(self.session, params)
    
    def get_streams(self):
        
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
            'Referer': self.url
        })

        cookies_list = []
        for k in dict_from_cookiejar(self.session.cookies):
            cookies_list.append(k)
        _authed = self.cmp_cookies_list(cookies_list)
        '''
        if _authed:
            print('Attempting to authenticate using cached cookies')
        elif (not _authed):
            if not self.login():
                print('Failed to login, check your username/password')
        '''
        user_id =self.user_id
        version = self.get_version(user_id)
        logintime=0
        runtime=0
        while(version == 'login'):
            if runtime:
                break
            if logintime :
                runtime+=1
                os.system('cd /root/u;rm cookies.txt')
            self.login()
            version = self.get_version(user_id)
            logintime+=1
        if(version and version !='login'):
            ws_url = self.get_ws_url(user_id, version)
            if self.get_ws_data(ws_url):
                sys.stdout.write('\r \033[K ok')
                return True
        return False
            #return self.get_rtmp(self.host_data['arguments'])
            
            
def main(test=None):
    global users
    if not os.path.exists('cookies.txt'):
        aa = requests.session()
        aa.keep_alive = False
        aa.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
            })
        x=FC2(983226,aa)
        x.login()
    
                
    if test:
        r = requests.session()
        r.keep_alive=False
        a = FC2(int(test),r)
        dodownload(a)
    else:
        while 1:
            users=[]
            fav = requests.session()
            fav.keep_alive = False
            fav.cookies = cj.LWPCookieJar(filename='cookies.txt')
            fav.cookies.load(filename='cookies.txt',ignore_discard=True)
            allres = fav.post('https://live.fc2.com/adult/contents/allchannellist.php').json()
            channel = allres['channel']
            try:
                res = fav.post('https://live.fc2.com/adult/contents/favorite.php').json()
            except:
                traceback.print_exc()
                time.sleep(10)
                continue
            if res['status'] == 0:
                aa = requests.session()
                aa.keep_alive = False
                aa.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
                })
                x=FC2(983226,aa)
                x.login(1)
            else:
                data = res['data']
                for i in data:
                    if(i):
                        for ii in channel:
                            if ii['id'] == str(i):
                                if not ii['pay']:
                                    r =requests.session()
                                    r.keep_alive = False
                                    a=FC2(int(i),r)
                                    users.append(a)
                                break
                '''if os.path.exists('fuser.txt'):
                    rr=open('fuser.txt','r')
                    for i in rr.readlines():
                        i=i.strip()
                        if i:
                            r =requests.session()
                            r.keep_alive = False
                            a=FC2(int(i),r)
                            users.append(a)
                    rr.close()'''
                for a in users:
                    if not a.user_id in recording:
                        a.thread=t=Thread(target=dodownload,args=(a,),name=a.user_id,daemon=True)
                        t.start()
            sys.stdout.write(f'\r\033[K正在录制{len(recording)}')
            time.sleep(random.randint(5,10))

def dodownload(a):
    if a.user_id in recording:
        return
    recording.append(a.user_id)
    print(f'\r\033[K{a.user_id}start')
    live=a.get_streams()
    if live:
        playlists=a.host_data['arguments']['playlists']
        for i in playlists:
            if i['mode'] == 0 or i['mode']== '0':
                print(f'\r\033[K{a.user_id}获取主列表{i["url"]}')
                master = i['url']
        #session = Streamlink()
        session = Livestreamer()
        if threads:
            session.set_option('hls-segment-threads',int(threads))
        if trytimes:
            session.set_option('hls-segment-attempts',int(trytimes))
        session.set_option('hls-live-edge',9999)
        session.set_option('hls-segment-timeout',6.0)
        session.set_option('hls-timeout',10.0)
        session.set_loglevel("none")
        #cmd = ['streamlink','hls://{}'.format(master),'best','-o','/root/te/t.ts']
        #subprocess.call(cmd)
        streams = session.streams('hlsvariant://'+master)
        stream = streams["best"]
        #print(stream.url)
        error = 0
        rstr = r"[\/\\\:\*\?\"\<\>\|\- \n]"
        oname = a.profile_data['name']
        otitle = a.channel_data['title']
        name = re.sub(rstr,"_",oname)
        title = re.sub(rstr,"_",otitle)
        path = '/root/b/d/fc2/'+str(a.user_id)
        if not os.path.exists(path):
            os.makedirs(path)
        userid = str(a.user_id)
        while(not error):
            if a.sameid == 0:
                break
            filename = path+'/'+userid+'-'+time.strftime('%y%m%d_%H%M%S')+'-'+name+'-'+title+'.ts'
            if len(filename) >=130:
                title = '_'
                filename = path+'/'+userid+'-'+time.strftime('%y%m%d_%H%M%S')+'-'+name+'-'+title+'.ts'
            fs = 0
            try:
                '''
                cmd = ['ffmpeg','-loglevel','quiet','-y','-i',master,'-c','copy','-fs','1073741824',filename]
                #cmd = ['ffmpeg','-y','-i',master,'-c','copy','-fs','1073741824',filename,'-loglevel','debug']
                error=subprocess.call(cmd)
                '''
                fd = stream.open()
                f = open(filename,'wb')
                desize = 1024*1024*1024
                while 1:
                    ddata = fd.read(8192)
                    if ddata:
                        fs+=f.write(ddata)
                        #if fs % 64 == 0:
                        #    sys.stdout.write(f'\r\033[K正在录制{len(recording)}{name}{userid}---{round(fs/1024/1024,2)}m')
                        if fs>=desize:
                            fs=0
                            f.close()
                            print(f'\r\033[K{filename}文件大小达到限制，切割')
                            shutil.move(filename,'/root/b/d/fc2')
                            filename = path+'/'+userid+'-'+time.strftime('%y%m%d_%H%M%S')+'-'+name+'-'+title+'.ts'
                            f = open(filename,'wb')
                    else:
                        print(f'{userid}停止录制')
                        break
                
            except Exception as e:
                print(f'\r\033[K{a.user_id}',e)
                #traceback.print_exc()
            finally:
                if 'fd' in locals():
                    fd.close()
                if 'f' in locals():
                    f.close()
                    ff = os.path.getsize(filename)
                    if ff<=1024*100:
                        print(f'\r\033[K{userid}文件下载失败')
                        #cmd = ['ffmpeg','-y','-i',master,'-c','copy','-fs','1073741824',filename,'-loglevel','debug']
                        #error=subprocess.call(cmd)

                    shutil.move(filename,'/root/b/d/fc2')
                os.rmdir(path)
                break
            #'''
            print(error)
            break
    a.end = True
    if a.user_id in recording:
        print(f'\r\033[K{a.user_id}从列表删除')
        recording.remove(a.user_id)
    else:
        print(f'\r\033[K{a.user_id}在列表中找不到{recording}')
    time.sleep(5)
    del a
    
if __name__ =='__main__':
    test=input('testid:')
    if test:
        main(test)
    else:
        main()
