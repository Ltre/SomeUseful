for f in *
do
	if [ -d $f ]; then
		echo "$f"
		cd $f
		for ff in *
		do
			if [ -f $ff ]; then
				echo "$ff"
				mv $ff /root/b
			fi
		done
		cd ..
	fi
done
