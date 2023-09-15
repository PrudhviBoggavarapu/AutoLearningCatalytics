#!/bin/bash
while true
do
! git pull --force | grep -q "Already up to date" && killall firefox && python3 main.py
sleep 10
echo "DoneLoop"
done