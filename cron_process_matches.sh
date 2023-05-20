#!/bin/bash

if ! pgrep -f 'process_matches.py'
then
    nohup python /root/pyserver/process_matches.py & > /root/pyserver/log_process_matches.log
fi
