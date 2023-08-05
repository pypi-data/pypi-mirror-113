'''
Periodic table.

'''

import json
from typing import Union

from .atom import Atom


class Table:

    def __init__(self):
        with open('data/table.json', 'r') as f:
            data = json.load(f)

        # No zero element
        self.elements = [Atom(index + 1, **item)
                         for index, item in enumerate(data)]

    def __getitem__(self, key: Union[str, int]) -> 'Atom':
        if type(key) is int:
            if 0 < key < 119:
                return self.elements[key - 1]
            else:
                raise ValueError(
                    'Only elements from 1 (H) to 118 (Og) are discovered so far')
        elif type(key) is str:
            try:
                return next(el for el in self.elements if el.symbol == key)
            except StopIteration:
                raise ValueError(f'Unknown element - `{key}`')
        else:
            raise ValueError(f'Integer between 1 and 118 or atom name was expected')

    def __repr__(self):
        return 'PERIODIC TABLE'


TABLE = Table()
