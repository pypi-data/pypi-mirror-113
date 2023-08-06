from string import ascii_letters
from itertools import product
from typing import Optional, NamedTuple

import re
import numpy as np

from .substance import Substance
from helpers.string import clean_ws

from .quantities import Quantities

from .Exceptions import ReactionQuantatiesUnmatch

class ReactionItem(Substance):
    quantity: Optional[Quantities]
    coeff: int
    user_moles: Optional[float]
    optimal_moles: float

    def __init__(self, data, coeff: int = 1, quantity: str = None, *args, **kwargs):
        super().__init__(data, *args, **kwargs)
        self.coeff = coeff

        self.quantity = Quantities(quantity, self.mass) if quantity else None
        self.user_moles = self.quantity.to_moles() if self.quantity else None
        
    @property    
    def normalized_moles(self) -> float:
        '''
        
        '''
        if self.coeff and self.user_moles:
            return self.user_moles / self.coeff
        else:
            return 0

    @property
    def excess(self) -> float:
        if self.user_moles:
            return self.user_moles - self.optimal_moles
        else:
            return 0

    def __str__(self):
        formula = super().__str__()
        coeff = '' if self.coeff == 1 else self.coeff
        if self.quantity:
            return f'{coeff}{formula} ({self.quantity.to_moles()}mol)'
        else:
            return f'{coeff}{formula}'

    def __repr__(self):
        res = super().__repr__()
        return f'{self.coeff}{res}'

class Reaction:
    '''
    Reaction class.

    Is responsible for BALANCING equations and calculating EXCESS
    '''

    equation: str
    atoms: set[str]
    
    reactants: list[ReactionItem]
    products: list[ReactionItem]
    reaction_items: list[ReactionItem]

    # List like ['5kg', '2mol', '']
    quantities: Optional[list[str]]

    solution: list[int]

    def __init__(self, equation: str, quantities: list[str] = None):  
        # TODO: Add comments
        self.equation = clean_ws(equation)
        self.validate()

        self.atoms = set([])
        self.reactants = []
        self.products = []
        self.reaction_items = []
        self.solution = []

        self.quantities = quantities if quantities else None

        # Splits the reaction into smaller components (REACTANTS, PRODUCTS, SUBSTANCES)
        self.parse()
        # Balances the equation
        self.solve()

        # Find optimal
        if self.quantities:
            self.normalize_reaction()

    def validate(self):
        # TODO: Improve validation
        '''
        Checks the validity of the reaction
            - Checks for '+' and '->' or '=' symbols
        '''

        subs_symbols = '[A-z\d\(\)\[\]]'
        reactant_pattern = f'({subs_symbols}+\+)*{subs_symbols}+'
        product_pattern = reactant_pattern

        pattern = '^{0}(=|->){1}$'.format(reactant_pattern, product_pattern)
        print(pattern)
        print(self.equation)
        check = re.match(pattern, self.equation)

        if not check:
            raise ValueError('Invalid reaction syntax')

    def parse(self):
        '''
        Splits the reaction into PRODUCTS and REACTANTS
        Splits each group into separate substances
        '''
        reaction_symbol = re.search(r'(->|=)', self.equation)
        if reaction_symbol:
            eq = self.equation.split(reaction_symbol.group(0))
        else:
            raise ValueError('No reaction symbol found')

        reactants, products = [item.split('+') for item in eq]
        substances = reactants + products

        if self.quantities:
            if not len(substances) == len(self.quantities):
                raise ReactionQuantatiesUnmatch
            sub_quant_pairs = zip(substances, self.quantities)
            self.reaction_items = [ReactionItem(sub, quantity=quant) for sub, quant in sub_quant_pairs]
        else:
            self.reaction_items = [ReactionItem(val) for val in substances]

        self.reactants = self.reaction_items[:len(reactants)]
        self.products = self.reaction_items[len(reactants):]

        # Update atoms list
        for subs in self.reactants:
            self.atoms.update(set(subs.composition.keys()))

    def get_coeffs_matrix(self):
        matrix = {key: [0]*len(self.reaction_items) for key in self.atoms}

        for i, item in enumerate(self.reaction_items):
            for atom, index in item.composition.items():
                if i < len(self.reactants):
                    matrix[atom][i] = index
                else:
                    matrix[atom][i] = -index

        return np.array(list(matrix.values()))

    def solve(self):
        '''
        Balances the equation
        '''
        coeffs = self.get_coeffs_matrix()
        # The system of linear equations to be solved is represented in the form of matrix AX = B

        # Select all columns except the last one
        A = coeffs[:, :-1]

        # Select the last column
        B = -coeffs[:, -1]
        
        # Solution could be found as X = A^-1 * B
        # X = np.linalg.inv(A).dot(B)

        # Alternative way
        try:
            X = np.linalg.solve(A, B)
            self.find_coeffs(X)
        except:
            self.solve_backup()
        for i, item in enumerate(self.reaction_items):
            item.coeff = self.solution[i]


        # Check that all coeffs are integers
    def find_coeffs(self, X):
        for i in range(1,50):
            probe = i * X
            probe_int = np.around(probe)

            if np.allclose(probe, probe_int):
                solution = list(probe_int.astype(int))
                solution.append(i)
                self.solution = solution
                break

            #if the matrix isn't square
    def solve_backup(self):
        '''
        A backup balancing method
            - Used if the matrix isn't square
            - Takes longer but is 100% efficient
        '''
        coeffs = self.get_coeffs_matrix()
            #generates possible combinations
        combs = product(range(1, 12), repeat=coeffs.shape[1])

        for i in combs:
            solution = np.array(i)
            res = coeffs.dot(solution)

            if np.count_nonzero(res, axis=None) == 0:
                self.solution = list(solution)
                break

       

    def __str__(self):
        reactants = ' + '.join([str(item) for item in self.reactants])
        products = ' + '.join([str(item) for item in self.products])
        return f'{reactants} -> {products}'

    
    def normalize_reaction(self) -> None:
        '''
            Walk through reactants and find excess reactants

            CASES

            1. One reactant           --> find all missing values (perfect reaction)
            2. One product            --> find all missing values (perfect reaction)
            3. Two(+) reactants       --> find smallest one (mol/coeff), find ideal reaction, compare new ideal value to original and find excess
            4. Reactant and product   --> use product to find ideal reaction, compare ideal value (in reactant)
            5. Two(+) products?       -->

            ALGORITHM
            
            1. Walk through reaction items, calculate normalized moles from user data
            2. Define minimal amount, hold it (reactant or product)
            3. Walk through reactions item, calculate ideal normalized moles based on minimal amount
        '''

        # Check if all have quantity

        any_quantity = any([True for el in self.reactants if el.quantity])

        if not any_quantity:
            raise ValueError('Not enough data to find excess reactant')
        else:
            self.find_optimal_moles()
        
    def find_optimal_moles(self):
        '''
        
        Example of full cycle:
        React       3Pl + 2H3PO4 = 3H2 + Pl3(PO4)2
        User_moles    9       10
        normalized   *3       *5
        min_val      min
        optimal       9       6     9     3
        excess        0       4    
        '''

        # Normalize amount of moles by reaction coefficient
        side = self.reactants
        if any([bool(el.quantity) for el in self.products]):
            side = self.products

        normalized = [el.normalized_moles for el in side if el.normalized_moles > 0]
        
        # Find min value
        if len(normalized) > 0:
            min_val = min(normalized)

            # Find optimal values for the equation
            for el in self.reaction_items:
                el.optimal_moles = min_val*el.coeff
        
        


        

        
      
