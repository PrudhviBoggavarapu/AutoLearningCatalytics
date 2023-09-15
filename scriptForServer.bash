#!/bin/bash
nohup python3 main.py 
while true
do
! git pull --force | grep -q "Already up to date" && killall firefox 
sleep 3
echo "DoneLoop"
done&

while true 
do 
python3 main.py
done