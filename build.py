import subprocess
from pathlib import Path
from dataclasses import dataclass
import sys
from tree_sitter import Language

CLONE_DIR = Path("cloned-langs")
SCRIPT = Path(__file__).name
SRC = Path("src","ts_language_collection")

@dataclass
class TSLangRepo:
    url: str
    
    def directory(self) -> Path:
        return Path(self.url.rstrip("/").split("/")[-1])

    def lang_name(self) -> str:
        return self.directory().name.split("-")[-1]

with open("repos.txt", "r") as file:
    repos = [TSLangRepo(url.rstrip()) for url in file]

# clone_directory = os.path.join("vendor", url.rstrip("/").split("/")[-1])
# repos.append((url, commit, clone_directory))

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

if sys.platform == "win32":
    languages_filename = f"{SRC}\\languages.dll"
else:
    languages_filename = f"{SRC}/languages.so"

print(f"{SCRIPT}: Building", languages_filename)

Language.build_library( languages_filename, [Path(CLONE_DIR,r.directory()) for r in repos])
