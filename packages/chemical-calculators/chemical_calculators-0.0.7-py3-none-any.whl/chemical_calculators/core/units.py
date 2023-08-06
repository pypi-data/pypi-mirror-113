import re
from typing import NamedTuple, Tuple
from .consts import Impirial


class FactorExpPair(NamedTuple):
    '''
    Creates parameters for  - Unit - Conversion - Exponent - relations
    Example 1: (gram, 1 (1 g = 1 g), 1 (exponent 1 applied to prefix)) --> (gram, 1, 1)
    Example 2: (pound, 453.592 (453.592 g = 1 lb), 1 (exponent 1 applied to prefix)) --> (pound, 453.592, 1)
    Example 3: (cubic inch, 0.0254^3 (0.0254^3 m^3 = 1 in^3), 3 (exponent 3 applied to prefix) --> (cubic inch, 0.0254^3, 3)
    '''
    names: list[str]
    # Hom nany units in base units, e.g. hom many meters in inch
    conv_value: float
    exp: float
   


class Unit:
    # holds user data (example cm^3, g, inch^3, etc.)
    user_input: str
    # conversion value, how many base units (g or m^3) fit into another unit (example: pound -> grams)
    conv_value: float
    # the final exponent with base 10. Is a multiplication of prefix exponent and unit exponent
    final_exponent: float
    
    prefixes = {
        'm': -3,
        'c': -2,
        'k': 3,
        'M': 6,
    }

    # Must be defined in children classes                                                       #cm^3
    DATA: list[FactorExpPair]

    def __init__(self, unit: str):
        '''
        unit: `cm^3`, for example
        '''
        if not (self.DATA):
            raise NotImplementedError('Child unit class must provide ...')
        
        prefix, unit = self.split_into_components(unit)                                         # c, m^3

        self.user_input = unit                                                                   # m^3

        data = self.get_data()                                                                  #(m^3, 1, 3)

      
        # Applies the appropriate exponent in accordance with the prefix
        if prefix:
            self.final_exponent = self.prefixes[prefix] * data.exp                             # -2 * 3 = -6
        else:
            self.final_exponent = 0

        self.conv_value = data.conv_value

    def get_data(self) -> FactorExpPair:
        '''
        Checks what unit it is (g, in, l, foot, etc.) in one of the child classes (depending on the iteration in check_unit func inside .quantities)
    
        Returns FactorExpPair
        '''
        for el in self.DATA:                      
            if self.user_input in el.names: 
                return el                                                                       #(m^3, 1, 3)
        raise ValueError()

    def split_into_components(self, unit) -> Tuple[str, str]:
        '''
        Splits the prefix from the units
        Example 1: kg -> k, g
        Example 2: cl -> c, l
        '''

        # combines base units into a string
        prefix = '|'.join(self.prefixes.keys())
        units = '|'.join(self.naming_list)# --> 'g'
        regexp = f'^({prefix})*({units})$'
        # regexp = f'^(\d+\.{0,1}\d*)(m|k|M)*(g|pound|l)$'
        # Find with regexp
        match = re.match(regexp, unit)
        if match:
            return match.group(1), match.group(2)
        else:
            raise ValueError


    def convert(self, to: str):
        # TODO: Implement
        pass

    def convert_to_user_unit(self):
        return self.convert(self.user_input)

    @property
    def naming_list(self):
        '''
        Creates a list of all possible units within MassUnit or VolumeUnit class (whichever is appropriate)
        This allows the program to check if the user has entered a recognized unit 
        (i.e. g, gram, pound, l, m^3 etc. and not something random)
        '''
        res = []
        for el in self.DATA:
            res += el.names
        return res

        
        


class MassUnit(Unit):
    '''
    Deals with mass units
    Base unit: Gram
    Examples: Gram, Pound, Short Tonne, Ounce, etc.
    '''
    DATA = [
        # Base unit
        FactorExpPair(['g','gram', 'grams'], 1, 1),
        # Other units
        FactorExpPair(['oz','ounce','ounces'], 28.3495, 1)
    ]
    


class VolumeUnit(Unit):
    '''
    Deals with volume units
    Base unit: Cubic meter
    Examples: Cubic meter, Cubic inch, Cubic foot, etc.
    '''
    DATA = [
        # Base unit
        FactorExpPair(['m\^3', 'm3'], 1, 3),
        # Other units
        FactorExpPair(['l','litre','litres'], 0.001, 1),
        FactorExpPair(['inch\^3', 'inch3', 'in\^3', 'in3'], Impirial.INCH ** 3, 3),
    ]


class Moles(Unit):
    DATA = [
        # Base unit
        FactorExpPair(['mol', 'moles'], 1, 1),
        
    ]

