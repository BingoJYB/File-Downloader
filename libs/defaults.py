import os

# Directory path of libs
LIBS_DIR = os.path.dirname(os.path.abspath(__file__))

# Root path of project
ROOT_DIR = os.path.join(LIBS_DIR, '..\\')

# Default path of download files if no custom path in config csv file
DEFAULT_DOWNLOAD_DIR = os.path.join(ROOT_DIR, 'download_files')

# A csv file used for user custom download files
CONFIG_CSV = os.path.join(ROOT_DIR, 'config.csv')

# URLs for scraping
BASE_URL = 'https://www.deutsche-boerse.com'
URL = BASE_URL + '/dbg-en/investor-relations/statistics'

# Date formatter used in download file name
DATE_FORMAT = '%d-%m-%Y'
