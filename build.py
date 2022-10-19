import subprocess
from pathlib import Path
from dataclasses import dataclass
import pickle
from tree_sitter import Language # external-lib

import src.ts_language_collection.common as common 

REPOS = Path("repos.txt")
CLONE_DIR = Path("cloned-langs")
SCRIPT = Path(__file__).name
DEST = Path("src","ts_language_collection")

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
lib_dest = common.lib_filename(DEST)

print(f"{SCRIPT}: Building", lib_dest)

# pass the torch
Language.build_library( str(lib_dest), dir_paths)

lang_names = [r.lang_name() for r in repos]
index_dest = common.lang_names_index_file(DEST)

print(f"{SCRIPT}: Store index", index_dest)
with open(index_dest, "wb") as outfile:
	pickle.dump(lang_names, outfile)
