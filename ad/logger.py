import logging

logger = logging.getLogger('upload-logger')
handler = logging.FileHandler('cron-upload_ads-logs.txt')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
