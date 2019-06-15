import os,sys,subprocess,shutil
from threading import Thread
from concurrent.futures import ThreadPoolExecutor, wait
milo = input('输入文件夹：')
if milo =='1':
    milo = 'milo'
elif milo == '2':
    milo = 'milo2'
elif milo == '3':
    milo ='milo3'
filepath = '/home/{}/b/Twitch'.format(milo)
files = os.listdir(filepath)
di = 0
executor = ThreadPoolExecutor(20)
fs = []
def dojob(f):
    global di
    if os.path.isfile(f):
        
        fsize = os.path.getsize(f)
        fsize = fsize/(1024*1024)
        fsize = round(fsize,2)
        sys.stdout.write('\r \033[K'+f+' '+str(fsize)+'m')
        sys.stdout.flush()
        if fsize <= 1:
            #os.system('rm {}'.format(f))
            os.remove(f)
            di +=1
            sys.stdout.write('\r \033[K'+f+' 大小 '+str(fsize)+'m---已删除 '+str(di))
            sys.stdout.flush()
        else:
            shutil.move(f,'/root/b/d/Twitch')
for f in files:
    f =filepath+'/'+f
    if os.path.isfile(f):
        fs.append(executor.submit(dojob,f))
        '''
        sys.stdout.write('\r \033[K'+f)
        sys.stdout.flush()
        fsize = os.path.getsize(f)
        fsize = fsize/(1024*1024)
        fsize = round(fsize,2)
        if fsize <= 1:
            #os.system('rm {}'.format(f))
            os.remove(f)
            di +=1
            sys.stdout.write('\r \033[K'+f+'---已删除 '+str(di))
            sys.stdout.flush()
        '''
    else:
        sys.stdout.write('\r \033[K'+f)
        sys.stdout.flush()
        files2 = os.listdir(f)
        for f2 in files2:
            f2 = f + '/' + f2
            fs.append(executor.submit(dojob,f2))
            '''
            #do = Thread(target = dojob,args =(f2,),name = f2)
            if os.path.isfile(f2):
                fsize = os.path.getsize(f2)
                fsize = fsize/(1024*1024)
                fsize = round(fsize,2)
                if fsize <= 1:
                    #os.system('rm {}'.format(f2))
                    os.remove(f2)
                    di +=1
                    sys.stdout.write('\r \033[K'+f2+'---已删除 '+str(di))
                    sys.stdout.flush()
            '''
wait(fs)
sys.stdout.write('\r \033[K共删除{}'.format(di))

