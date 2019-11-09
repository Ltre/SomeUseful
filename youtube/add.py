while 1:
    link = input('输入：')
    if not link or link=='q':
        exit(0)
    names = link.split('/')
    name = names[-2]+'/'+ names[-1]
    if 'youtu' in link:
        with open('youtube_names.txt','r+') as f:
            if not name in f.read().splitlines():
                f.write(name)
                f.write('\n')
                f.close()
                print('添加成功')
            else:
                print('该name已存在')

