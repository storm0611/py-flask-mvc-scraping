import os
from dotenv import load_dotenv

load_dotenv()

try:
    LIMIT = int(os.environ.get('LIMIT', None))
except:
    LIMIT = None
PROFILE_NUM = int(os.environ.get('PROFILE_NUM', 0))