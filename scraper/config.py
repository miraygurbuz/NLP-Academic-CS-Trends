import os
import logging

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
}

def setup_logger(name='scraper_logger', log_file='scraper.log'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    file_formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler = logging.FileHandler(log_file, mode='a')
    file_handler.setFormatter(file_formatter)
    stream_formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(stream_formatter)
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
TEMP_DIR = os.path.join(DATA_DIR, 'temp')
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

BASE_URL = 'https://arxiv.org/search/advanced'
DEFAULT_TERM = 'ACM OR IEEE'
SECOND_TERM = 'Springer OR Elsevier'
CLASSIFICATION_COMPUTER_SCIENCE = 'y'
INCLUDE_CROSS_LIST = 'exclude'
SIZE = 200
ORDER = ''
ABSTRACTS = 'show'

OUTPUT1_CSV = os.path.join(DATA_DIR, 'data1.csv')
OUTPUT2_CSV = os.path.join(DATA_DIR, 'data2.csv')
MERGED_OUTPUT_CSV = os.path.join(DATA_DIR, 'merged.csv')
Y_MERGED_OUTPUT_CSV = os.path.join(DATA_DIR, 'yearly_merged.csv')

def get_output_file(year):
    return os.path.join(DATA_DIR, f'data_{year}.csv')
