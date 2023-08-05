'''
Chemical substance class.

Features:

- Determines substance composition
- Calculates molar (atomic) mass of a substance
- Beautifies chemical formula for text output
'''

from string import ascii_letters
from typing import Optional

from .composition import Composition
from .table import TABLE
from helpers.string import subscript_it, clean_ws


import re


class Substance:
    '''
    Main class for substance.

    formula - something like `H2O`
    composition - self-descriptive, something like {'H': 2, 'O': 1}
    mass - molar (atomic) mass
    '''
    formula: str
    mass: float
    composition: Composition


    def __init__(self, formula: str):  #COMMENTS - ADD THEM!!!!

        # A clean version of the substance
        self.formula: str = clean_ws(formula)

        # Checks if the formula is valid
        self.validate()

        # Finds the composition of the substance
        self.find_composition()

        # Finds the molar mass of the substance
        self.find_mass()

    def validate(self):
        '''
        Checks the validity of the substance
            - Acceptable characters
            - Acceptable substances ( looks for atom-index pairs and checks the periodic table)
            - Brackets
        '''
        formula = self.formula
        if len(formula) == 0:
            # UI - bring to another level
            raise ValueError("don't be shy, type something")
        allowed_chars = ascii_letters + "1234567890()[]"

        for char in formula:
            if not char in allowed_chars:
                raise ValueError(f'Unknown char is given: `{char}`')

        pattern = r'([A-Z]{1}[a-z]{0,1})(\d*)'
        Atom_index_pairs = re.findall(pattern, formula) #--> [[Atom, Index], [Atom, Index], [Atom, Index]]

        if not Atom_index_pairs:
            raise ValueError('Bad substance given')

        # Checks if the atom is real
        for atom, _ in Atom_index_pairs:
            test = TABLE[atom]

        pairs = [atom + index for atom, index in Atom_index_pairs]

        for pair in pairs:
            if pair in formula:
                formula = formula.replace(pair, '', 1)

        # Checking
        check_lowercase = re.match(r'[a-z]+', formula)

        if check_lowercase:
            raise ValueError(f'Unexpected lowercase letter')

        # Replacing all digits
        formula = re.sub(r'\d+', '', formula)
        brackets = {
            ']': '[',
            ')': '('
        }

        if len(formula) > 0:
            stack: list[str] = []
            for char in formula:
                if char in brackets.values():
                    stack.append(char)
                elif char in brackets.keys():
                    if stack[-1] == brackets[char]:
                        stack.pop()
                else:
                    raise ValueError(f'Unknown char found: `{char}`')

            if len(stack) > 0:
                raise ValueError('Bracket pairs do not match')

    def find_composition(self):
        '''
        Determines atomic composition of a substance
            - Determines separate atoms
            - Determines the quanitity of each atom
        EX: H2O --> H:2, O:1
        '''

        stack: list[str] = ['']

        bracket_index: Optional[str] = None

        for char in self.formula:
            if not bracket_index == None:
                if char.isnumeric():
                    bracket_index += char
                    continue
                else:
                    last = stack.pop()

                    stack[-1] += str(Composition(
                        last) * int(bracket_index))

                    bracket_index = None

            if char.isalnum():
                stack[-1] += char
            elif char in ['(', '[']:
                stack.append('')
            elif char in [')', ']']:
                bracket_index = ''

        # Checking end of a formula
        if bracket_index:
            last = stack.pop()
            stack[-1] += str(Composition(last) * int(bracket_index))

        self.composition = Composition(stack[0])

    def find_mass(self):
        '''
        Finds molar (atomic) mass of a substance
            - Uses quantities of each atom and their molar mass from the TABLE 
        '''

        self.mass = 0

        for atom, index in self.composition.items():
            self.mass += TABLE[atom].mass * index

        self.mass = round(self.mass, 3)

    def __str__(self):
        '''
        Returns beautified version of the formula with subscripts
        For example, `H2O` becomes `H₂O`
        '''

        return subscript_it(self.formula)

    def __repr__(self):
        return f'{str(self)} ({repr(self.composition)}, {self.mass} g/mol)'
