from tree_sitter import Language, Parser
from .. import common
import pickle
from pathlib import Path

HERE = Path(__file__).absolute().parent

# DESerialization
with open(common.lang_names_index_file(HERE), "rb") as infile:
    lang_names = pickle.load(infile)


def get_language(language:str) -> Language:
    assert language in lang_names, "Not a valid language option!"
    return Language(str(common.lib_filename(HERE)), language)


def get_parser(language:str) -> Parser:
    lang_obj = get_language(language)
    parser = Parser()
    parser.set_language(lang_obj)
    return parser

