## ОЛХ парсер
#### Установка
```bash
git clone https://github.com/lerdem/olx-parser
cd olx-parser/
docker-compose up -d
# run uploader via cron
                                    # full path to ads uploader script
crontab -e # than add: 0/5 * * * * docker exec -it olx- python -m ad.upload_ads
```
После выполненых шагов установки, подключите rss ссылку http://<ip где установлен server>:12345/detail-rss в свой rss ридер


#### Планы
- [ ] Вестка шаблона html для rss ридера
- [ ] Семантическое версионирование
- [ ] Парсинг номеров телефонов
- [ ] Конфигурация парсинга всех объявллений(ads), а не только квартир
