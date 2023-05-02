#!/bin/sh
./start_server.sh &
while true;do
  ./order.sh;sleep 60
done
