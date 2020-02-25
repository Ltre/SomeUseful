import requests,os,time
hcookies = {"Cookie":
        "SoundValue=0.50; alphaValue=0.80; __yamid_tt1=0.5630173980060627; __yamid_new=C8736F6698800001A3314BF01CD08350; udb_guiddata=4d0af64ce63b43f29a7a5975d914b205; udb_accdata=undefined; Hm_lvt_51700b6c722f5bb4cf39906a596ea41f=1576679026,1576732023,1577338814,1577958774; guid=0ad6867c39df195e6201245925596308; isInLiveRoom=; udb_passdata=3; __yasmid=0.5630173980060627; web_qrlogin_confirm_id=07537ea4-50e2-4875-b740-6d96faf478f2; udb_uid=1199513272235; yyuid=1199513272235; udb_passport=35184377273454hy; username=35184377273454hy; udb_version=1.0; udb_origin=0; udb_status=1; h_unt=1582507113; __yaoldyyuid=1199513272235; _yasids=__rootsid%3DC8CDD793BB500001F81513A0DDB018DD; udb_biztoken=AQAR_ZWuvDSX-euEpEE_X9orLG5qCZzq3eWN2xe_Z6iOZ46k2l1ZCdRflqfiQUe0No_1vruXDQRGMqDSKPqJO-bi-XKG0-1lBTPxlnWOEQpM7FA56BTcKCb2kB1wFiiDY0fv16_OoJ_aGS47BPzVeV7XGUKzxscbm6x9QRQSydJKQSXAVD1x0pbn2WwTacI6XrI41UcoJuJ7qD2H5-Nz5ZUs7FGDgbprp9U1IBrw9_VungRuitvYpFjeVPLZayYtW2Y2BtNdDSJecgDKMEOpIG_v0lVh68j6dyiqac6juwuKNDUMhq89HBgEYCnUyZpp7fsk3FPzwbLG2GAxwOjFlnre; rep_cnt=24"
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
    
