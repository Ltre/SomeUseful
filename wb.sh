echo "输入微博路径："
read path
source /root/u/milo.conf
runtime=0
t=${milostatic}
while [ true ]
do
if [ -d ${path}/weibo ]
then
	cd ${path}/weibo
	for f in *;do
		if [ -d "./${f}" ]
		then
			cd "./${f}"
			for i in *;do
				if [ -d "./${i}" ]
				then
					cd "./${i}"
					for j in *;do
						if [ -d "./${j}" ]
						then
							cd "./${j}"
							for k in *;do
								if [ -f "./${k}" ]
								then
									cd ..
									echo "上传${f}的${i}/${j}"
									rclone move "./${j}" "${t}:milo/b/wb/${f}/${i}/${j}" -P
									break
								else
									cd ..
								fi
							done
						elif [ -f "./${j}" ]
						then
							echo "同步${f}${i}未下载${j}"
							rclone sync "./${j}" "${t}:milo/b/wb/${f}/${i}" -P
						else
							cd ..
						fi
					done
				fi
				if [ -f "./${i}" ]
				then
					echo "同步${f}配置文件${i}"
					rclone sync "./${i}" "${t}:milo/b/wb/${f}/${i}" -P
				fi
			done
		fi
		cd ${path}/weibo
	done
fi
sleep 5
done
