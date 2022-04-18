from enum import Enum
from dataclasses import dataclass
import datetime
from typing import Optional
import numpy as np


class PositionType(Enum):
    Long = 1,
    Short = -1,
    Flat = 0,

    def name(self):
        if self == PositionType.Long:
            return "Long"
        elif self == PositionType.Short:
            return "Short"
        elif self == PositionType.Flat:
            return "Flat"

    def is_flat(self):
        return self == PositionType.Flat


def position_from_value(value) -> PositionType:
    """Matches a position type from a value"""
    for position_type in PositionType:
        if position_type.value == value:
            return position_type
    raise ValueError('Invalid position type value: {}'.format(value))


@dataclass
class Position:
    symbol: str
    point_value: float
    position_type: PositionType
    amount: float
    entry_date: datetime.datetime
    entry_price: float
    entry_commission: float
    entry_slippage: float
    exit_date: Optional[datetime.datetime]
    exit_price: Optional[float]
    max_favorable_excursion: float
    max_adverse_excursion: float
    exit_commission: Optional[float]
    exit_slippage: Optional[float]
    pnl: float
    trade_duration: Optional[datetime.timedelta]
    multiplier: float
    total_commissions: float
    total_slippage:float

    def __init__(self, amount: int, entry_date: datetime.datetime, entry_price: float, position_type: PositionType, entry_commission: float,symbol: str, entry_slippage: float=0,  point_value: float=1):
        self.symbol = symbol
        self.amount = amount
        self.entry_date = entry_date
        self.entry_price = entry_price
        self.exit_date = None
        self.exit_price = None
        self.position_type = position_type
        self.max_favorable_excursion = 0
        self.max_adverse_excursion = 0
        self.entry_commission = entry_commission
        self.entry_slippage = entry_slippage
        self.point_value = point_value
        self.multiplier = self.amount * self.point_value
        self.pnl = 0

    def update(self, high: float, low: float):
        if self.position_type == PositionType.Long:
            current_favorable_excursion = (self.multiplier*(high - self.entry_price))
            mfe = max(self.max_favorable_excursion, current_favorable_excursion)
            self.max_favorable_excursion = mfe
            current_adverse_excursion = (self.multiplier*(self.entry_price - low))
            mae = max(self.max_adverse_excursion, current_adverse_excursion)
            self.max_adverse_excursion = mae
        elif self.position_type == PositionType.Short:
            current_favorable_excursion = (self.multiplier*(self.entry_price - low))
            current_adverse_excursion = (self.multiplier*(high - self.entry_price))
            mfe = max(self.max_favorable_excursion, current_favorable_excursion)
            mae = max(self.max_adverse_excursion, current_adverse_excursion)
            self.max_favorable_excursion = mfe
            self.max_adverse_excursion = mae
        else:
            self.max_favorable_excursion = 0
            self.max_adverse_excursion = 0

    def open_pnl(self, price: float) -> float:
        if self.position_type == PositionType.Long:
            pnl = ((price - self.entry_price) * self.multiplier)
            self.pnl = pnl
            return pnl
        elif self.position_type == PositionType.Short:
            pnl = ((self.entry_price - price) * self.multiplier)
            self.pnl = pnl
            return pnl
        else:
            return 0

    def is_open(self):
        return (self.exit_date is None) & (self.exit_price is None)

    def close(self, exit_date: datetime.datetime, exit_price: float, exit_commission: float, exit_slippage: float,):
        self.exit_date = exit_date
        self.exit_price = exit_price
        self.exit_commission = exit_commission
        self.exit_slippage = exit_slippage
        self.trade_duration = self.exit_date - self.entry_date
        total_commissions = self.entry_commission + self.exit_commission
        total_slippage = self.entry_slippage + self.exit_slippage
        self.pnl = self.open_pnl(exit_price) - \
            (total_commissions + total_slippage)
        self.total_commissions = total_commissions
        self.total_slippage = total_slippage

        
        
        
        