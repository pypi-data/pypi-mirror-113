import re


class Composition(dict):
    '''
    Helper class for substance.

    Generally it is a dict[str, int]

    TODO: Provide some examples
    '''

    def __init__(self, data, *args, **kwargs) -> None:
        super(Composition, self).__init__(*args, **kwargs)

        if isinstance(data, dict):
            for key, val in data.items():
                self[key] = val
        else:
            self.parse(data)

    def parse(self, formula: str):
        pattern = r'([A-Z]{1}[a-z]{0,1})(\d*)'
        res = re.findall(pattern, formula)

        for atom, index in res:
            if index == '':
                index = 1
            if not atom in self:
                self.setdefault(atom, 0)
            self[atom] += int(index)

    def __add__(self, comp: 'Composition') -> 'Composition':
        if isinstance(comp, Composition):
            new_data = dict(self)

            for atom, index in comp.items():
                if not atom in new_data:
                    new_data.setdefault(atom, 0)
                new_data[atom] += index

            return Composition(new_data)
        else:
            raise ValueError(
                'Only addition between two Composition instances is allowed')

    def __iadd__(self, comp: 'Composition') -> 'Composition':
        if isinstance(comp, Composition):
            for atom, index in comp.items():
                if not atom in self:
                    self.setdefault(atom, 0)
                self[atom] += index

            return self
        else:
            raise ValueError(
                'Only addition between two Composition instances is allowed')

    def __mul__(self, factor: int):
        if isinstance(factor, int):
            new_data = {key: val * factor for key,
                        val in self.items()}

            return Composition(new_data)
        else:
            raise ValueError(f'The factor type must be `int`')

    def __imul__(self, factor: int) -> 'Composition':
        if isinstance(factor, int):
            for key, val in self.items():
                self[key] = val * factor

            return self
        else:
            raise ValueError(f'The factor type must be `int`')

    def __str__(self):
        res = [f'{key}{val}' for key, val in self.items()]
        return ''.join(res)
