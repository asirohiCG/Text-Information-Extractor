import logging
import os
from dotenv import load_dotenv

dotenv_path = os.path.join('.', '.env')
load_dotenv(dotenv_path)

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(name)s :: %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
tie_logger = logging.getLogger("tie")
formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(name)s :: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler = logging.FileHandler(os.getenv('LOG_FILE_PATH'))
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
tie_logger.addHandler(file_handler)
werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.setLevel(logging.INFO)
werkzeug_logger.addHandler(file_handler)
