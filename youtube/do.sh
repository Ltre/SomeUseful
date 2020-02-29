#/bin/sh
if [ ! -d '/root/b/d/youtube' ]
then
	mkdir -p '/root/b/d/youtube'
fi
source /root/u/milo.conf
runtime=0
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
		while [ -f ${f} ]
		do
			temp=${milolist[0]}
			echo "$temp"
			if [ ! -d "/home/${temp}/b/youtube/${arr[0]}" ]
			then mkdir -p "/home/${temp}/b/youtube/${arr[0]}"
			fi
			echo "开始上传${f}至${temp}:milo/b/youtube/${arr[0]}"
			rclone move "${f}" "${temp}:milo/b/youtube/${arr[0]}" -P --low-level-retries 1
			if [ -f "$f" ]
			then
				milolist=("${milolist[@]:1:5}" $temp)
			fi
		done
		echo "${f}上传成功"
		let runtime++
		if [ $runtime -ge 25 ]
		then
			source /root/u/milo.conf
			runtime=0
		fi

	fi
done
sleep 5
done
