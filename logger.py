import logging
import os
from datetime import datetime

class Logger:
    def __init__(self):
        LOG_DIR = "logs/"
        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR)
        self.LOG_DIR = LOG_DIR + "{}.log"
    
    def _update_config(self):
            curr_date = datetime.now().strftime("%Y-%m-%d")
            logging.basicConfig(
                filename = self.LOG_DIR.format(curr_date),
                filemode = 'a',
                format = '(%(asctime)s) %(name)s | %(message)s',
                datefmt = '%H:%M:%S',
                level = logging.INFO
            )

    def log(self, msg):
        self._update_config()
        logging.info(msg)