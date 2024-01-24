#!/bin/bash
echo start
while [ "hello" = "hello" ]; do
    while IFS= read -r line; do
        curl -u admin:password "$line/start"
        sleep 5
    done < "url_list.txt" 
    sleep 5m
done
echo Accidental termination
