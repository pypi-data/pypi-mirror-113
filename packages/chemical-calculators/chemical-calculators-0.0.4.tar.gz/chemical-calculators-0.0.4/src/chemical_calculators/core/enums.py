from enum import Enum
from .units import MassUnit, VolumeUnit, Moles

class UnitType(Enum):
    mass = MassUnit
    volume = VolumeUnit
    moles = Moles
