from enum import Enum
# this can be used as inputs to the StrategyPerformanceReport class, and tell it what price to use for the fills
class FillType(Enum):
    NextBarOpen = 1,
    SameBarClose = 2,
    SameBarOpen = 3,
    AdjustedClose = 4,
