# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 18:14:28 2020

@author: zhang
"""
import random
import requests
import json
import time
import re
import os
import traceback
from collections import OrderedDict
from requests.adapters import HTTPAdapter
from tqdm import tqdm
from threading import Thread,Semaphore
import sys
import gc

headers_raw="""Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,ja;q=0.8
Cache-Control: max-age=0
Connection: keep-alive
Cookie: _uuid=7C2EDDAA-B843-15E6-EFEE-DD0EA2F301B023443infoc; buvid3=E1815B06-1828-481F-BC84-498ABFD4F5EA155828infoc; LIVE_BUVID=AUTO4315670402248481; sid=lp8rpg6n; CURRENT_FNVAL=16; rpdid=|(J|)JkR|YR|0J'ulY~|R|k~u; UM_distinctid=16ce24c5cdd32-05def6882cc6ef-396a4605-1fa400-16ce24c5cde221; im_notify_type_1836737=0; stardustvideo=1; laboratory=1-1; INTVER=-1; pgv_pvi=9402613760; CURRENT_QUALITY=116; LIVE_PLAYER_TYPE=1; DedeUserID=1836737; DedeUserID__ckMd5=326caeb00bc9daa3; SESSDATA=68b4dc5a%2C1582691072%2C26581e11; bili_jct=c56310cc6de31f6e8728de07648983ec; flash_player_gray=false; html5_player_gray=false; bp_t_offset_1836737=359095747404222299; _dfcaptcha=d766283d73a7c658c29253faa4ab9077
Host: api.bilibili.com
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36"""

iplist = []
def getip():
    r = requests.get("http://127.0.0.1:5010/get_all/")
    data = r.json()
    for i in data:
        iplist.append(i.get("proxy"))
getip()
class Bili():
    def __init__(self,uid,since):
        self.name = ''
        self.uid = uid
        self.data = ''
        if since:
            self.since = since
        else:
            self.since = '1900-01-01 00:00:01'
        self.jpg=0
        self.png=0
        self.gif=0
        self.mp4=0
        self.bl_id_list = []
        self.dt=[]
        self.download_urls=[]
    def get_stream(self,i):
        url,file_path,name = i[0],i[1],i[2]
        proxies={}
        ip=''
        p=0
        downloaded = 0
        dheaders = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'}
        pro=0
        while 1:
            if pro:
                #proxies = {'http':'34.92.3.74:3654','https':'34.92.3.74:3654'}
                ip = iplist[random.randint(0,len(iplist) - 1)]
                proxies = {'http':ip,'https':ip}
            if not os.path.exists(file_path):
                try:
                    s = requests.Session()
                    s.mount(url, HTTPAdapter(max_retries=2))
                    downloaded = s.get(url,timeout=(5,8),proxies=proxies,headers=dheaders)
                    if downloaded.status_code ==404:
                        break
                    if downloaded.status_code ==200:
                        with open(file_path,'wb') as f:
                            f.write(downloaded.content)
                    else:
                        raise Exception('wrong_code')
                except Exception as e:
                    if 'wrong_code' in str(e):
                        print(e,url)
                        p = 1
                        pro = 1
                        del proxies,ip
                        time.sleep(1)
                    else:
                        pass#print(e)
                    continue
                    with open(f'{apath}/not_downloaded.txt','a') as f:
                        if name[0] == name[1]:
                            url = name[0]+':'+url+' '+file_path+'\n'
                        else:
                            url = name[0]+'_'+name[1]+':'+url+' '+file_path+'\n'
                        f.write(url)
                    traceback.print_exc()
            if p:
                print(file_path,'下载完成')
            if downloaded:
                downloaded.close()
            del proxies,ip,downloaded
            break
    def get_url(self,next_offset):
        params = {
                'host_uid':self.uid,
                'offset_dynamic_id':next_offset,
                'need_top':0
                }
        url= 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history'
        r = requests.get(url,params=params)
        result = r.json()
        r.close()
        return result
                
    def get_user_info(self,user_profile):
        user_info = {}
        try:
            try:
                user_info['uname'] = self.rename(user_profile['info']['uname'])
            except:
                user_info['uname'] = ''
            user_info['uid'] = str(user_profile['info']['uid'])
            try:
                user_info['face'] = user_profile['info']['face']
            except:
                user_info['face'] = ''
            user_info['sign'] = user_profile['sign']
            user_info['official'] = user_profile['card']['official_verify']['desc']
            #self.user = user_info
            return user_info
        except:
            traceback.print_exc()
            return 'error'
    def print_user_info(self):
        result_headers = ('用户昵称：'+self.user['uname']+
              '\n用户id：'+self.uid+
              '\n签名：'+self.user['sign']+
              '\n官方认证：'+self.user['official']
              )
        result= ''.join(result_headers)
        print(result+'\n\n'+'-'*30)
    def get_pic_urls(self,info):
        temp = []
        if isinstance(info,list):
            for i in info:
                temp.append(i['img_src'])
        else:
            temp.append(info)
        return temp
    def parse_daily(self,item,user=None):
        bl = OrderedDict()
        if user:
            bl['uid'] = user['uid']
            bl['uname'] = self.rename(user['uname'])
        else:
            bl['uid'] = self.uid
            bl['uname'] = self.name
        if 'rp_id' in item:
            print('纯动态')
            bl['description'] = item['content']
            bl['pictures']= []
            bl['video'] = ''
            bl['upload_time'] = self.str_to_time(item['timestamp'])
            return bl
        bl['id'] = item['id']
        bl['description'] = item['description']
        try:
            bl['category'] = item['category']
        except:
            pass
        if 'pictures' in item:
            bl['pictures'] = self.get_pic_urls(item['pictures'])
        else:
            bl['pictures']= []
        if 'video_playurl' in item:
            bl['video'] = item['video_playurl']
        else:
            bl['video'] = ''
        bl['upload_time'] = self.str_to_time(item['upload_time'])
        return bl
        '''
        except Exception as e:
            print('parse_daily Error:',e)
            traceback.print_exc()
            print(item)
            sys.exit()
        '''
    def parse_tg(self,card,user=None):
        bl = OrderedDict()
        if user:
            bl['uid'] = str(user['uid'])
            bl['uname'] = self.rename(user['uname'])
        else:
            bl['uid'] = self.uid
            bl['uname'] = self.name
        try:
            bl['aid'] = str(card['aid'])
        except:
            print(card)
            time.sleep(10)
        try:
            bl['cid'] = str(card['cid'])
        except:
            bl['cid'] ='0'
        bl['description'] = card['dynamic']
        bl['title'] = card['title']
        bl['desc'] = card['desc']
        bl['jump_url'] = card['jump_url']
        bl['pictures']=self.get_pic_urls(card['pic'])
        bl['video'] = ''
        bl['owner'] = card['owner']
        bl['video']=''
        bl['upload_time'] = self.str_to_time(card['pubdate'])
        return bl
    
    def str_to_time(self,text):
        if ':' in str(text):
            result = time.strptime(text,"%Y-%m-%d %H:%M:%S")
        else:
            result = time.localtime(text)
        return result
    
    def print_dt(self,bl):
        result = self.write_str(bl)
        print(result)
    def get_one_page(self,page):
        #global still_d
        try:
            cards = self.data['cards']
        except:
            print(self.name,'无更多动态')
            return
        has_more = self.data['has_more']
        for i in cards:
            card = json.loads(i['card'])
            if 'aid' in card:
                display = i['display']
                bl = self.parse_tg(card)
                bl['dynamic_id'] = i['desc']['dynamic_id']
                bl['usr_action'] = display['usr_action_txt']
            elif 'origin' in card:
                if 'episode_id' in card['origin']:
                    print('番剧')
                    continue
                user = self.get_user_info(card['origin_user'])
                if user == 'error':
                    if 'summary' in card or not card:
                        continue
                    else:
                        print(card)
                        sys.exit()
                if str(user['uid']) == self.uid:
                    continue
                bl = OrderedDict()
                item = card['item']
                bl['description']=item['content']
                origin=json.loads(card['origin'])
                if 'item' in origin:
                    oitem = origin['item']
                    oitem['user'] = user
                    bl['origin']=self.parse_daily(oitem,user)
                elif 'aid' in origin:
                    bl['origin'] = self.parse_tg(origin,user)
                else:
                    continue
                bl['origin']['dynamic_id'] = i['desc']['orig_dy_id']
                bl['dynamic_id'] = i['desc']['dynamic_id']
                bl['upload_time'] = self.str_to_time(card['item']['timestamp'])
                bl['pictures'] = ''
                bl['video'] = ''
            elif 'item' in card:
                item = card['item']
                try:
                    bl = self.parse_daily(item)
                except Exception as e:
                    print("item Error:",e)
                    traceback.print_exc()
                    print(card)
                    sys.exit()
                bl['dynamic_id'] = i['desc']['dynamic_id']
            elif 'sketch' in card:
                continue
            elif 'playCnt' in card:
                continue
            elif 'roomid' in card:
                continue
            elif not 'category' in card:
                print(card)
                exit(1)
            elif '小说' in card['category']['name'] or 'summary' in card:
                continue
            else:
                print(card)
                exit(1)
            if bl['dynamic_id'] in self.bl_id_list:
                continue
            try:
                publish_time = bl['upload_time']
            except:
                print(card)
                sys.exit()
            since_date = self.str_to_time(self.since)
            if publish_time < since_date:
                print(f"到达限制日期,已获取{self.name}的第{page}页动态")
                #if not write_it:
                return 0
                #else:
                #    self.write_data()
                #    self.dt=[]
                #    self.download_urls=[]
                #    still_d=0
            self.print_dt(bl)
            print('*'*20)
            self.dt.append(bl)
            self.bl_id_list.append(bl['dynamic_id'])
        print(f"已获取{self.name}的第{page}页动态")
        return has_more
                
    def rename(self,oname):
        rstr = r"[\/\\\:\*\?\"\<\>\|\- \n]"
        name = re.sub(rstr,"_",oname)
        return name
    def write_data(self):
        self.path = apath#f'{apath}/'+self.name
        if is_try:
            self.path = 'C:/Users/zhang/Desktop'
        self.filepath = self.path+f'/{self.name}.txt'
        if not os.path.exists(self.filepath):
            self.write_txt(0)
        else:
            self.write_txt(1)
        self.download_files()
    def get_download_urls(self,i,zf = 0):
        try:
            if i['pictures']:
                for pic in i['pictures']:
                    if not self.jpg and 'jpg' in pic:
                        self.jpg=1
                    if not self.png and 'png' in pic:
                        self.png=1
                    if not self.gif and 'gif' in pic:
                        self.gif=1
                    if zf:
                        filename = f"{self.name}-{time.strftime('%Y%m%d_%H%M%S',i['upload_time'])}-{i['uname']}-{pic.split('/')[-1]}"
                    else:
                        filename = f"{i['uname']}-{time.strftime('%Y%m%d_%H%M%S',i['upload_time'])}-{pic.split('/')[-1]}"
                    path = os.path.join(opath,self.name)
                    if not os.path.exists(path):
                        os.makedirs(path)
                    filepath = os.path.join(path,filename)
                    self.download_urls.append([pic,filepath,[self.name,i['uname']]])
            if i['video']:
                if not self.mp4 and 'mp4' in i['video']:
                    self.mp4=1
                if zf:
                    filename = f"{self.name}-{time.strftime('%Y%m%d_%H%M%S',i['upload_time'])}-{i['uname']}-{i['video'].split('/')[-1].split('?')[0]}"
                else:
                    filename = f"{i['uname']}-{time.strftime('%Y%m%d_%H%M%S',i['upload_time'])}-{i['video'].split('/')[-1].split('?')[0]}"
                path = os.path.join(opath,self.name)
                if not os.path.exists(path):
                    os.makedirs(path)
                filepath = os.path.join(path,filename)
                self.download_urls.append([i['video'],filepath,[self.name,i['uname']]])
            if 'origin' in i:
                self.get_download_urls(i['origin'],1)
        except Exception as e:
            print('get download url Error:',e)
            traceback.print_exc()
            print(i)
            sys.exit()
            
    def write_str(self,i):
        if 'origin' in i:
            first = '转发动态\n'
        else:
            first = ''
        temp_str=(first+i['description']+
            '\n发布时间：'+time.strftime("%Y-%m-%d %H:%M:%S",i['upload_time'])
            )
        result = ''.join(temp_str)
        if first:
            try:
                result+='\n原始用户：'+i['origin']['uname']+'\n'+'原始id:'+i['origin']['uid']+'\n'+self.write_str(i['origin'])
            except:
                print(i)
                sys.exit()
        else:
            if 'aid' in i:
                temp_str=('\n投稿了视频'+
                          '\naid:'+i['aid']+
                          '\ncid:'+i['cid']+
                          '\n标题：'+i['title']+
                          '\n描述：'+i['desc']
                          )
                result+=''.join(temp_str)         
        return result
    
    def write_txt(self,mode):
        temp_result= []
        if not mode:
            result_headers = ('用户昵称：'+self.user['uname']+
                              '\n用户id：'+self.uid+
                              '\n签名：'+self.user['sign']+
                              '\n官方认证：'+self.user['official']+
                              '\n动态内容：\n'+'-'*20+'\n'
                              )
            temp_result.append(result_headers)
        for i in self.dt:
            aresult=self.write_str(i)+'\n\n'
            temp_result.append(aresult)
            self.get_download_urls(i)
        result = ''.join(temp_result)
        with open(self.filepath,'a',encoding = 'utf-8') as f:
            f.write(result)
        print(f"{len(self.dt)}个动态已保存到{self.filepath}")
            
    def download_files(self):
        temp = []
        count = 0
        for i in tqdm(self.download_urls,desc="下载文件",ncols=50):
            self.get_stream(i)
            count+=1
            if count %15 ==0:
                time.sleep(random.randint(1,2))
        '''
        for i in self.download_urls:
            t = Down_thread(i)
            t.start()
            temp.append(t)
        for j in tqdm(temp,desc="下载文件",ncols=50):
            if j.is_alive():
                j.join()
            count+=1
            temp.remove(j)
            del j
            if count % 50 ==0:
                time.sleep(random.choice([1,2,3]))
        '''
    def get_pages(self):
        result = self.get_url(0)
        self.data= result['data']
        if not 'cards' in self.data:
            print(f'{self.uid}没有动态')
            return 'no'
        cardnum=0
        card = self.data['cards'][cardnum]
        while 1:
            try:
                user_profile = card['desc']['user_profile']
                self.user=self.get_user_info(user_profile)
                break
            except Exception as e:
                print(e)
                cardnum+=1
                card = self.data['cards'][cardnum]
                time.sleep(1)
        try:
            self.name = self.rename(self.user['uname'])
        except:
            print(self.user)
            exit(1)
        self.print_user_info()
        page_num=1
        while 1:
            hasmore = self.get_one_page(page_num)
            if hasmore:
                next_offset = self.data['next_offset']
                result = self.get_url(next_offset)
                self.data= result['data']
            else:
                break
            if page_num %10==0:
                self.write_data()
                self.dt= []
                self.download_urls = []
            page_num+=1
        self.write_data()
    
    def update_user(self,temp_time):
        with open('bilidt.txt') as f:
            lines = f.read().splitlines()
        has_uid=0
        for i, line in enumerate(lines):
            temp = line.split('  ')
            if self.uid == temp[0]:
                has_uid=1
                if len(temp) < 3:
                    temp.append(self.name)
                    temp.append(temp_time)
                else:
                    temp[1] = self.name
                    temp[2] = temp_time
                lines[i] = '  '.join(temp)
        if not has_uid:
            temp = f'{self.uid}  {self.name}  {temp_time}'
            lines.append(temp)
        with open('bilidt.txt','w') as f:
            f.write('\n'.join(lines))
    def start(self):
        temp_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        result = self.get_pages()
        if result == 'no':
            return
        self.update_user(temp_time)
        path = os.path.join(opath,self.name)
        '''if self.jpg:
            os.system(f"cd {path};mv *jpg ..")
        if self.png:
            os.system(f"cd {path};mv *png ..")
        if self.gif:
            os.system(f"cd {path};mv *gif ..")
        if self.mp4:
            os.system(f"cd {path};mv *mp4 ..")'''
class Down_thread(Thread):
    def __init__(self,i):
        Thread.__init__(self)
        self.i=i
    def run(self,pro=0):
        with thread_max_num:
            url,file_path,name = self.i[0],self.i[1],self.i[2]
            proxies={}
            ip=''
            p=0
            downloaded = 0
            dheaders = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'}
            while 1:
                if pro:
                    #proxies = {'http':'34.92.3.74:3654','https':'34.92.3.74:3654'}
                    ip = iplist[random.randint(0,len(iplist) - 1)]
                    proxies = {'http':ip,'https':ip}
                if not os.path.exists(file_path):
                    try:
                        s = requests.Session()
                        s.mount(url, HTTPAdapter(max_retries=2))
                        downloaded = s.get(url,timeout=(5,8),proxies=proxies,headers=dheaders)
                        if downloaded.status_code ==404:
                            break
                        if downloaded.status_code ==200:
                            with open(file_path,'wb') as f:
                                f.write(downloaded.content)
                        else:
                            raise Exception('wrong_code')
                    except Exception as e:
                        if 'wrong_code' in str(e):
                            print(e,url)
                            p = 1
                            pro = 1
                            del proxies,ip
                            time.sleep(1)
                        else:
                            pass#print(e)
                        continue
                        with open(f'{apath}/not_downloaded.txt','a') as f:
                            if name[0] == name[1]:
                                url = name[0]+':'+url+' '+file_path+'\n'
                            else:
                                url = name[0]+'_'+name[1]+':'+url+' '+file_path+'\n'
                            f.write(url)
                        traceback.print_exc()
                if p:
                    print(file_path,'下载完成')
                if downloaded:
                    downloaded.close()
                del proxies,ip,downloaded
                break 
def get_headers(header_raw):
    return dict(line.split(": ", 1) for line in header_raw.split("\n"))

      
def getuids():
    f = open('/root/u/checked_fmid.txt')
    uids = f.read().splitlines()
    f.close()
    return uids

def get_user_config(i):
    print(i)
    temp = i.split('  ')
    if len(temp) == 3:
        return temp[0],temp[2]
    else:
        return temp[0],0

headers = get_headers(headers_raw)
is_try = input('测试？')
opath = input("路径：")
thread_num = int(input("线程数："))
if not opath:
    apath = opath = 'C:/Users/zhang/Desktop'
else:
    apath = '/root/u/bilidt'
opath+='/bilidt'

thread_max_num = Semaphore(thread_num)

write_it=0
still_d=1
def main():
    global write_it
    if not os.path.exists(f'{apath}/bili404.txt'):
        f = open(f'{apath}/bili404.txt','w')
        f.close()
    if not os.path.exists('bilidt.txt'):
        f = open('bilidt.txt','w')
        f.close()
    while 1:
        with open('bilidt.txt') as f:
            odtlist = f.read().splitlines()
        dtlist = [i.split('  ')[0] for i in odtlist]
        if is_try:
            for i in odtlist:
                if '463999' in i:
                    tt = i
            uid,start_time = get_user_config(tt)
            B = Bili(uid,start_time)
            B.start()
            sys.exit(1)
        for i in odtlist:
            write_it=1
            still_d=1
            uid,start_time = get_user_config(i)
            B = Bili(uid,start_time)
            gc.disable()
            B.start()
            gc.enable()
            del B
            gc.collect()
        uids = getuids()
        for uid in uids:
            write_it=0
            if uid in dtlist:
                sys.stdout.write(f'\r\033[K{uid}跳过')
                continue
            uid,start_time = get_user_config(uid)
            B = Bili(uid,start_time)
            gc.disable()
            B.start()
            gc.enable()
            del B
            gc.collect()
            dtlist.append(uid)
        time.sleep(5)
if __name__ == '__main__':
    main()
