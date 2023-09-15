#!/bin/bash
nohup python3 main.py 
while true
do
! git pull --force | grep -q "Already up to date" && killall firefox && nohup python3 main.py 
sleep 10
echo "DoneLoop"
done