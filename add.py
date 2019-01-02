import sys

with open("user.txt","a") as f:
    for i in sys.argv[1:]:
        for j in i.split(','):
            j = j.strip()
            ii = 0
            for line in open("user.txt").read().splitlines():
                if(line == j):
                    ii =1
                    break
            if(ii == 1):
                print("%s存在跳过" % )
                continue
            f.writelines(j)
            f.write('\n')
            f.close
            print('%s已添加' % j)
