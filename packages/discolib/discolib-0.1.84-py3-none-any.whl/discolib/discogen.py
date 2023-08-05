import os
import pathlib
from distutils import dir_util

LANGUAGE_C = 'c'
CODEGEN_PATH = pathlib.Path(__file__).parent / 'codegen'

def _gen_c():
    # TODO: Parse disco.json @ CWD
    print(f'Generating C code at {os.getcwd()}...')
    clang_path = CODEGEN_PATH / 'clang'
    dir_util.copy_tree(clang_path, os.getcwd())
    # TODO: Modify required files


LANGUAGE_MAP = {
    LANGUAGE_C : _gen_c()
}
