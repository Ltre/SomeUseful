import requests,os
hcookies = {"Cookie":
        "SoundValue=0.50; alphaValue=0.80; __yamid_tt1=0.5630173980060627; __yamid_new=C8736F6698800001A3314BF01CD08350; udb_guiddata=4d0af64ce63b43f29a7a5975d914b205; first_username_flag=35184377273454hy_first_1; isInLiveRoom=; udb_accdata=undefined; Hm_lvt_51700b6c722f5bb4cf39906a596ea41f=1576679026,1576732023,1577338814,1577958774; PHPSESSID=d2k1ovl0fauakmlbl44fg2g2t3; __yasmid=0.5630173980060627; udb_passdata=3; web_qrlogin_confirm_id=52c78657-d4d0-4b1e-9306-6d13f312ebb3; sdid=; udb_uid=1199513272235; yyuid=1199513272235; udb_passport=35184377273454hy; username=35184377273454hy; udb_version=1.0; udb_biztoken=AQBZ7vrqUpXWos8q2M0OU89zsElWoiKbHYJBNByB5SKLKpII2Yjl_FVHiIb5UjU155-ib8DuS17qiQ07PDq6kP3ngrW09uO0RZLxhd-MOO0poNLYKSsaFll9moVtWJBz8IUGJICkEHaoDdksxnU-HpheU595n4JrP9lccGwHYC14sX3UMbTqcueYeRDriHXzqddTSUsHLk6cKFrG_8E7cdZkGZ_yf-A65QDhKPxnzWZTv-mcyNWyb4fx5rsFufCgvH6U1kzuomneAaulRRVQyzlsAanVrWcO2bCJdAHh7lv5f2-sSVss-O-Lg1EtCrVEPu_MJ7XFdG0cHb-hHOrCA6Y0; udb_origin=0; udb_status=1; __yaoldyyuid=1199513272235; _yasids=__rootsid%3DC8BFDC03906000011AE01CFAB4004CC0; undefined=undefined; h_unt=1578753678; rep_cnt=5"
        }
headers={"Accept":"application/json, text/javascript, */*; q=0.01","User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.0 Safari/534.20 QBWebViewUA/2 QBWebViewType/1 WKType/1","Referer":"http//i.huya.com/","Accept-Language":"zh-cn"}
url = 'https://fw.huya.com/dispatch?do=subscribeList&uid=1199513272235&page=1&pageSize=1000'
if not os.path.exists('huser.txt'):
    os.makedirs('huser.txt')
namelist = open('huser.txt').read().splitlines()
if namelist:
    print(namelist)
r = requests.get(url,headers=headers,cookies=hcookies,timeout=5)
data = r.json()['result']
dlist = data['list']
liveCount = data['liveCount']
with open('huser.txt','a') as f:
    for i in dlist:
        name = str(i['profileRoom'])
        if name not in namelist:
            print(name)
            f.write(name)
            f.write('\n')
