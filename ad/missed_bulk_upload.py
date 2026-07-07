from ad.implementations import bulk_update_missed_detail_ads
from ad.logger import logger

if __name__ == '__main__':
    try:
        res = bulk_update_missed_detail_ads()
    except Exception as e:
        logger.error(f'Error with {e}')
    else:
        logger.debug(res)
