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
* * * * * python3 /root/pyserver/cron_process_matches.sh >> /root/pyserver/shlog.txt
* * * * * python3 /root/pyserver/cron_schedule_runs.sh >> /root/pyserver/shlogruns.txt
crontab -

