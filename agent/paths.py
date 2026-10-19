"""Where CodeFix finds its files, from source or as the frozen desktop build (PyInstaller, see codefix.spec).

From source everything stays in this repository folder, as before. Frozen, the program folder is read-only
(Program Files, or a per-user install that an update replaces), so:
  bundle_dir()  read-only files shipped inside the build (frontend/dist): sys._MEIPASS
  data_dir()    everything CodeFix writes (projects/, data/, .env, the log): %APPDATA%\\CodeFix
"""
import os
import sys
from pathlib import Path

FROZEN = bool(getattr(sys, "frozen", False))
SOURCE_ROOT = Path(__file__).resolve().parent.parent


def bundle_dir():
    return Path(getattr(sys, "_MEIPASS", SOURCE_ROOT))


def data_dir():
    if FROZEN:
        return Path(os.getenv("APPDATA") or Path.home()) / "CodeFix"
    return SOURCE_ROOT


def home():
    """Root of projects/ and data/. CODEFIX_HOME wins, so tests and power users can move it."""
    return Path(os.getenv("CODEFIX_HOME") or data_dir())


def env_file():
    """The .env with GEMINI_API_KEY. Never bundled into the build: each user keeps their own."""
    return data_dir() / ".env"
