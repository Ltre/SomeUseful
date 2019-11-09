#/bin/sh
if [ ! -d '/root/b/d/youtube' ]
then
	mkdir -p '/root/b/d/youtube'
fi
cd /root/b/d/youtube
while [ true ]
do
for f in *.ts
do
	if [ -f ${f} ]
	then	
		OLD_IFS="$IFS"
		IFS="-"
		arr=($f)
		IFS="$OLD_IFS"
		#rclone move "${f}" "milo:milo/b/huya/${arr[1]}" --bwlimit 10M
		if [ ! -d "/home/milo/b/youtube/${arr[0]}" ]
		then mkdir -p "/home/milo/b/youtube/${arr[0]}"
		fi
		#mv  "${f}" "/home/milo/b/huya/${arr[1]}"
		echo "开始上传${f}至milo:milo/b/youtube/${arr[0]}"
		rclone move "${f}" "milo:milo/b/youtube/${arr[0]}" -P --low-level-retries 1
		if [ -f $f ]
		then if [ ! -d "/home/milo2/b/youtube/${arr[0]}" ]
			then mkdir -p "/home/milo2/b/youtube/${arr[0]}"
			fi
			#mv  "${f}" "/home/milo2/b/huya/${arr[1]}"
			echo "开始上传${f}至milo2:milo/b/youtube/${arr[0]}"
			rclone move "${f}" "milo2:milo/b/youtube/${arr[0]}" -P --low-level-retries 1
			if [ -f $f ]
			then if [ ! -d "/home/milo3/b/huya/youtube/${arr[0]}" ]
				then mkdir -p "/home/milo3/b/youtube/${arr[0]}"
				fi
				#mv  "${f}" "/home/milo3/b/huya/${arr[1]}"
				echo "开始上传${f}至milo3:milo/b/youtube/${arr[0]}"
				rclone move "${f}" "milo3:milo/b/youtube/${arr[0]}" -P --low-level-retries 1
				if [ -f $f ]
				then if [ ! -d "/home/milo4/b/youtube/${arr[0]}" ]
					then mkdir -p "/home/milo4/b/youtube/${arr[0]}"
					fi
					echo "开始上传${f}至milo4:milo/b/youtube/${arr[0]}"
					rclone move "${f}" "milo4:milo/b/youtube/${arr[0]}"  -P --low-level-retries 1
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
