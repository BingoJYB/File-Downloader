import os

LIBS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.join(LIBS_DIR, '..\\')

BASE_URL = 'https://www.deutsche-boerse.com'

URL = BASE_URL + '/dbg-en/investor-relations/statistics'

DATE_FORMAT = '%d-%m-%Y'
