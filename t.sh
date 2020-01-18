#/bin/bash
name=milooo
folder=milo
echo "${name}"

sed -i '4i\name='${name}'' autoupload.sh
sed -i '4i\folder='${folder}'' autoupload.sh
