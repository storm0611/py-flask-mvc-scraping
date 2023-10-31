import os
from dotenv import load_dotenv

load_dotenv()

LIMIT = int(os.environ.get('LIMIT', None))
PROFILE_NUM = int(os.environ.get('PROFILE_NUM', 0))