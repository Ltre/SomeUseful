#/bin/sh
omilolist=(milo4)
milolist=(${omilolist[@]})
runtime=0
cd /root/bilidt
while [ true ]
do
for f in *
do
        if [ -f "${f}" ]
        then
               	n=$(du -sk ${f} | awk '{print $1}')
                if [ $n -lt 2 ]
                then
                        echo "${f} 文件过小，删除"
                        rm ${f}
                        continue
                fi 
		OLD_IFS="$IFS"
                IFS="-"
                arr=($f)
                IFS="$OLD_IFS"
                
        while [ -f "$f" ]
        do
            temp=${milolist[0]}
            echo "$temp"
            echo "开始上传${f}至${temp}:milo/b/bilidt/${arr[0]}"
            if [ ! -d "/home/${temp}/b/bilidt/${arr[0]}" ]
            then mkdir -p "/home/${temp}/b/bilidt/${arr[0]}"
            fi
            rclone move "${f}" "${temp}:milo/b/bilidt/${arr[0]}" --buffer-size 32M --transfers 4 -P --low-level-retries 1
            if [ -f "$f" ]
            then
                sleep 1
            #    milolist=("${milolist[@]:1:5}" $temp)
            fi
        done
        echo "${f}上传成功"
        fi
done
sleep 10
done
