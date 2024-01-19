from time import sleep
import logging
from random import randint

from ad.core.errors import UseCaseError
from ad.implementations import ad_detail_uploader, ads_creator


def _upload_job():
    logger.debug('uploader started')
    while True:
        time_to_wait = randint(45, 120)
        logger.debug(f'waiting before upload from olx {time_to_wait} seconds')
        sleep(time_to_wait)
        try:
            new_ad_ids = ads_creator()
        except UseCaseError as e:
            logger.error(e)
        else:
            logger.debug(f'Загружены ads: {new_ad_ids}')
            for _id in new_ad_ids:
                try:
                    ad_detail_uploader(ad_id=_id)
                except Exception as e:
                    logger.error(f'Error with {_id}, {e}')


if __name__ == '__main__':
    logger = logging.getLogger('upload-logger')
    handler = logging.FileHandler('cron-upload_ads-logs.txt')
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    _upload_job()
