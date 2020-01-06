sudo ps -ef | grep "python3 manage" | grep -v grep | cut -c 9-15 | xargs kill -s 9
sudo ps -ef | grep "python3 pika_rabbit" | grep -v grep | cut -c 9-15 | xargs kill -s 9
sudo ps -ef | grep "python3 crawl" | grep -v grep | cut -c 9-15 | xargs kill -s 9
nohup python3 manage.py runserver 0.0.0.0:8080 &
cd ffxivbot/
nohup python3 pika_rabbit.py &
cd ../utils
nohup python3 crawl_wb.py &
nohup python3 crawl_live.py &
cd ..
