from .helpers import is_windows
import os

# JSON file paths
if is_windows():
    DATA_FILE = os.path.join(os.getenv("APPDATA"), "hourtrack", "data.json")
else:
    DATA_FILE = os.path.join(os.getenv("HOME"), ".hourtrack", "data.json")
