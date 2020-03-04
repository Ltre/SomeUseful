import requests,os,time
hcookies = {"Cookie":
        "SoundValue=0.50; alphaValue=0.80; __yamid_tt1=0.5630173980060627; __yamid_new=C8736F6698800001A3314BF01CD08350; udb_guiddata=4d0af64ce63b43f29a7a5975d914b205; first_username_flag=35184377273454hy_first_1; udb_accdata=undefined; Hm_lvt_51700b6c722f5bb4cf39906a596ea41f=1576679026,1576732023,1577338814,1577958774; guid=0ad6867c39df195e6201245925596308; udb_passdata=3; __yasmid=0.5630173980060627; isInLiveRoom=true; web_qrlogin_confirm_id=7c2b76b3-3478-4027-8623-8a781b8bdb42; udb_other=%7B%22lt%22%3A%221583155678597%22%2C%22isRem%22%3A%221%22%7D; udb_uid=1199513272235; yyuid=1199513272235; udb_passport=35184377273454hy; username=35184377273454hy; udb_version=1.0; udb_origin=0; udb_status=1; rep_cnt=17; h_unt=1583155740; __yaoldyyuid=1199513272235; _yasids=__rootsid%3DC8D04226B2600001E867E8201711C0A0; huya_flash_rep_cnt=16; udb_biztoken=AQCPgSb_RAp2Lkq_LRPzj-_3SooD7ucFltQSNoc09Z6JU3sujkVXK9djBMBhMuMScB6e27Y9xm4GX-U-j5aUATaeg26L4-ghXpi0qjWVMLkx0oC7WNpy2LIrs6RC9e6Z4UM3b0EkQEooqZDHMPRs6eiVfRvCtOuYqQjLoCUCxLtrSKPwC2Fsso4qAZFonDKQijGLUuD8WsAmj8kYe4T3XQ77DF15J0UEJPTi8iLWHmqCjLq3Sn4ewLBV8rInE6gyW7KVR398oLwQHTJJIqaPNQnG3eBTdFxqe3Pk2hcWfrjeBtlek34BpsyOap59iH6fn6rFgQTTW0ZnTt4-_FohOZAb; PHPSESSID=8q4kdj213rm41gjatak7lhg383; undefined=undefined; huya_web_rep_cnt=16"
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
        print(e,r.json())
        if not 'time' in str(e):
            while 1:
                try:
                    r = s.get(loginurl,allow_redirects=False,timeout=10)
                    print(r.status_code,r.headers)
                    break
                except:
                    print('登录失败')
    finally:
        r.close()
        time.sleep(5)
    
