#/bin/sh
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
		echo "开始上传${f}至milo:milo/b/${arr[1]}"
		#rclone move "${f}" "milo:milo/b/${arr[1]}" --bwlimit 10M
		if [ ! -d "/home/milo/b/${arr[1]}" ]
		then mkdir -p "/home/milo/b/${arr[1]}"
        fi
        #mv  "${f}" "/home/milo/b/${arr[1]}"
		rclone move "${f}" "milo:milo/b/${arr[1]}" --buffer-size 32M --transfers 4 -P --low-level-retries 1 
		if [ -f $f ]
		then if [ ! -d "/home/milo2/b/${arr[1]}" ]
			then mkdir -p "/home/milo2/b/${arr[1]}"
			fi
			#mv  "${f}" "/home/milo2/b/${arr[1]}"
			echo "开始上传${f}至milo2:milo/b/${arr[1]}"
			rclone move "${f}" "milo2:milo/b/${arr[1]}" --buffer-size 32M --transfers 4 -P --low-level-retries 1
			if [ -f $f ]
			then if [ ! -d "/home/milo3/b/${arr[1]}" ]
				then mkdir -p "/home/milo3/b/${arr[1]}"
				fi
				#mv  "${f}" "/home/milo3/b/${arr[1]}"
				echo "开始上传${f}至milo3:milo/b/${arr[1]}"
				rclone move "${f}" "milo3:milo/b/${arr[1]}" --buffer-size 32M --transfers 4  -P --low-level-retries 1
				if [ -f $f ]
				then if [ ! -d "/home/milo4/b/${arr[1]}" ]
					then mkdir -p "/home/milo4/b/${arr[1]}"
					fi
					echo "开始上传${f}至milo4:milo/b/${arr[1]}"
					rclone move "${f}" "milo4:milo/b/${arr[1]}" --buffer-size 32M --transfers 4  -P --low-level-retries 1
				fi
			fi
		fi
		if [ ! -f $f ]
		then
			#rclone copy "${f}" "milo:milo/b/${arr[1]}" --bwlimit 10M
			echo "${f} 上传完成"
			#rm "${f}"
		else
			echo "${f} 未上传"
		fi
	else
		sleep 1
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
		if [ ! -d "/home/milo/b/huya/${arr[1]}" ]
		then mkdir -p "/home/milo/b/huya/${arr[1]}"
		fi
		#mv  "${f}" "/home/milo/b/huya/${arr[1]}"
		echo "开始上传${f}至milo:milo/b/huya/${arr[1]}"
		rclone move "${f}" "milo:milo/b/huya/${arr[1]}" --buffer-size 32M --transfers 4 -P --low-level-retries 1
		if [ -f $f ]
		then if [ ! -d "/home/milo2/b/huya/${arr[1]}" ]
			then mkdir -p "/home/milo2/b/huya/${arr[1]}"
			fi
			#mv  "${f}" "/home/milo2/b/huya/${arr[1]}"
			echo "开始上传${f}至milo2:milo/b/${arr[1]}"
			rclone move "${f}" "milo2:milo/b/huya/${arr[1]}" --buffer-size 32M --transfers 4 -P --low-level-retries 1
			if [ -f $f ]
			then if [ ! -d "/home/milo3/b/huya/${arr[1]}" ]
				then mkdir -p "/home/milo3/b/huya/${arr[1]}"
				fi
				#mv  "${f}" "/home/milo3/b/huya/${arr[1]}"
				echo "开始上传${f}至milo3:milo/b/${arr[1]}"
				rclone move "${f}" "milo3:milo/b/huya/${arr[1]}" --buffer-size 32M --transfers 4 -P --low-level-retries 1
				if [ -f $f ]
				then if [ ! -d "/home/milo4/b/huya/${arr[1]}" ]
					then mkdir -p "/home/milo4/b/huya/${arr[1]}"
					fi
					echo "开始上传${f}至milo4:milo/b/${arr[1]}"
					rclone move "${f}" "milo4:milo/b/huya/${arr[1]}" --buffer-size 32M --transfers 4 -P --low-level-retries 1
				fi
			fi
		fi
		if [ ! -f $f ]
		then
			echo "${f}上传成功"
			#rm "${f}"
		else
			echo "${f} 未上传"
		fi
	else
		sleep 1
	fi
done
sleep 5
done
