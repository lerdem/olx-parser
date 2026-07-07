import sys

from time import sleep
from random import randint
from ad.implementations import bulk_ads_deactivation
from ad.logger import logger


def _deactivate_job():
    logger.debug('DEACTIVATOR: started')
    while True:
        time_to_wait = randint(180, 240)
        logger.debug(
            f'DEACTIVATOR: waiting {time_to_wait} seconds before check ads status'
        )
        sleep(time_to_wait)
        try:
            res = bulk_ads_deactivation()
        except Exception as e:
            logger.error(f'DEACTIVATOR: Error with {e}')
        else:
            logger.debug(f'DEACTIVATOR: {res}')
        logger.debug(f'DEACTIVATOR: circle done')


if __name__ == '__main__':
    try:
        _deactivate_job()
    except KeyboardInterrupt:
        logger.debug("[!] Ctrl+C detected!")
        sys.exit(0)
