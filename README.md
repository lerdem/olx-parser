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
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



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
    <a href="https://github.com/lerdem/olx-parser"><strong>Explore the docs »</strong></a>
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
2. frontend - любое приложение поддерживающие RSS протокол. Т.е. начиная [RSS клиентами](https://en.wikipedia.org/wiki/Comparison_of_feed_aggregators), заканчивая ботами в мессенжерах

### Системные заввисимости
<div id="prerequisites"></div>

Для установки backend необходимо иметь следующее ПО:
- [git](https://git-scm.com/downloads)
- docker
- либо на уровне провайдера открыть порт номер 12345 либо с помощью ufw

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
## Roadmap
<div id="roadmap"></div>

- [ ] Семантическое версионирование
- [ ] Добавить скрипт по генерации changelog на базе коммитов
- [ ] картинки в base64 (вопрос приватности)
    - [ ] размер картинок
- [ ] Проврка на уникальность поискового запроса
- [ ] Причины написания парсера
- [ ] Добавить альтернативу RSS
- [ ] Разное время парсинга для разных урлов
- [ ] Прокидывать ли тег в имя фида?
- [ ] Главная страница с:
    - [ ] Конфигурацией настроек парсера. Объявлений (из url/form)
    - [ ] Списком возможных фидов
    - [ ] Списком вариантов деплоя проекта
- [ ] Трансформация введенной урл в rss?
    - [ ] Сделать хранение csv опциональным
    - [ ] Разделять base и detail для экономии трафика
- [ ] Парсинг номеров телефонов
- [ ] Поддержка sentry

See the [open issues](https://github.com/lerdem/olx-parser/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">в начало</a>)</p>


<!-- LICENSE -->
## License
<div id="license"></div>

Распространяется под лицензиев GPL-3. [Детали](https://github.com/lerdem/olx-parser/blob/master/LICENSE).

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
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[frontend-example]: https://quiterss.org/en/download
[screenshot-1]: docs/screenshots/screenshot-1.png
