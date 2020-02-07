import requests,os,time
hcookies = {"Cookie":
        'SoundValue=0.50; alphaValue=0.80; __yamid_tt1=0.5630173980060627; __yamid_new=C8736F6698800001A3314BF01CD08350; udb_guiddata=4d0af64ce63b43f29a7a5975d914b205; first_username_flag=35184377273454hy_first_1; udb_accdata=undefined; Hm_lvt_51700b6c722f5bb4cf39906a596ea41f=1576679026,1576732023,1577338814,1577958774; guid=0ad6867c39df195e6201245925596308; isInLiveRoom=true; udb_passdata=3; __yasmid=0.5630173980060627; udb_other=%7B%22lt%22%3A%221580637380270%22%2C%22isRem%22%3A%221%22%7D; web_qrlogin_confirm_id=9bb7cb17-6c43-4d23-a5dc-86b6516fe14e; udb_uid=1199513272235; yyuid=1199513272235; udb_passport=35184377273454hy; username=35184377273454hy; udb_version=1.0; udb_origin=0; udb_status=1; h_unt=1580637410; __yaoldyyuid=1199513272235; _yasids=__rootsid%3DC8C6E07BFAE00001A6887F2085D01896; udb_biztoken=AQB_yEbIQD4qLnPRik1zepaQSUwq0vFnHZGbJp5AYvTUED5xBGKlrsGJnjfDt8rknqYzlo6vRTHzkHh-seGkx_4psi9eWcq9fM8X-HlbAxd63jzN2vAErbAeAkkIxiDo-ngq_-SyiWLSkF2iwF4wyS2mBNRbCReVsL4i1xBKplYysxKoIinhePIeTOeuTE2Zpy7tI2MtpeF9jG-hVFR1oCzptIQqK8PHzwxHyh92tWzuSkotRFG9y6MFi9t22Ke681iavpODtcVL_pgr0i1HrHlV4_G0aWN4yDcNj-VmrnhLU2wt_zhCHuDp6uAd-FLwgAl8xy1eeqsDLGEo7KYsth-G; rep_cnt=77; PHPSESSID=i8r1l87pvcodh89o9r8uof29h2'
        }

headers={"Accept":"application/json, text/javascript, */*; q=0.01","User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.0 Safari/534.20 QBWebViewUA/2 QBWebViewType/1 WKType/1","Referer":"http//i.huya.com/","Accept-Language":"zh-cn"}
url = 'https://fw.huya.com/dispatch?do=subscribeList&uid=1199513272235&page=1&pageSize=1000'
if not os.path.exists('huser.txt'):
    os.makedirs('huser.txt')
namelist = open('huser.txt').read().splitlines()
if namelist:
    print(len(namelist))
loginurl = 'https://udblgn.huya.com/login/ticket?uid=1199513272235&appid=5010&ticket=0QDPAAEDAAAAq%2F%2BPSBcBAAAAAAAAAAAAAAQANTAxMCQAOUFDQTdGQjYtNDFBNC00RUZCLUEwOEUtNTM2MTQwMEEzMzFCBAA1MDEwggACElNWHv3EkCdBlk4zpBXj6HaMCMCehMPpzA2ULeluk38zGRAKyt2Belo84jh17D5TqPKGQA4GuaNk4gTU09wyqKi9ChoK6Zad4jUWCEy%2BS4ZXf93KivebHEJ7mL0VD%2FGCrc6NVoDwXs%2BApFVh3hZ8e%2FlDK%2Bn46EMUUFABoQd5XMzDAAAAAA%3D%3D&ticketType=2&busiId=&cks=true&busiUrl=https%3A%2F%2Fhd.huya.com%2FappTestPage%2FwriteCookieLgnPreview.html&reqDomainList=huya.com&passport=35184377273454hy&bypass=3'
s=requests.session()
s.cookies.update(hcookies)
while 1:
    try:
        r = s.get(url,timeout=10)
        data = r.json()['result']
        dlist = data['list']
        liveCount = data['liveCount']
        with open('huser.txt','a') as f:
            for i in dlist:
                name = str(i['profileRoom'])
                if name not in namelist:
                    print(time.strftime('%Y_%m_%d-%H:%M:%S'),name)
                    f.write(name)
                    f.write('\n')
                    if not name in namelist:
                        namelist.append(name)
    except Exception as e:
        print(e)
        if not 'time' in str(e):
            r = s.get(loginurl,allow_redirects=False)
    finally:
        r.close()
        time.sleep(5)
    
