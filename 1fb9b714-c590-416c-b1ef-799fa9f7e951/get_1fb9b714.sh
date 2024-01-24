#!/bin/bash
echo start
while [ "hello" = "hello" ]; do
    while IFS= read -r line; do
        curl -u admin:password https://gfl.srt14gk.biz.id/start
        curl -u admin:password https://asft.aderving.bf/start
        curl -u admin:password https://smkl.ekuljfhx.cf/start
        curl -u admin:password https://tyjh.htfd.cf/start
        curl -u admin:password https://gl1.dinyue.link/start
        sleep 5
    done < "/root/flask/users/1fb9b714-c590-416c-b1ef-799fa9f7e951/url_list.txt" 
    sleep 5m
done
echo Accidental termination
