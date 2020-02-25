#/bin/sh
omilolist=(milo milo2 milo3 milo5 milo6 milo4)
milolist=(${omilolist[@]})
runtime=0
echo ${milolist[0]}
while [ true ]
do
	for f in *.flv
do
	if [ ${f} != "*.flv" ]
	then
		n=$(du -sm ${f} | awk '{print $1}')
		if [ $n -lt 2 ]
		then
			echo "${f} 文件过小，删除"
			rm "${f}"
			continue
		fi
		ffmpeg -i "${f}" -y -vcodec copy -acodec copy -flvflags add_keyframe_index  "waitting${f}"
		if [ -f "waitting${f}" ]
		then
			m=$(du -sm "waitting${f}" | awk '{print $1}')
			sum=$(($n-$m))
			echo "原：$n 新：$m"
			echo "文件大小误差$sum m"
			if [ $sum -lt 7 ]
			then
				mv "waitting${f}" ${f}
			else
				rm "waitting${f}"
			fi
		else
			echo "没有待转换文件"
		fi
		echo "${f}转换完成"	
		OLD_IFS="$IFS" 
		IFS="-" 
		arr=($f) 
		IFS="$OLD_IFS"
        while [ -f $f ]
        do
            #rclone move "${f}" "milo:milo/b/${arr[1]}" --bwlimit 10M
            temp=${milolist[0]}
	    echo "$temp"
            echo "开始上传${f}至${temp}:milo/b/${arr[1]}"
	    if [ ! -d "/home/${temp}/b/${arr[1]}" ]
            then mkdir -p "/home/${temp}/b/${arr[1]}"
            fi
            rclone move "${f}" "${temp}:milo/b/${arr[1]}" --buffer-size 32M --transfers 4 -P --low-level-retries 1
            if [ -f $f ]
            then
		    milolist=("${milolist[@]:1:5}" $temp)
            fi
		done
			echo "${f} 上传完成"
	fi
    let runtime++
    if [ $runtime -ge 25 ]
    then
	milolist=(${omilolist[@]})
        runtime=0
    fi
done
for f in *.mp4
do
	if [ ${f} != "*.mp4" ]
	then
		n=$(du -sm ${f} | awk '{print $1}')
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
		#rclone move "${f}" "milo:milo/b/huya/${arr[1]}" --bwlimit 10M
        while [ -f $f ]
        do
            temp=${milolist[0]}
	    echo "$temp"
            if [ ! -d "/home/${temp}/b/huya/${arr[1]}" ]
            then mkdir -p "/home/${temp}/b/huya/${arr[1]}"
            fi
            rclone move "${f}" "${temp}:milo/b/huya/${arr[1]}" --buffer-size 32M --transfers 4 -P --low-level-retries 1
            if [ -f $f ]
            then
		    milolist=("${milolist[@]:1:5}" $temp)
            fi
        done
		echo "${f}上传成功"
	fi
    let runtime++
    if [ $runtime -ge 25 ]
    then
        milolist=(${omilolist[@]})
        runtime=0
    fi
done
sleep 5
done
