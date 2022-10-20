from tree_sitter import Language, Parser
import pickle
import sys
from pathlib import Path

HERE = Path(__file__).absolute().parent
lib_ext = ".dll" if sys.platform == "win32" else ".so"
LIB_FILE = Path(HERE,f"languages{lib_ext}")
INDEX_FILE = Path(HERE,"index.pickle")

# DESerialization
with open(INDEX_FILE,"rb") as infile:
    lang_names = pickle.load(infile)


def get_language(language:str) -> Language:
    assert language in lang_names, "Not a valid language option!"
    return Language(str(LIB_FILE), language)


def get_parser(language:str) -> Parser:
    lang_obj = get_language(language)
    parser = Parser()
    parser.set_language(lang_obj)
    return parser

