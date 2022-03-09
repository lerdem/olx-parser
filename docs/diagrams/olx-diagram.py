from diagrams import Cluster, Diagram
from diagrams.custom import Custom
from diagrams.onprem.compute import Server


with Diagram('Архитектура приложения', show=False, filename='olx-parser-architecture'):
    with Cluster('Backend'):
        web = Server('Веб приложение')
        cron = Server('Загрузчик данных из ОЛХ')
        olx_server = Custom('Олх сайт', 'olx-icon.png')

        backend = [web, cron, olx_server]

    rss_client = Custom('RSS frontend', 'rss-icon.jpeg')

    rss_client >> web >> cron >> olx_server
