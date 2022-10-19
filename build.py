import subprocess
from pathlib import Path
from dataclasses import dataclass
import pickle
import sys
from tree_sitter import Language # external-lib

REPOS = Path("repos.txt")
CLONE_DIR = Path("cloned-langs")
SCRIPT = Path(__file__).name
SRC = Path("src","ts_language_collection")
lib_ext = "dll" if sys.platform == "win32" else "so"
lib_filename = Path(SRC, f"languages.{lib_ext}")
lang_names_path = Path(SRC,"langs_index.pickle")

@dataclass
class TSLangRepo:
    url: str
    
    def directory(self) -> Path:
        return Path(self.url.rstrip("/").split("/")[-1])

    def lang_name(self) -> str:
        return self.directory().name.split("-")[-1]

with open(REPOS, "r") as file:
    repos = [TSLangRepo(url.rstrip()) for url in file]

# During the build, this script runs several times, and only needs to download
# repositories on first time.
if CLONE_DIR.is_dir() and len(list(CLONE_DIR.iterdir())) == len(repos):
    print(f"{SCRIPT}: Language repositories have been cloned already.")
else:
    # TODO: what if some-failed
    #        or repos.txt was changed in-between runs?
    CLONE_DIR.mkdir(exist_ok=True)
    for r in repos:
        print()
        print(f"{SCRIPT}: Cloning: {r.url} --> {CLONE_DIR.name}/{r.directory()}")
        print()
        # TODO: async
        subprocess.check_call(["git", "clone", r.url], cwd=CLONE_DIR.name)

print()

dir_paths = [Path(CLONE_DIR, r.directory()) for r in repos]

print(f"{SCRIPT}: Building", lib_filename)

# pass the torch
Language.build_library( str(lib_filename), dir_paths)

lang_names = [r.lang_name() for r in repos]

print(f"{SCRIPT}: Store index", lang_names_path)
with open(lang_names_path, "wb") as outfile:
 	# "wb" argument opens the file in binary mode
	pickle.dump(lang_names, outfile)
