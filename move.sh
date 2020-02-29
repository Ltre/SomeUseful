echo "输入路径"
read path
if [ ! -d $path ]; then
	echo "路径不存在"
else
cd $path
for f in *
do
	if [ -d "$f" ]; then
		echo "$f"
		cd "$f"
		for ff in *
		do
			if [ -f "$ff" ]; then
				echo "$ff"
				mv "$ff" ..
			fi
		done
		cd ..
	fi
done
fi
