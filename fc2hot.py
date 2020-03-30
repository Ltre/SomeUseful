# -*- coding: utf-8 -*-
import traceback
import requests
import random
import time
import os
from email.header import Header
from email.mime.text import MIMEText
import smtplib
import http.cookiejar as cj
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import sys
sender = 'zhangzongqian32@outlook.com'
#sender = '1650658858@qq.com'
receiver = 'zhangzongqian32@icloud.com'
def send_mail(content,uid,image,subject=None):
    #主题
    """**主题如果是纯中文或纯英文则字符数必须大于等于5个，
    不然会报错554 SPM被认为是垃圾邮件或者病毒** """
    if not subject:
        subject = f"fc2热度更新{uid}{content.split(',')[0]}"
    #内容
    #contents=f'{content}\n{image}'
    contents = f"<html><body><h1>{content}</h1><p><img src='cid:0'></p></body></html>"
    #服务器地址
    smtpserver = 'smtp.office365.com'
    #smtpserver = 'smtp.qq.com'
    #用户名（不是邮箱）
    username = '提醒'
    #163授权码
    password='zongqian12345'
    #password='ihpdbjbsiszgdach'
    msg = MIMEMultipart()
    msg.attach(MIMEText(contents, 'html', 'utf-8'))  # 中文需参数‘utf-8'，单字节字符不需要
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = sender#username
    msg['To'] = receiver
    
    while 1:
        try:
            r = requests.get(image,timeout=8)
            break
        except Exception as e:
            if not 'time' in str(e):
                print("下载img失败",e)
                r=''
                break
    # 设置附件的MIME和文件名，这里是png类型:
    mime = MIMEBase('image', 'jpg', filename=f'{uid}.jpg')
    # 加上必要的头信息:
    mime.add_header('Content-Disposition', 'attachment', filename=f'{uid}.jpg')
    mime.add_header('Content-ID', '<0>')
    mime.add_header('X-Attachment-Id', '0')
    # 把附件的内容读进来:
    if r:
        mime.set_payload(r.content)
    else:
        mime.set_payload(b'1')
    # 用Base64编码:
    encoders.encode_base64(mime)
    # 添加到MIMEMultipart:
    msg.attach(mime)
    
    #服务器地址和端口25
    smtp = smtplib.SMTP(smtpserver,587)
    #smtp = smtplib.SMTP_SSL(smtpserver, 465)
    smtp.starttls()
    try:
        smtp.login(sender, password)
        smtp.sendmail(sender, receiver, msg.as_string())
        smtp.quit()
        print('发送邮件成功')
    except Exception as e:
        print("发送邮件失败",e)

def get_favorite():
    favorite_url = 'https://live.fc2.com/adult/contents/favorite.php'
    r = s.post(favorite_url,timeout=10)
    status = r.json()['status']
    if not status:
        if login():
            print('重登录成功')
            return get_favorite()
    data = r.json()['data']
    r.close()
    return data

def login():
    #if os.path.exists('cookies.txt'):
    #    s.cookies = cj.LWPCookieJar(filename='cookies.txt')
    #    s.cookies.load(filename='cookies.txt', ignore_discard=True)
    #else:
    #    s.cookies = cj.LWPCookieJar()
    login_url = 'https://secure.id.fc2.com/index.php?mode=login&switch_language=en'
    data = {
                'email':'48161925@qq.com',
                'pass':'aa678678',
                'done':'livechat',
                'keep_login': 1
            }
    
    r = s.post(login_url,data=data)
    if 'Set-Cookie' in r.headers:
        return 1
    else:
        return 0
    

def add_id(uid):
    add_url = 'https://live.fc2.com/api/favoriteManager.php'
    d = {
            "id":uid,
            "mode":"add",
         }
    d2 = {
            "id":uid,
            "mode":"switch",
            }
    r = s.post(add_url,data=d)
    if r.json()['status']:
        r.close()
        r = s.post(add_url,data=d2)
        return r.json()['status']
def delete_id(uid):
    delete_url = 'https://live.fc2.com/api/favoriteManager.php'
    d = {
            "id":uid,
            "mode":"remove",
            "page":""
        }
    r = s.post(delete_url,data=d)
    return r.json()['status']
def hot_record(uid,start,new):
    finduid = 0
    recorded = 0
    data=''
    rf = open(path,encoding='utf-8-sig',errors='ignore')
    hotlist = rf.readlines()
    rf.close()
    if new == '低热':
        for i in hotlist:
            if new in i:
                print('删除',i)
                continue
            data+=i
    else:
        for i in hotlist:
            if not recorded:
                if not '--' in i and i == str(uid)+'\n' and not finduid:
                    finduid = 1
                elif finduid and '--' in i:
                    check_start = i.split('--')[1].split(',')[0]
                    if check_start == start:
                        old = i.split(',')[1]
                        i = i.replace(old,new)
                        recorded = 1
                elif finduid and not '--' in i:
                    i = f'--{start},{new},{name},{title}\n'+i
                    recorded = 1
            data+=i
        if not finduid:
            write_str = f'{uid}\n--{start},{new},{name},{title}\n'
            data+=write_str
    with open(path,'w',encoding='utf-8-sig') as f:
        f.writelines(data)

