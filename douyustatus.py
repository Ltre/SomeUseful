from mail import send_mail
import os,time,sys
from threading import Thread
password = input("pass:")
filepath = "/root/b/d/d"
filepath2 = "/root/b/d/huya"
filepath3 = '/root/b/d'
subject = "斗鱼没文件"
subject2 = "虎牙没文件"
subject3 = 'bilibili没文件'
contents = "没有录制文件了，可能出错了，请检查"
retry = 0
def running(filepath,subject,contents,password):
    while True:
        t = time.strftime('%c',time.localtime(time.time()))
        sys.stdout.write("\r{}检查文件中 当前时间{}".format(filepath,t))
        files = os.listdir(filepath)
        if not files:
            send_mail(subject,contents,password)
            time.sleep(60)
            retry = retry + 1
            if retry >= 10:
                retry = 0
                time.sleep(3600)
        else:
            retry = 0
            time.sleep(60)
a=Thread(target=running,args=(filepath,subject,contents,password,),name=('douyu'))
b=Thread(target=running,args=(filepath2,subject2,contents,password,),name=('huya'))
c=Thread(target=running,args=(filepath3,subject3,contents,password,),name=('bili'))

a.start()
b.start()
c.start()
a.join()
b.join()
c.join()
