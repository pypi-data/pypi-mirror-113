class Atom:
    '''
    Atom class.

    Z: int
    symbol: str
    name: str
    mass: float
    electron_structure: list
    '''

    Z: int
    symbol: str
    mass: float

    def __init__(self, Z: int, symbol: str, mass: float):
        self.Z: int = Z
        self.symbol: str = symbol
        self.mass: float = mass

    def find_electron_structure(self):
        # TODO: implement
        pass

    def __repr__(self):
        return f'{self.symbol}\nMass: {self.mass}'
