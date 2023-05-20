#!/bin/bash

if ! pgrep -f 'schedule_runs.py'
then
    nohup python /root/pyserver/schedule_runs.py & > /root/pyserver/log_schedule_runs.log
fi
