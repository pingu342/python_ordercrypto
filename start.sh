#!/bin/sh
cd `dirname $0`

if [ -z $ENV_ORDERCRYPTO_DATA_DIR ]; then
	echo 'Please set the "ENV_ORDERCRYPTO_DATA_DIR" environment variable and try again.' >&2
	exit -1
fi

dir=$ENV_ORDERCRYPTO_DATA_DIR
file='config.yaml'
path="${dir%/}/${file}"
echo "Check $path"
if ! [ -e $path ]; then
	echo 'Copy initial files to data directory.'
	cp -R data/. $dir
fi

. ~/virtualenv/bitbankcc/bin/activate

echo 'Start Http server.'
cd server
python -m http.server 5555 --cgi &

cd ..
echo 'Start ordering periodicaly.'
while true;do
  python order.py; sleep 60
done
