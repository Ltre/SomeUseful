#/bin/sh
while [ true ]
do
cd /root/b/d/pic
for f in *
do
        if [ -f "${f}" ]
	#if [ "${f}" != "*.mp4" ]
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
		if [ ! -d "/home/milo4/b/pic/${arr[0]}" ]
                then mkdir -p "/home/milo4/b/pic/${arr[0]}"
                fi
                #mv  "${f}" "/home/milo4/b/pic/${arr[0]}"
		echo "开始上传${f}至milo4:milo/b/pic/${arr[0]}"
		rclone move "${f}" "milo4:milo/b/pic/${arr[0]}" --buffer-size 32M --transfers 4 -P --low-level-retries 1
		if [ -f $f ]
		then if [ ! -d "/home/milo4/b/pic/${arr[0]}" ]
                	then mkdir -p "/home/milo4/b/pic/${arr[0]}"
                	fi
                	#mv  "${f}" "/home/milo4/b/pic/${arr[0]}"
                	echo "开始上传${f}至milo4:milo/b/pic/${arr[0]}"
			rclone move "${f}" "milo4:milo/b/pic/${arr[0]}" --buffer-size 32M --transfers 4 -P --low-level-retries 1
			if [ -f $f ]
                	then if [ ! -d "/home/milo4/b/pic/${arr[0]}" ]
                    	then mkdir -p "/home/milo4/b/pic/${arr[0]}"
                    	fi
                    	#mv  "${f}" "/home/milo4/b/pic/${arr[0]}"
			echo "开始上传${f}至milo4:milo/b/pic/${arr[0]}"
			rclone move "${f}" "milo4:milo/b/pic/${arr[0]}" --buffer-size 32M --transfers 4 -P --low-level-retries 1
			if [ -f $f ]
                	then if [ ! -d "/home/milo4/b/pic/${arr[0]}" ]
                    	then mkdir -p "/home/milo4/b/pic/${arr[0]}"
                    	fi
			echo "开始上传${f}至milo4:milo/b/pic/${arr[0]}"
			rclone move "${f}" "milo4:milo/b/pic/${arr[0]}" --buffer-size 32M --transfers 4 -P --low-level-retries 1
                    fi
                    fi
		fi
                echo "${f}上传成功"
                #rm "${f}"
        else
                sleep 1
        fi
done
sleep 10
done
