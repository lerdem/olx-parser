## ОЛХ парсер
### Возможности
##### Скачивание данных с объявлений ОЛХ по поисковому запросу
##### Сохранение данных в csv формате
##### RSS лента для отслеживаия поискового запроса

#### Установка
```bash
git clone https://github.com/lerdem/olx-parser
cd olx-parser/
# set url for monitor(serarch) in ad/core/usecases/create_base_ads.py:12
docker-compose up -d --build
# run for creating empty .csv files
docker exec -it olx-server python -m ad.adapters.repository
```
После выполненых шагов установки, подключите rss ссылку http://<ip где установлен server>:12345/detail-rss в свой rss ридер


#### Планы
- [ ] Вестка шаблона html для rss ридера
- [ ] Семантическое версионирование
- [ ] Упростить хранение csv(хранить частями со сборкой в конце)
    - [ ] удалить publication_date
- [ ] Парсинг номеров телефонов
- [ ] Причины написания парсера
- [ ] Конфигурация поиска объявлений (из url/form)
- [ ] Возможность добавления нескольких запросов на мониторинг
- [ ] Добавить скрипт по генерации changelog на базе коммитов
- [ ] Добавить альтернативу RSS
