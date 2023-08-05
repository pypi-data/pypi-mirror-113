
from .units import MassUnit, VolumeUnit, Moles, Unit
import re
from typing import Optional, Tuple
from .table import TABLE
from .substance import Substance
from .consts import Consts
from .enums import UnitType

# cases
# 1. given quantities -> find excess or how much is needed
# EXAMPLE ---> H2+O2->H2O :  X quantity of H + Y quantity of O
# 2. Final quantities given -> find initial quantities

# aos == Amount of Substance


class Quantities:
    coeff: float
    unit: Unit

    def __init__(self, user_input: str, molar_mass: float, unit_type: Optional[UnitType] = None):
        # user input of unit and quantity
        self.user_input = user_input

        # splits coefficient from the unit
        coeff, unit_str = self.split_coeff()

        # coefficient originally inputted by the user
        self.coeff = coeff

        # Checks if it's a mass, volume or mole
        if unit_type:
            # type of value (Mass, Volume, Mole)
            self.unit_type = unit_type
            self.unit = self.unit_type.value(unit_str)
        else:
            self.unit = self.check_unit(unit_str)

        # molar mass of substance
        self.molar_mass = molar_mass

        # the amount of grams or cubic meters after transforming the prefixes and coefficients
        self.quantity_value = coeff * 10**self.unit.final_exponent * self.unit.conv_value

        # atmospheric pressure
        self.pressure = 1

        # temperature
        self.temperature = 300

        # molar_volume
        self.molar_volume = (Consts.IDEALGAS * self.temperature)/self.pressure


    
    def split_coeff(self) -> Tuple[float, str]:
        '''
        separates coefficient from the index-unit
        Example 1: 5kg --> 5, kg
        Example 2: 4cl --> 4, cl
        '''
        # combines base units into a string
        
        regexp = r'^(\d+\.{0,1}\d*)([A-z\^\d]+)$'

        # Find with regexp
        match = re.match(regexp, self.user_input)
        if match:
            coeff = float(match.group(1)) if match.group(1) else 1
            return coeff, match.group(2)
        else:
            raise ValueError
    
    def get_SI_coeff(self):
        print(self.coeff*self.unit.conv_value)
        return self.coeff * self.unit.conv_value

    def check_unit(self, unit_str: str) -> Unit: 
        '''
        Checks to determine the appropriate class (i.e. Mass, Volume or Moles)

        Runs units.py through each class until a non-error solution is obtained
        '''
        unit_classes = [MassUnit, VolumeUnit, Moles]

        for unit_cls in unit_classes:
            try:
                return unit_cls(unit_str)
            except:
                continue

        raise ValueError(f'Unknown units given - {unit_str}')
        

    def to_moles(self) -> float:
        '''
        converts mass (g) and volume (m^3) to moles (mol)
        '''
        if isinstance(self.unit, MassUnit):
            mole_value = self.quantity_value/self.molar_mass 

        elif isinstance(self.unit, VolumeUnit):
            mole_value = self.quantity_value/self.molar_volume

        else:
            # It's moles
            mole_value = self.quantity_value

        return mole_value

    def to_mass(self) -> float:
        '''
        converts volume (m^3) and moles (mol) to mass (g) 
        '''
        # TODO: Convert to optional units? To kg or whatever

        if isinstance(self.unit, VolumeUnit):
            mass_value = self.to_moles()*self.molar_mass
        elif isinstance(self.unit, Moles):
            mass_value = self.to_moles()*self.molar_mass        
        else:
            # it's mass
            mass_value = self.quantity_value

        return mass_value

    def to_volume(self) -> float:
        '''
        converts mass (g) and moles (mol) to volume (m^3)
        '''
        if isinstance(self.unit, MassUnit):
            volume_value = self.to_moles()*self.molar_volume
        elif isinstance(self.unit, Moles): 
            volume_value = self.quantity_value*self.molar_volume
        else:
            # it's volume
            volume_value = self.quantity_value
        return volume_value

   



