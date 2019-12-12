import sys,os
import time
import shutil
fp1 = '/root/b/'
fp2 = '/root/b/d/bu/'
fp3 = '/root/b/d/bu/bt/'

def ck(fp1,fp2,fstr):
    files = os.listdir(fp1)
    fnum = 0
    emp = 0
    hasf = 0

    for i in files:
        if fstr in i and not "waitting" in i:
            fnum+=1
            if fnum > 2:
                hasf = fp1+i
    files = fnum
    if fnum < 2:
        emp = fp1
    files2 = os.listdir(fp2)
    fnum = 0
    for i in files2:
        if fstr in i and not "waitting" in i:
            fnum += 1
            if fnum > 2:
                hasf = fp2+i
    files2 = fnum
    if fnum < 2:
       emp = fp2
    sys.stdout.write("\r\033[K"+fp1+": "+fstr+" "+str(files)+"\n\r\033[K"+fp2+": "+fstr+" "+str(files2))
    sys.stdout.write("\033[A")
    if emp and hasf:
        try:
            shutil.move(hasf,emp)
        except:
            pass
        time.sleep(1)
        sys.stdout.write("\r\033[K"+hasf+" to "+emp)
    time.sleep(1)

while 1:
    ck(fp1,fp2,'flv')
    ck(fp1,fp2,'mp4')
    ck(fp1,fp3,'flv')
    ck(fp1,fp3,'mp4')
    ck(fp2,fp3,'flv')
    ck(fp2,fp3,'mp4')
    time.sleep(5)
