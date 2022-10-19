
from pathlib import Path
import sys

lib_ext = "dll" if sys.platform == "win32" else "so"

def lib_filename(dir:Path):
    return Path(dir, f"languages.{lib_ext}")

def lang_names_index_file(dir:Path):
    return Path(dir, "langs_index.pickle")
