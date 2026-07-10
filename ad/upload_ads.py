import sys
from time import sleep, time
from random import randint

from ad.core.errors import UseCaseError
from ad.implementations import ad_detail_uploader, create_ads_and_notify
from ad.logger import logger


def _upload_job():
    logger.debug('UPLOADER: started')
    while True:
        started = time()
        try:
            new_ad_ids = create_ads_and_notify()
        except UseCaseError as e:
            logger.error(f'UPLOADER: {e}')
            logger.debug(f'UPLOADER: duration {time() - started}')
        else:
            logger.debug(f'UPLOADER: Загружены ads {new_ad_ids}')
            for _id in new_ad_ids:
                try:
                    ad_detail_uploader(ad_id=_id)
                except Exception as e:
                    logger.error(
                        f'UPLOADER: Error with {_id}, {e}'
                    )
        logger.debug(f'UPLOADER: duration {time() - started}')
        time_to_wait = randint(60, 120)
        logger.debug(
            f'UPLOADER: waiting before upload from olx {time_to_wait} seconds'
        )
        sleep(time_to_wait)


if __name__ == '__main__':
    try:
        _upload_job()
    except KeyboardInterrupt:
        logger.debug("UPLOADER: [!] Ctrl+C detected!")
        sys.exit(0)
