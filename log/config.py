import logging

logger = logging.getLogger('my_messenger')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - \
                               %(module)s - %(funcName)s - %(message)s')

fh = logging.FileHandler("my_messenger.log", encoding='utf-8')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)

logger.addHandler(fh)
logger.setLevel(logging.DEBUG)