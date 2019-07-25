from mail import send_mail
import os,time,sys
password = input("pass:")
filepath = "/root/b/d/d"
subject = "斗鱼没文件"
contents = "没有录制文件了，可能出错了，请检查"
retry = 0
while True:
    t = time.time()
    sys.stdout.write("\r检查文件中 {}".format(t))
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
        time.sleep(5)
