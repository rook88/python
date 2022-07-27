from IPython.core.magic import (register_line_magic, register_cell_magic, register_line_cell_magic)
from IPython.core.magic_arguments import (argument, magic_arguments, parse_argstring)

import __main__

@register_line_cell_magic
@magic_arguments()
@argument('-c', '--conversion',    help='Use __repr__ for conversion', action = 'store_true')

def cm(line, cell):
    args = parse_argstring(cm, line)
    code = cell
    if args.conversion:
        code = code.replace('}', '!r}')
    print(code.format(**vars(__main__)))

__version__ = 1.1
