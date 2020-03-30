#/bin/sh
source /root/u/milo.conf
runtime=0
cd /root/b/d/bilidt
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
            		mv "./${f}" "${arr[0]}/${f}"
    		done
        	echo "${f}上传成功"
        fi
	if [ -d "./${f}" ]
	then
		cd "./${f}"
		for i in *;do
			if [ -f "./${i}" ]
			then
				cd ..
				temp=${milostatic}
				rclone move "./${f}" "${temp}:milo/b/bilidt/${f}" --buffer-size 32M --transfers 4 -P --low-level-retries 1
				break
			else
				cd ..
			fi
			break
		done
		let runtime++
	fi
	if [ $runtime -ge 25 ]
	then
		source /root/u/milo.conf
		runtime=0
	fi
done
sleep 10
done
