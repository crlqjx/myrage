import os

from decolog.logger import Logger
from dotenv import load_dotenv


load_dotenv()


logger = Logger(
    app_name = os.environ['APP_NAME'],
    dir_path = os.environ['LOG_PATH']
)
