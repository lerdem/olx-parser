<div id="top"></div>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![GPL-3 License][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
<!--
  <a href="https://github.com/lerdem/olx-parser">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>
-->

<h3 align="center">Олх парсер с оповещением</h3>

  <p align="center">
    Возможности:
    <ul>
        <li>Скачивание данных объявлений с ОЛХ по поисковому запросу</li>
        <li>Сохранение данных объявлений в csv формате</li>
        <li>RSS лента для отслеживаия/мониторинга поискового запроса</li>
    </ul>
    <br />
    <a href="https://github.com/lerdem/olx-parser"><strong>Документация »</strong></a>
    <br />
    <br />
    <a href="https://github.com/lerdem/olx-parser">View Demo</a>
    ·
    <a href="https://github.com/lerdem/olx-parser/issues">Report Bug</a>
    ·
    <a href="https://github.com/lerdem/olx-parser/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Содержание</summary>
  <ol>
    <li><a href="#about-the-project">О проекте</a></li>
    <li>
      <a href="#getting-started">Начало</a>
      <ul>
        <li><a href="#prerequisites">Системные заввисимости</a></li>
        <li><a href="#installation">Установка backend</a></li>
      </ul>
    </li>
    <li><a href="#usage">Использование</a></li>
    <li><a href="#roadmap">Планы доработок</a></li>
    <li><a href="#reasons-for-creating-project">Причины создания проекта</a></li>
    <li><a href="#license">Лицензия</a></li>
    <li><a href="#acknowledgments">Благодарности</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## О проекте
<div id="about-the-project"></div>

![Скриншот поиска "аренды жилья" в клиенте QuiteRSS][screenshot-1]

<p align="right">(<a href="#top">в начало</a>)</p>



<!-- GETTING STARTED -->
## Начало
<div id="getting-started"></div>

Верхнеуровнево проект состорит из двух частей:
1. backend - состотит из веб приложения и процесса который загружает данные из ОЛХ объявлений
2. frontend - любое приложение поддерживающие [RSS протокол](https://ru.wikipedia.org/wiki/RSS).
Т.е. начиная [RSS клиентами](https://en.wikipedia.org/wiki/Comparison_of_feed_aggregators), заканчивая ботами в мессенжерах ([пример](https://github.com/BoKKeR/RSS-to-Telegram-Bot))

### Системные заввисимости
<div id="prerequisites"></div>

Для установки backend необходимо иметь следующее ПО:
- [git](https://git-scm.com/downloads)
- [docker](https://docs.docker.com/engine/install/)
- [docker-compose](https://docs.docker.com/compose/install/)
- либо на уровне провайдера открыть порт номер 12345 либо с помощью [ufw](https://wiki.ubuntu.com/UncomplicatedFirewall)

Работу с frontend рассмотрим на примере RSS клиента [QuiteRSS][frontend-example]

### Установка backend
<div id="installation"></div>

1. Клонирование репозитория
   ```sh
   git clone https://github.com/lerdem/olx-parser.git
   ```
2. Установка поисковых запросов для мониторинга в файле configuration.json ([пример конфигурации](https://github.com/lerdem/olx-parser/blob/master/configuration.json))
   ```sh
   cd olx-parser/ && nano configuration.json
   ```
3. Сборка и запуск backend
    ```sh
    docker-compose up -d --build
   ```
4. Создание *.csv файлов для хранения деталей объявлений
    ```sh
   docker exec -it olx-server python -m ad.adapters.repository
   ```

<p align="right">(<a href="#top">в начало</a>)</p>



<!-- USAGE EXAMPLES -->
## Использование
<div id="usage"></div>

Необходимо добавить feed в выбраный вами вариант frontend.
Для этого на примере QuiteRSS добавьте в feed (через Ctrl+N) ссылку
вида http://<ip сервера где установлен backend>:12345/detail-rss

<p align="right">(<a href="#top">в начало</a>)</p>



<!-- ROADMAP -->
## Планы доработок
<div id="roadmap"></div>

- [ ] Реклама в сообществах аренды жилья
- [ ] Сеть каналов по регионам
- [ ] Семантическое версионирование
- [ ] Добавить скрипт по генерации changelog на базе коммитов
- [ ] картинки в base64 (вопрос приватности т.к. загрузка идет с серверов олх)
    - [ ] размер картинок
- [ ] Добавить альтернативу RSS
- [ ] Разное время парсинга для разных урлов
- [ ] Главная страница с:
    - [ ] Конфигурацией настроек парсера. Объявлений (из url/form)
    - [ ] Списком возможных фидов
    - [ ] Списком вариантов деплоя проекта
- [ ] Трансформация введенной урл в rss?
    - [ ] Сделать хранение csv опциональным
    - [ ] Разделять base и detail для экономии трафика
- [ ] Поиск дубликатов фото объявлений и мошенников
    - [ ] Бан база по телефону и отзыву пользователей
- [ ] Парсинг номеров телефонов
- [ ] Поддержка [sentry](https://docs.sentry.io/platforms/python/)
- [ ] Валидация тегов и 404

See the [open issues](https://github.com/lerdem/olx-parser/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">в начало</a>)</p>


<!-- Reasons why -->
## Причины создания проекта
<div id="reasons-for-creating-project"></div>

Причина написания проекта родилась после осознания состояния рынка недвижимости.
До развала СССР рынка недвижимости не было, т.к. в СССР жилье было правом и гарантировалось конституцией, получали его не за деньги, а по распределению.
Сейчас, в 21 веке, капитализм распространен по большинству стран, следовательно, вместо самореализации в жизни человек вынужден выбирать максимально денежную работу для выплаты ипотеки/аренды недвижимости.
И попытка строительства в СССР прогрессивного экономического уклада **социализма** была призвана решить положение экономического принуждения человека.
Все аспекты прогрессивности социализма можно увидеть только сравнивая с **капитализмом**.
Капитализму как экономическому укладу свойственен рынок, посредством него происходит обмен товаров частных собственников.
Вопрос появления рынка недвижимости, был вопросом времени, но второстепенным в "лихие 90-е".
Первостепенным вопросом был, получение контроля на крупнейшими активами советского времени, т.е. **перевод собственности общественной на заводы/шахты/фабрики/земельные участки в собственность частную**.
После этого передела, вдруг бандиты стали бизнесменами и начались "честные" рыночные отношения(в истории такой процесс называется первичным накоплением капитала).
После уже появляются разнообразные рынки товаров и интересующий нас рынок недвижимости.

Конкретно будет рассматриваться аренда жилья, но из дальнейшего изложения можно увидеть сходства с другими рынками.
На этом рынке как и на любом другом есть **продавец** и **покупатель** у первого товар у второго деньги.
У каждого участника свои требования, например продавец ищет кандидатов со "стабильной" работой и региональной пропиской, арендатор ищет вариант недалеко от метро и максимально дешево.
Помимо требований бывает еще ряд проблем: мошенники, арестованное жилье, личностные черты характера участников сделки.
И вот, чтобы упростить все эти моменты на рынке появляется **посредник - риелтор**, часть проблем по поиску жилья от берет на себя.
Платит за его услуги зачастую покупатель.
Продавец здесь имеет более выгодное положение по отношению к покупателю, т.к. он собственник недвижимости и без него сделки не будет.
И вроде все логично, хочешь самостоятельно искать недвижимость - будет дешевле, дольше с поиском и согласованием, хочешь через риелтора - будет дороже, возможно быстрее с поиском и урегулирование берет на себя посредник.

Что упускается из этой логичной "картины"? Факторы **монополизации рынка и интернет**.
С развитием рынка менее конкурентных поглощают более конкурентные участники.
Т.е. на место множества малых(или одиночных) риелторов, со своими базами недвижимости, приходят меньшее множество фирм предоставляющими риелторские услуги.
И здесь риелтор уже просто наемный работник. Базы недвижимости становятся больше и в меньшем количестве рук.
И это явление монополизации происходит постоянно, т.к. это свойство рынка.
Теперь о другом факторе - интернет.
**Интернет стал условием для появления новой формы отношений между продавцом и покупателем.**
Стали появляться интернет магазины, доски объявлений(и ОЛХ который парсим в этом проекте).
Теперь проблема поиска недвижимости была сведена к обустройству системы(сайта) с возможностью публикации информации со стороны собственника и инструментами поиска и фильтрации со стороны соискателя.
И по началу появление таких сайтов упрощало взаимодействие людей при поиске недвижимости.
Но не забываем **это рынок и монополисты свой денежный интерес не упустят**.
Спустя время, доски объявлений станут платными, а объявления о недвижимости преимущественно будут от риелторских фирм.
Даже в ситуации когда человек не из их базы решит сдать недвижимость, для этого он разместит объявление на сайтах объявлений, после чего фирмы убеждают человека о необходимости сделки через них.

Итог, процесс монополизации рынка недвижимости в пользу риелторских фирм ставит в безвыходное положение соискателя.
Он практически не может отказаться от услуг риелторов.
Доски объявлений/сайты в своем рассвете приносящие пользу со временем стали орудием в руках монополистов.
С течением развития рынка недвижимости суть риелторской услуги это монопольное владение информацией о продавцах и продажа ее покупателю.
И не вся информация продается, а лишь информация про нужный объект недвижимости.
Т.е. оплата идет за нечто (информацию) производство которого равно публикации поста в социальной сети.
Интернет дает возможность обмениваться информацией бесплатно, но бизнесмены умудряются влезть в обмен и брать плату.
Описанный пример показывает паразитическую сущность капитализма в 21 веке.

Этот [проект](https://github.com/lerdem/olx-parser) как [авада-кедавра](https://dic.academic.ru/dic.nsf/ruwiki/152498) бессмертному, монопольное положение собственников риелторских фирм победить он не может.
Проект может лишь увеличишь шанс сделать звонок собственнику недвижимости до звонка риелтора.

Что нужно для победы над монополистами вообще?
**Нужна смена экономического уклада, смена капитализма социализмом**.
Любые попытки сопротивления антимонопольными законами или написания open source альтернатив, равно борьбе со следствиями.
Учитесь, анализируйте, действуйте!

<p align="right">(<a href="#top">в начало</a>)</p>


<!-- LICENSE -->
## Лицензия
<div id="license"></div>

Распространяется под лицензией GPL-3. [Детали](https://github.com/lerdem/olx-parser/blob/master/LICENSE).

<p align="right">(<a href="#top">в начало</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Благодарности
<div id="acknowledgments"></div>

* [Best-README-Template](https://github.com/othneildrew/Best-README-Template)

<p align="right">(<a href="#top">в начало</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/lerdem/olx-parser.svg?style=for-the-badge
[contributors-url]: https://github.com/lerdem/olx-parser/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/lerdem/olx-parser.svg?style=for-the-badge
[forks-url]: https://github.com/lerdem/olx-parser/network/members
[stars-shield]: https://img.shields.io/github/stars/lerdem/olx-parser.svg?style=for-the-badge
[stars-url]: https://github.com/lerdem/olx-parser/stargazers
[issues-shield]: https://img.shields.io/github/issues/lerdem/olx-parser.svg?style=for-the-badge
[issues-url]: https://github.com/lerdem/olx-parser/issues
[license-shield]: https://img.shields.io/github/license/lerdem/olx-parser.svg?style=for-the-badge
[license-url]: https://github.com/lerdem/olx-parser/blob/master/LICENSE.txt
[frontend-example]: https://quiterss.org/en/download
[screenshot-1]: docs/screenshots/screenshot-1.png
