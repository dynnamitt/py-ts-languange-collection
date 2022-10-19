from tree_sitter import Language, Parser, Node, Tree
from pathlib import Path
from typing import List
import sys


def init_langs(lang_names:List[str]) -> List[Language]:
    try:
        langs = [Language(OUT_LIB,n) for n in lang_names]
    except OSError as e:
            sys.stderr.write(str(e)+"\n")
            raise ImportError(f"Failed to find/open {OUT_LIB}")
     
