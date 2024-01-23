from time import sleep
from random import randint

import punq

from ad.adapters.presenter import BaseAdTelegramPresenter
from ad.adapters.repository import TelegramSender, ViewsRepoCsv, GetBaseAdRepoCsv
from ad.core.adapters import Presenter
from ad.core.adapters.repository import GetRepo, ViewsRepo, Sender
from ad.core.errors import UseCaseError
from ad.core.usecases.ads_sender import AdsSenderUseCase
from ad.logger import logger


def _telegram_sender_job():
    logger.debug('Telegram sender started')
    while True:
        time_to_wait = randint(45, 120)
        logger.debug(f'waiting before send to telegram {time_to_wait} seconds')
        sleep(time_to_wait)
        try:
            ads_sender(tag=None)
        except UseCaseError as e:
            logger.error(e)
        else:
            logger.debug(f'Telegram sender отработал без ошибок')


if __name__ == '__main__':
    container = punq.Container()
    container.register(GetRepo, GetBaseAdRepoCsv)
    container.register(ViewsRepo, ViewsRepoCsv)
    container.register(Sender, TelegramSender)
    container.register(Presenter, BaseAdTelegramPresenter)
    container.register(AdsSenderUseCase)
    _ads_sender = container.resolve(AdsSenderUseCase)
    ads_sender = _ads_sender.execute

    _telegram_sender_job()
