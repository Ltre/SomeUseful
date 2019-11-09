#/bin/sh
while [ true ]
do
cd /root/b/d/fc2

for f in *.ts
do
        if [ "${f}" != "*.ts" ]
        then
                OLD_IFS="$IFS"
                IFS="-"
                arr=($f)
                IFS="$OLD_IFS"
		#rclone move "${f}" "milo:milo/b/huya/${arr[1]}" --bwlimit 10M
		if [ ! -d "/home/milo/b/fc2/${arr[0]}" ]
                then mkdir -p "/home/milo/b/fc2/${arr[0]}"
                fi
                #mv  "${f}" "/home/milo/b/fc2/${arr[0]}"
		rclone move "${f}" "milo:milo/b/fc2/${arr[0]}" -P --low-level-retries 1
		if [ -f $f ]
		then if [ ! -d "/home/milo2/b/fc2/${arr[0]}" ]
                	then mkdir -p "/home/milo2/b/fc2/${arr[0]}"
                	fi
                	#mv  "${f}" "/home/milo2/b/fc2/${arr[0]}"
                	rclone move "${f}" "milo2:milo/b/fc2/${arr[0]}" -P --low-level-retries 1
			if [ -f $f ]
                	then if [ ! -d "/home/milo3/b/fc2/${arr[0]}" ]
                    	then mkdir -p "/home/milo3/b/fc2/${arr[0]}"
                    	fi
                    	#mv  "${f}" "/home/milo3/b/fc2/${arr[0]}"
			rclone move "${f}" "milo3:milo/b/fc2/${arr[0]}" -P --low-level-retries 1
			if [ -f $f ]
                	then if [ ! -d "/home/milo4/b/fc2/${arr[0]}" ]
                    	then mkdir -p "/home/milo4/b/fc2/${arr[0]}"
                    	fi
			rclone move "${f}" "milo4:milo/b/fc2/${arr[0]}" -P --low-level-retries 1
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
