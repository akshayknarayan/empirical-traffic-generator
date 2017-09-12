#!/bin/zsh

ps aux | grep ./bin/server | awk '{printf $2;printf " ";}' > a.txt
python kill.py
killall ./bin/client
rm -rf a.txt
./run-multiple-server.sh
./exp-help2.sh &
mm-delay 25 mm-link --downlink-queue=droptail --downlink-queue-args=\"packets=800\" ~/bw96.mahi ~/bw96.mahi ./exp-help1.sh $1
killall ./bin/client
killall ./bin/server
ps aux | grep ./bin/server | awk '{printf $2;printf " ";}' > a.txt
python kill.py
rm -rf a.txt
