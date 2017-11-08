import logging
import logging.handlers

log_file_name = 'my_messenger.log'

logger = logging.getLogger(log_file_name)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - \
                               %(module)s - %(funcName)s - %(message)s')

fh = logging.FileHandler(log_file_name, encoding='utf-8')
fh = logging.handlers.TimedRotatingFileHandler(log_file_name, when='midnight', interval=1, backupCount=2)
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)

logger.addHandler(fh)
logger.setLevel(logging.DEBUG)