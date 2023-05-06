#!/bin/sh
cd `dirname $0`

if [ -z $ENV_ORDERCRYPTO_DATA_DIR ]; then
	echo 'Please set the "ENV_ORDERCRYPTO_DATA_DIR" environment variable and try again.' >&2
	exit -1
fi

dir=$ENV_ORDERCRYPTO_DATA_DIR
if ! [ -d $dir ]; then
	echo 'The directory specified in ENV_ORDERCRYPTO_DATA_DIR environment variable does not exist.' >&2
	exit -1
fi

file='config.yaml'
path="${dir%/}/${file}"
echo "Check $path"
if ! [ -e $path ]; then
	echo 'Copy initial files to data directory.'
	cp -R data/. $dir
fi

echo 'Start tor'
tor &
file=/var/lib/tor/hidden_service/hostname
while [ ! -f "$file" ]
do
  sleep 1
done
export APP_HIDDEN_SERVICE=$(cat $file | tr -d '[:space:]')

echo 'Start Http server.'
./start_server.sh >> $dir/server_log.txt 2>&1 &

echo 'Start ordering periodicaly.'
while true;do
 ./order.sh >> $dir/order_log.txt 2>&1; sleep 60
done

