import logging
import os
from datatime import datatime
import os

#log file name
LOG_FILE_NAME = f"{datatime.now().strftime('%m%d%Y__%H%M_%S')}.log"

#log directory
LOG_FILE_DIR = os.path.join(os.getcwd(),"logs")

#create folder if not available
os.makedirs(LOG_FILE_DIR,exist_ok=True)

#log file path

LOG_FILE_PATH = os.path.join(LOG_FILE_DIR, LOG_FILE_NAME)

logging.basicConfig(
    filename=LOG_FILE_NAME,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(messsage)s",
    level=logging.INFO,
)
