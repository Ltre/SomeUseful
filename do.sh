#/bin/sh
for f in *.flv
do
	ffmpeg -i "${f}" -y -vcodec copy -acodec copy "waitting${f}"
	rm -rf %{f}
	yamdi -i "waitting${f}" -o "${f}"
	rm -rf "waitting${f}"
	echo "${f}转换完成"

	OLD_IFS="$IFS" 
	IFS="-" 
	arr=($f) 
	IFS="$OLD_IFS"
	echo "开始上传${f}至milo:milo/b/${arr[1]}"
	rclone move "${f}" "milo:milo/b/${arr[1]}"
	sleep 5
done
echo "上传结束"
