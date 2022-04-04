from enum import Enum
#this position class improves readablity and better pattern matching
class PositionType(Enum):
    Long = 1,
    Short = -1,
    Flat = 9,
    Hold = 0,
    def name(self):
        if self == PositionType.Long:
            return "Long"
        elif self == PositionType.Short:
            return "Short"
        elif self == PositionType.Flat:
            return "Flat"
        elif self == PositionType.Hold:
            return "Hold"

def position_from_value(value) -> PositionType:
    """Matches a position type from a value"""
    for position_type in PositionType:
        if position_type.value == value:
            return position_type
    raise ValueError('Invalid position type value: {}'.format(value))