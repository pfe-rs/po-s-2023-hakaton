Regarding setting this up on a VPS

(TBD) how to provision
sudo apt update
sudo apt install python3 nginx gunicorn screen

to run flask server in background:
screen -S guni
gunicorn --max-requests 1 -w 5 pyserver:app
press ctrl+a and then d

initial database setup
run initial_database.py

to setup crons
sudo systemctl start cron
crontab -e
* * * * * /usr/bin/flock -n /tmp/fcj_proc.lockfile python3 /root/pyserver/schedule_runs.py >> /root/pyserver/log_schedule_runs.txt 2>&1
* * * * * /usr/bin/flock -n /tmp/fcj_sch.lockfile python3 /root/pyserver/process_matches.py >> /root/pyserver/log_process_matches.log 2>&1

chmod +x /root/pyserver/cron_*
