echo -n "请输入路径:"
read path
if [ ! -d $path ]; then
        mkdir -p $path
fi
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
                                mv "$ff" $path
                        fi
                done
                cd ..
        fi
done
