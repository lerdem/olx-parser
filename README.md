## ОЛХ парсер
### Возможности
##### Скачивание данных с объявлений ОЛХ по поисковому запросу
##### Сохранение данных в csv формате
##### RSS лента для отслеживаия поискового запроса

#### Установка
```bash
git clone https://github.com/lerdem/olx-parser
cd olx-parser/
docker-compose up -d --build
# run for creating empty .csv files
docker exec -it olx-server python -m ad.adapters.repository
# run uploader via cron for every 5 minutes
(crontab -l; echo "*/5 * * * * docker exec -it olx-server python -m ad.upload_ads > /dev/null 2>&1") | crontab -
```
После выполненых шагов установки, подключите rss ссылку http://<ip где установлен server>:12345/detail-rss в свой rss ридер


#### Планы
- [ ] Вестка шаблона html для rss ридера
- [ ] Семантическое версионирование
- [ ] Парсинг номеров телефонов
- [ ] Конфигурация парсинга всех объявллений(ads), а не только квартир
- [ ] Причины написания парсера
- [ ] Конфигурация поиска объявлений (из url/form)
