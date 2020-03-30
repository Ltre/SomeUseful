import requests,os,time
import toml
def get_headers(header_raw):
    return dict(line.split(": ", 1) for line in header_raw.split("\n") if line != '')
def get_cookies(cookie_raw):
    return dict(line.split("=", 1) for line in cookie_raw.split("; "))
'''hcookies = {"Cookie":
        "SoundValue=0.50; alphaValue=0.80; __yamid_tt1=0.5630173980060627; __yamid_new=C8736F6698800001A3314BF01CD08350; udb_guiddata=4d0af64ce63b43f29a7a5975d914b205; first_username_flag=35184377273454hy_first_1; udb_accdata=undefined; Hm_lvt_51700b6c722f5bb4cf39906a596ea41f=1576679026,1576732023,1577338814,1577958774; guid=0ad6867c39df195e6201245925596308; udb_passdata=3; __yasmid=0.5630173980060627; isInLiveRoom=true; web_qrlogin_confirm_id=7c2b76b3-3478-4027-8623-8a781b8bdb42; udb_other=%7B%22lt%22%3A%221583155678597%22%2C%22isRem%22%3A%221%22%7D; udb_uid=1199513272235; yyuid=1199513272235; udb_passport=35184377273454hy; username=35184377273454hy; udb_version=1.0; udb_origin=0; udb_status=1; rep_cnt=17; h_unt=1583155740; __yaoldyyuid=1199513272235; _yasids=__rootsid%3DC8D04226B2600001E867E8201711C0A0; huya_flash_rep_cnt=16; udb_biztoken=AQCPgSb_RAp2Lkq_LRPzj-_3SooD7ucFltQSNoc09Z6JU3sujkVXK9djBMBhMuMScB6e27Y9xm4GX-U-j5aUATaeg26L4-ghXpi0qjWVMLkx0oC7WNpy2LIrs6RC9e6Z4UM3b0EkQEooqZDHMPRs6eiVfRvCtOuYqQjLoCUCxLtrSKPwC2Fsso4qAZFonDKQijGLUuD8WsAmj8kYe4T3XQ77DF15J0UEJPTi8iLWHmqCjLq3Sn4ewLBV8rInE6gyW7KVR398oLwQHTJJIqaPNQnG3eBTdFxqe3Pk2hcWfrjeBtlek34BpsyOap59iH6fn6rFgQTTW0ZnTt4-_FohOZAb; PHPSESSID=8q4kdj213rm41gjatak7lhg383; undefined=undefined; huya_web_rep_cnt=16"
        }'''
hcookies_raw = toml.load("/root/u/huya.conf")['hcookies_raw']
hcookies=get_cookies(hcookies_raw)
headers={"Accept":"application/json, text/javascript, */*; q=0.01","User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.0 Safari/534.20 QBWebViewUA/2 QBWebViewType/1 WKType/1","Referer":"http//i.huya.com/","Accept-Language":"zh-cn"}
url = 'https://fw.huya.com/dispatch?do=subscribeList&uid=1199513272235&page=1&pageSize=1000'
if not os.path.exists('huser.txt'):
    os.makedirs('huser.txt')
namelist = open('huser.txt').read().splitlines()
if namelist:
    print(len(namelist))
