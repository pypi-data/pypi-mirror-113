import os
from pathlib import Path

HOME_DIR = str(Path.home())
DIR_NAME = ".pylista"
LISTS_DIR = os.path.join(HOME_DIR, DIR_NAME)
