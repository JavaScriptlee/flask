#!/bin/bash
echo start
while [ "hello" = "hello" ]; do
    while IFS= read -r line; do
        curl -u admin:password "$line/start"
        sleep 5
    done < "/users/a1d90ffb-5987-4aa3-a731-e9eee8998544/url_list.txt" 
    sleep 5m
done
echo Accidental termination
