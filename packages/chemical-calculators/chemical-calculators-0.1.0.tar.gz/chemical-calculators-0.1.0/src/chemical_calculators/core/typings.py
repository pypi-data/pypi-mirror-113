from enum import Enum

from .unit import MassUnit, VolumeUnit, MolesUnit

# ENUMS


class UnitType(Enum):
    mass = MassUnit
    volume = VolumeUnit
    moles = MolesUnit


# EXCEPTIONS

class SpecificError(BaseException):
    pass


class ReactionQuantatiesUnmatch(BaseException):
    pass