upurl='https://udblgn.huya.com/web/cookieExchange'
upheaders_raw='''user-agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36
content-type: application/json
accept: */*
origin: https://udblgn.huya.com
sec-fetch-site: same-origin
sec-fetch-mode: cors
referer: https://udblgn.huya.com/proxy.html'''
upheaders=get_headers(upheaders_raw)
d={"uri":20009,"version":"1.0","context":"1","appId":"5002","lcid":"2052","data":{"info":"w5/Ch8Obw5rDjcObwqvDksORw5vDosKRwqrCk8K/w6LDrsOew6LDo8OZwqjCr8KpwqzCncKmw5bDqcOvw6bDssO7w7jCpsOVw5zCqcK7wrvCusK9w4nCr8Onw6DDqcOJw4jCvsK2w5jEiMSJxIbEgMOzxILEgMOqxInElcORw5jDl8Ocw5TDmsOew4nDksO2w7TEgcO7w7vDnMORxJ7EnMSfxJrDlsO+xJ3EnMSlxKrDpcOdxIHEp8SyxLDEr8Sow7PDvcO2w7XClMKTwpnCoMKgwqDCmMKcwqDCpsKOw4LDkcOXw5PDpcOdwqTCq8Kqwq/Cp8KtwrHCnsKpwqDDrsO1w7XDp8O1w4zDqsOvw67DsMO9wqzDhcK9wr3DhsK/wrzCs8SBxIjEiMO6xIjDrsSBw73EjsSDwr7Dl8OPw5jDksORw47DhcSXxIjEmMSMxI3El8O2xJDEksShw5DDqcOgw53DlMSmxJfEp8SbxJzEpsSNxKnEq8Oew7fDrsOrw6LEqcSnxKzEq8StxLrDqcKewpbClsKfwpjClcKMw6LDlcORw6LDl8KSwqvCo8KswqbCpcKiwpnDm8Oow6bDqsOuw4HDo8Ovw7TDqcKkwr3CtsK5wrLCqcO4w7LEgsOww7jDkcOzw7/EhMO5wrTDjcOGw4nDgsK5xIjEhcSPxILEhcSLw4DDmcSbw4PDpcSLxJbElMSTxIzDiMO5w67DscOMw73EmsSkxJfEmsSgw5XDrsSww5jEm8SdxKzDnMO1w57EjcStxLHEtMSixKTEr8Spw6XEisS2w4fDmsOTw4zDlsOdworCscObw5/Dm8OQw6TCk8KewpXDmsOew6LDnMOmw5rDp8Ogwp7Ct8Kgw6jDrsO1w6fDtcOyw6bDssK0w7jDrcOwwrjEgsO2w7PEhsO1xIPCtMSQw4DCt8OZw7/EisSIxIfEgMK8w63DosOlw4DDt8SLxIjEm8SKxJjDicOixKTDjMSPxJHEoMOQw6nDksOTw57DlcSaxJ7EosScxKbEmsSnxKDDnsO3w6DErMSoxKvEqMSlxLHEqcStxKrDisOPw4jDicOYw4rDj8Oaw5bDnMOUw57DmMOgw5fDmcObw57Dm8Ofw6LDmsOjwp3DucKpwqDDjcOhw7XDq8O5w6nCpcOJw7PDscOuw7jDv8Kuw4fEicKxw7TDtsSFwrXDjsK3wrjDg8K6w7/Eg8SHxIHEi8O/xIzEhcODw5zDhcSNxJPEmsSMxJrEl8SLxJfDmcSbxI/EksScw57EosSfxKnEnMSfxKXDmsS2xLfDp8OexKnEn8StxKfEtsSjxKrEqcS4w6jEgcKGw5/DjsKUwqvCt8KWw6XDlMKZw5jDkMKSwp3ClMOWw6PDpMOhw6DDncK+w6jDnMOew6nDo8OjwqLCu8Kkw7zDqcO4wqjCs8Kqw6rDusO7w4/DvMOyw7TDnsOyw7/DuMK2w4/CuMOkxIfEk8SDxIfEiMO+w4DDi8OCxILEksSTw7LEhsSTxIzDisOjw4zDucSRxKHEocSSxJHEocSXw5XDoMOXxKbEo8SZxK3EoMSqxK7EqsOgw7nDosSYxKvEscO3w7fDqMOzwobDiMOHw5XDnsOKw53CscOcwo/CqMKRwqDCqsKiw5XCrcKqwqjCrsKrwqvCsMKswrHCtMK3wrPCtcOnwrTCtcOlwrjCvsK3wrjDgMOww4DDgsK9w4fCv8O2w4XDgsODw7nDu8O3w4nCusOFwrzEjsSAxIbEgsOBw5rDg8OEw4/DhsSNxIfEmsO0xJjEjcSMxJjEgMSixJ7EosSSxJnEmMOWw6/EqsSpxK3EnsOmw53EpMSexLHEksSlxLTEtcSsxLPEs8SZxLvDk8OXw4fDjsONwovCpMOfw57DosOTwpvCksOZw5PDpsK9w6PDmsOcw7DCvcOcwp3CtsOxw7DDtMOlwq3CpMOsw7fDiMOnw7XDvsOqw73DnsSBw73DvsO+xILEhcO3w7fCtsOPxIrEicSNw77DhsK9w77Ej8SNxJbEhcSTw4TDncOGxIjEjsSZxJfElsSPw43DmMOPxJfEosO/xKHEl8Shw7fEpMSkxKrEp8SlxJ/DncO2xKPEn8SrxLPEpsOuw6XEscSuxKrDqcKewofCqcKfwp/CnMKgwrHCosKjwqfCp8KowqHCosKjwqTCpsK3wqrCq8Kqwq7CvcOCwq3Cr8OCw4TCscK6wrbCucK1wqjEhA=="}}
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
        if not 'time' in str(e):
            print(e,r.json())
            while 1:
                try:
                    r = s.post(upurl,headers=upheaders,data=d,allow_redirects=False,timeout=10)
                    print(r.status_code,r.headers)
                    break
                except:
                    print('登录失败')
    finally:
        r.close()
        time.sleep(5)
    
