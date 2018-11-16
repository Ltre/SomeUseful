import os
import time


def main():
    os.system("apt-get install -y sqlite3 python3-lxml && pip3 install web.py==0.40-dev1 requests chardet sqlalchemy gevent psutil")
    while True:
        try:
            os.system('cd /root/i && python3 I*')
        except:
            pass
        finally:
            time.sleep(0.1)
        
if __name__ =="__main__":
    main()
