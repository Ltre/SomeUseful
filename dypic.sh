#/bin/sh
source /root/u/milo.conf
runtime=0
cd /root/b/d/pic
while [ true ]
do
for f in *
do
        if [ -f "${f}" ]
        then
               	n=$(du -sk ${f} | awk '{print $1}')
                if [ $n -lt 8 ]
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
            temp=${milostatic}
            echo "$temp"
            echo "开始上传${f}至${temp}:milo/b/pic/${arr[0]}"
            #if [ ! -d "/home/${temp}/b/pic/${arr[0]}" ]
            #then mkdir -p "/home/${temp}/b/pic/${arr[0]}"
            #fi
            rclone move "${f}" "${temp}:milo/b/pic/${arr[0]}" --buffer-size 32M --transfers 4 -P --low-level-retries 1
            if [ -f "$f" ]
            then
                sleep 1
		let runtime++
		if [ $runtime -ge 25 ]
		then
			source milo.conf
			runtime=0
		fi
            #    milolist=("${milolist[@]:1:5}" $temp)
            fi
        done
        echo "${f}上传成功"
        fi
	let runtime++
	if [ $runtime -ge 25 ]
	then
		source /root/u/milo.conf
		runtime=0
	fi
done
sleep 10
done
