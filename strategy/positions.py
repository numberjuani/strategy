from enum import Enum
#this position class improves readablity and better pattern matching
class PositionType(Enum):
    Long = 1,
    Short = -1,
    Flat = 9,
    Hold = 0,
    def name(self):
        match self:
            case PositionType.Long:
                return "Long"
            case PositionType.Short:
                return "Short"
            case PositionType.Flat:
                return "Flat"
            case PositionType.Hold:
                return "Hold"

def position_from_value(value) -> PositionType:
    """Matches a position type from a value"""
    for position_type in PositionType:
        if position_type.value == value:
            return position_type
    raise ValueError('Invalid position type value: {}'.format(value))