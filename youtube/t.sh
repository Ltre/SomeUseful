if [ ! -d '/root/b/d/youtube' ]; then
	mkdir -p /root/b/d/youtube
fi
cd /root/b/d/youtube
for f in *
do
	if [ -d $f ]; then
		echo "$f"
		cd $f
		for ff in *
		do
			if [ -f $ff ]; then
				echo "$ff"
				mv $ff /root/b/d/youtube
			fi
		done
		cd ..
	fi
done
