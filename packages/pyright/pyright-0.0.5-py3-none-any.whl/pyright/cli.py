import os
import sys
import logging
from typing import List, NoReturn

from . import node


log: logging.Logger = logging.getLogger(__name__)


def main(args: List[str]) -> int:
    version = os.environ.get('PYRIGHT_PYTHON_FORCE_VERSION')
    if version is None:
        version = node.latest('pyright')

    npx = node.version('npx')
    if npx[0] >= 7:
        return node.run('npx', '--yes', f'pyright@{version}', *args).returncode

    return node.run('npx', f'pyright@{version}', *args).returncode


def entrypoint() -> NoReturn:
    sys.exit(main(sys.argv[1:]))
