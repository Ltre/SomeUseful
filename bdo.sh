#/bin/sh
while [ true ]
do
	for f in *.flv
do
	if [ ${f} != "*.flv" ]
	then
		ffmpeg -i "${f}" -y -vcodec copy -acodec copy -copyts -g 1 "waitting${f}"
		#yamdi -i "waitting${f}" -o "${f}"
		mv "waitting${f}" ${f}
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
                mv  "${f}" "/home/milo/b/${arr[1]}"
		if [ -f $f ]
		then if [ ! -d "/home/milo2/b/${arr[1]}" ]
                	then mkdir -p "/home/milo2/b/${arr[1]}"
                	fi
                	mv  "${f}" "/home/milo2/b/${arr[1]}"
                	if [ -f $f ]
                	then if [ ! -d "/home/milo3/b/${arr[1]}" ]
                    	then mkdir -p "/home/milo3/b/${arr[1]}"
                    	fi
                    	mv  "${f}" "/home/milo3/b/${arr[1]}"
                    fi
		fi
			#rclone copy "${f}" "milo:milo/b/${arr[1]}" --bwlimit 10M
		echo "${f} 上传完成"
		#rm "${f}"
		
	else
		sleep 1
	fi
done
for f in *.mp4
do
        if [ ${f} != "*.mp4" ]
        then
                OLD_IFS="$IFS"
                IFS="-"
                arr=($f)
                IFS="$OLD_IFS"
		#rclone move "${f}" "milo:milo/b/huya/${arr[1]}" --bwlimit 10M
		if [ ! -d "/home/milo/b/huya/${arr[1]}" ]
                then mkdir -p "/home/milo/b/huya/${arr[1]}"
                fi
                mv  "${f}" "/home/milo/b/huya/${arr[1]}"
		if [ -f $f ]
		then if [ ! -d "/home/milo2/b/huya/${arr[1]}" ]
                	then mkdir -p "/home/milo2/b/huya/${arr[1]}"
                	fi
                	mv  "${f}" "/home/milo2/b/huya/${arr[1]}"
                	if [ -f $f ]
                	then if [ ! -d "/home/milo3/b/huya/${arr[1]}" ]
                    	then mkdir -p "/home/milo3/b/huya/${arr[1]}"
                    	fi
                    	mv  "${f}" "/home/milo3/b/huya/${arr[1]}"
                    fi
		fi
                echo "${f}上传成功"
                #rm "${f}"
        else
                sleep 1
        fi
done

sleep 5
done