login_cookies = {
    "_ga":"GA1.2.1206995401.1580623938",
    "__utma":"168497334.1206995401.1580623938.1580624041.1580624041.1",
    "__utmz":"168497334.1580624041.1.1.utmcsr=id.fc2.com|utmccn=(referral)|utmcmd=referral|utmcct=/",
    "FC2_GDPR":"true",
    "fgcv":"1%3BjzlTKJX7D%2FSEjmFFR4jTc9pfuiSSElq%2FdTBm2%2FuDXpX8Y82G",
    "_gid":"GA1.2.187524437.1581153901",
    "fclo":"1581337162943%2Czh-CN%2C8",
    "login_status":"1%7C35940324%7CezJd5eRwIoiWBXIT3Lkp%7C1581515479%7C1%7C723a76888c2ed92eda6504bf98fbe9db",
    "PHPSESSID":"khahe737cqd9mvki2kva33ei21",
    "_gat":"1"
}
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36",
"Referer": "https://live.fc2.com/adult/"}
url = 'https://live.fc2.com/adult/contents/allchannellist.php'

s = requests.session()
s.headers.update(headers)
#s.cookies.update(login_cookies)

opath = input('路径:')
if not opath:
    opath = 'C:/Users/zhang/Desktop'
path = os.path.join(opath,'hotlist.txt')
if not os.path.exists(path):
    with open(path,'w') as f:
        pass
hot_spot = {}
nofollow = open('/root/u/nofollow.txt').read().splitlines()
while 1:
    try:
        favoritelist = get_favorite()
        break
    except Exception as e:
        print(e)
        time.sleep(2)
'''
hot_find = {
        '中热':1,
        '热':2,
        '大热':3,
        '超热':4,
        }
'''
runtime = 0
while 1:
    try:
        r = s.post(url,timeout=(5,10))
        data = r.json()
        r.close()
        is_adult = data['is_adult']
        if is_adult:
            channel = data['channel']
            for i in channel:
                uid = category = count = image = 0
                uid = i['id']
                category = i['category']
                count = i['count']
                image = i['image']
                if str(uid) in nofollow and uid in favoritelist:
                    if delete_id(uid):
                        print(f'\r\033[K{uid}解除关注成功')
                    else:
                        print(f'\r\033[K{uid}解除关注失败')
                if count >=100 and str(uid) not in nofollow:
                    name = i['name']
                    title = i['title']
                    start = i['start']
                    if not uid in favoritelist and category !=4:
                        if add_id(uid):
                            print(f'{uid}添加成功')
                            favoritelist.append(uid)
                            content=f'已关注{name},{title}'
                            subject=f'fc2新关注{uid}'
                            send_mail(content,uid,image,subject)
                        else:
                            print(r"{uid}添加失败")
                    if uid in favoritelist:
                        if count >=250 and count < 500:
                            do=0
                            if not uid in hot_spot or not hot_spot[uid]:
                                do=1
                            if do:
                                new='低热'
                                print(f'\r\033[K{uid}{new},{start},{name},{title}')
                                content = f'{new},{start},{name},{title}'
                                send_mail(content,uid,image)
                                hot_spot[uid] = -1
                                hot_record(uid,start,new)
                        elif count >=500 and count < 1000:
                            do = 0
                            if not uid in hot_spot or hot_spot[uid] <=0:
                                do = 1
                            if do:
                                new = '中热'
                                print(f'\r\033[K{uid}中热,{start},{name},{title}')
                                content = f'中热,{start},{name},{title}'
                                hot_spot[uid] = 1
                                hot_record(uid,start,new)
                                send_mail(content,uid,image)
                        elif count >=1000 and count < 2000:
                            do = 0
                            if not uid in hot_spot or hot_spot[uid] <=1:
                                do = 1
                            if do:
                                new = '热'
                                print(f'\r\033[K{uid}热,{start},{name},{title}')
                                content = f'热,{start},{name},{title}'
                                hot_spot[uid] = 2
                                hot_record(uid,start,new)
                                send_mail(content,uid,image)
                        elif count >=2000 and count < 3000:
                            do = 0
                            if not uid in hot_spot or hot_spot[uid] <=2:
                                do = 1
                            if do:
                                new = '大热'
                                print(f'\r\033[K{uid}大热,{start},{name},{title}')
                                content = f'大热,{start},{name},{title}'
                                hot_spot[uid] = 3
                                hot_record(uid,start,new)
                                send_mail(content,uid,image)
                        elif count >=3000:
                            do = 0
                            if not uid in hot_spot or hot_spot[uid] <=3:
                                do = 1
                            if do:
                                new = '超热'
                                print(f'\r\033[K{uid}超热,{start},{name},{title}')
                                content = f'超热,{start},{name},{title}'
                                hot_spot[uid] = 4
                                hot_record(uid,start,new)
                                send_mail(content,uid,image)
        runtime += 1
        if runtime % 3 == 0:
            favoritelist = get_favorite()
        if runtime >= 10:
            runtime = 0
            for i in hot_spot:
                if i not in favoritelist:
                    print(f'\r\033[K{uid} 已停止,删除热度')
                    hot_spot[i] = 0
        
        nofollow = open('/root/u/nofollow.txt').read().splitlines()
        time.sleep(random.randint(8,12))
    except Exception as e:
        print("Error",e)
        traceback.print_exc()

