from dotenv import load_dotenv

from . import paths

# From source: the .env found from the repo folder, as before. Frozen: %APPDATA%\CodeFix\.env (agent/paths.py).
load_dotenv(paths.env_file() if paths.FROZEN else None)
