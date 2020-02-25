#/bin/sh
omilolist=(milo milo2 milo3 milo5 milo6 milo4)
milolist=(${omilolist[@]})
runtime=0
cd /root/b/d/kr
while [ true ]
do
for f in *.ts
do
    if [ "${f}" != "*.ts" ]
    then
        n=$(du -sm "${f}" | awk '{print $1}')
        if [ $n -lt 2 ]
        then
            echo "${f} 文件过小，删除"
            rm "${f}"
            continue
        fi
        OLD_IFS="$IFS"
        IFS="-"
        arr=($f)
        IFS="$OLD_IFS"
    if [ ! -d "/home/${temp}/b/kr/${arr[0]}" ]
        then mkdir -p "/home/${temp}/b/kr/${arr[0]}"
        fi
    while [ -f "$f" ]
    do
        temp=${milolist[0]}
        echo "$temp"
        echo "保存${f}到${temp}:milo/b/kr/${arr[0]}"
        if [ ! -d "/home/${temp}/b/kr/${arr[0]}" ]
        then mkdir -p "/home/${temp}/b/kr/${arr[0]}"
        fi
        rclone move "${f}" "${temp}:milo/b/kr/${arr[0]}" --buffer-size 32M --transfers 4 -P --low-level-retries 1
        if [ -f "$f" ]
        then
            milolist=("${milolist[@]:1:5}" $temp)
        fi
    done
    echo "${f}上传成功"
    else
        sleep 1
    fi
    let runtime++
    if [ $runtime > 25 ]
    then
        milolist=(${omilolist[@]})
        runtime=0
    fi
done
sleep 10
done
