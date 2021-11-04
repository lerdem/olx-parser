## ОЛХ парсер
#### Установка
```bash
git clone https://github.com/lerdem/olx-parser
cd olx-parser/
pip install -r requirements.txt
# run uploader via cron
                                    # full path to ads uploader script
crontab -e # than add: 0/5 * * * * sh /home/user/olx-parser/upload_ads.sh
# run server for getting ads
nohup /home/user/olx-parser/venv/bin/python /home/lerdem/olx-parser/app.py > olx-server.txt &
```
После выполненых шагов установки, подключите rss ссылку http://<ip где установлен server>:12345/detail-rss в свой rss ридер
