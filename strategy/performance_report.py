from dataclasses import dataclass
import pandas as pd
import numpy as np
from strategy.fills import FillType as fill
from strategy.positions import PositionType as pos, position_from_value, Position


@dataclass
class StrategyPerformanceReport:
    symbol: str
    strategy_name: str
    strategy_data: pd.DataFrame
    signal_column_name: str
    trade_amount: float
    entry_fill: fill
    exit_fill: fill
    initial_account_balance: float
    point_value: float
    commission_per_trade: float
    slippage: float
    start_at_index: int
    multiplier: float

    def __init__(self,
                 symbol: str,
                 strategy_name: str,
                 strategy_data: pd.DataFrame,
                 signal_column_name: str,
                 trade_amount: float = 100,
                 entry_fill: fill = fill.NextBarOpen,
                 exit_fill: fill = fill.NextBarOpen,
                 point_value: float = 1,
                 commission_per_trade: float = 0,
                 slippage: float = 0.0,
                 start_at_index=50,
                 intial_account_balance: float = 100000):
        self.symbol = symbol
        self.strategy_name = strategy_name
        self.strategy_data = strategy_data
        self.signal_column_name = signal_column_name.lower()
        self.trade_amount = trade_amount
        self.entry_fill = entry_fill
        self.exit_fill = exit_fill
        self.initial_account_balance = intial_account_balance
        self.point_value = point_value
        self.commission_per_trade = commission_per_trade
        self.slippage = slippage
        self.start_at_index = start_at_index
        self.multiplier = trade_amount * point_value

    def _get_trades_list(self):
        # we copy the data to prevent getting the pandas error "SettingWithCopyWarning"
        self.strategy_data = self.strategy_data.copy()
        self.strategy_data = self.strategy_data.reset_index()
        # we start analysis in the user provided index, given that some strategies need to start at a specific index
        self.strategy_data = self.strategy_data.iloc[self.start_at_index:]
        # make all the strategy data columns lower case in case input is upper case or mixed case
        self.strategy_data.columns = [
            x.lower() for x in self.strategy_data.columns
        ]
        # make sure the signal column is a numeric column since its multiplied by the price difference
        self.strategy_data[self.signal_column_name] = self.strategy_data[self.signal_column_name].astype('float')
        self.strategy_data['open'] = self.strategy_data['open'].astype('float')
        self.strategy_data['high'] = self.strategy_data['high'].astype('float')
        self.strategy_data['low'] = self.strategy_data['low'].astype('float')
        self.strategy_data['close'] = self.strategy_data['close'].astype('float')
        # if the strategy does not contain a datetime column, we create it for we need it to calculate trade durations with timedelta
        if 'datetime' not in self.strategy_data.columns:
            # combine date and time columns
            if 'time' in self.strategy_data.columns:
                self.strategy_data[
                    'datetime'] = self.strategy_data['date'].map(
                        str) + ' ' + self.strategy_data['time'].map(str)
            else:
                self.strategy_data['datetime'] = self.strategy_data[
                    'date'].map(str) + ' 00:00:00'
            self.strategy_data['datetime'] = pd.to_datetime(
                self.strategy_data['datetime'])
        if self.entry_fill == fill.NextBarOpen:
            self.strategy_data['next_bar_open'] = self.strategy_data['open'].shift(
                -1)
            self.strategy_data['next_bar_datetime'] = self.strategy_data['datetime'].shift(
                -1)
            entry_fill_price = 'next_bar_open'
            entry_fill_date = 'next_bar_datetime'
            entry_index_adjustment = 1
        elif self.entry_fill == fill.SameBarClose:
            entry_fill_price = 'close'
            entry_fill_date = 'datetime'
            entry_index_adjustment = 0
            entry_fill_price = 'close'
        elif self.entry_fill == fill.SameBarOpen:
            entry_fill_price = 'open'
            entry_fill_date = 'datetime'
            entry_index_adjustment = 0
        elif self.entry_fill == fill.AdjustedClose:
            entry_fill_price = 'adjusted_close'
            entry_fill_date = 'datetime'
            entry_index_adjustment = 0
        # calculate relevant values for the simulated exit fill
        if self.entry_fill == fill.NextBarOpen:
            if 'next_bar_open' not in self.strategy_data.columns:
                self.strategy_data['next_bar_open'] = self.strategy_data['open'].shift(
                    -1)
            self.strategy_data['next_bar_datetime'] = self.strategy_data['datetime'].shift(
                -1)
            exit_fill_price = 'next_bar_open'
            exit_fill_date = 'next_bar_datetime'
        elif self.entry_fill == fill.SameBarClose:
            exit_fill_price = 'close'
            exit_fill_date = 'datetime'
        elif self.entry_fill == fill.SameBarOpen:
            exit_fill_price = 'open'
            exit_fill_date = 'datetime'
        elif self.entry_fill == fill.AdjustedClose:
            exit_fill_price = 'adjusted_close'
            exit_fill_date = 'datetime'
        current_position = pos.Flat
        trades_list = []
        unrealized_pnls = []
        entry_index = None
        # check if index in self.strategy_data is datetime, if not, we convert it to datetime
        for i in range(len(self.strategy_data)):
            new_position_type = position_from_value(
                self.strategy_data.iloc[i][self.signal_column_name])
            unrealized_pnl = 0
            if not current_position.is_flat():
                open_trade.update(
                    float(self.strategy_data.iloc[i]['high']),float(self.strategy_data.iloc[i]['low']))
                unrealized_pnl = open_trade.open_pnl(
                    self.strategy_data.iloc[i][exit_fill_price])
            unrealized_pnls.append(
                {'date': self.strategy_data.iloc[i]['datetime'], 'pnl': unrealized_pnl})
            if new_position_type != current_position:
                # closing previous trade
                if entry_index:
                    open_trade.close(self.strategy_data.iloc[i][exit_fill_date], self.strategy_data.iloc[i]
                                     [exit_fill_price], self.commission_per_trade, self.slippage)
                    trades_list.append(open_trade)
                    entry_index = None
                # open new trades
                if not new_position_type.is_flat():
                    entry_index = i + entry_index_adjustment
                    current_position = new_position_type
                    open_trade = Position(self.trade_amount, self.strategy_data.iloc[i][entry_fill_date], self.strategy_data.iloc[i][
                                          entry_fill_price], new_position_type, self.commission_per_trade, self.symbol, self.slippage, self.point_value)
        frame = pd.DataFrame([x.__dict__ for x in trades_list])
        frame.index.name = 'Trade Number'
        self.raw_trade_list = frame
        upl_frame = pd.DataFrame(unrealized_pnls)
        if 'date' in upl_frame.columns:
            upl_frame.set_index('date', inplace=True)
        self.unrealized = upl_frame

    def _get_trade_collection_analytics(self, trades_list: pd.DataFrame):
        """Function to generate strategy analytics from a trades list"""
        trades_list = trades_list.copy()
        trades_list['strategy_equity'] = self.initial_account_balance + \
            trades_list.pnl.cumsum()
        trades_list['strategy_returns'] = (
            100 *
            (trades_list.strategy_equity / self.initial_account_balance)) - 100
        trades_list['high_watermark'] = trades_list['strategy_equity'].cummax()
        trades_list['drawdown'] = -(trades_list['high_watermark'] -
                                    trades_list['strategy_equity'])
        # replace NaN with 0 is strategy_return is NaN
        trades_list['strategy_returns'].fillna(0, inplace=True)
        analytics = {}
        analytics['start_date'] = trades_list.entry_date.min().date()
        analytics['end_date'] = trades_list.exit_date.max().date()
        analytics['trading_period_days'] = (analytics['end_date'] -
                                            analytics['start_date']).days
        number_of_years = (
            (analytics['end_date'] - analytics['start_date']).days) / 365
        analytics['trading_period_years'] = number_of_years
        analytics['total_net_profit'] = trades_list.pnl.sum()
        analytics['gross_profit'] = trades_list.loc[
            trades_list.pnl > 0].pnl.sum()
        analytics['gross_loss'] = trades_list.loc[
            trades_list.pnl < 0].pnl.sum()
        analytics['profit_factor'] = (analytics['gross_profit'] /
                                      -analytics['gross_loss'])
        analytics['total_trades'] = len(trades_list)
        analytics['percent_profitable'] = 100 * safe_division(
            len(trades_list.loc[trades_list.pnl > 0]), analytics['total_trades'])
        analytics['winning_trades'] = len(trades_list.loc[trades_list.pnl > 0])
        analytics['losing_trades'] = len(trades_list.loc[trades_list.pnl <= 0])
        analytics['avg_trade_net_profit'] = trades_list.pnl.mean()
        analytics['avg_win_trade_pnl'] = trades_list.loc[trades_list.pnl > 0].pnl.mean()
        analytics['avg_lose_trade_pnl'] = trades_list.loc[trades_list.pnl <= 0].pnl.mean()
        analytics['ratio_avg_win_loss'] = safe_division(
            analytics['avg_win_trade_pnl'], analytics['avg_lose_trade_pnl'])
        analytics['max_win_trade_pnl'] = trades_list.loc[
            trades_list.pnl > 0].pnl.max()
        analytics['max_lose_trade_pnl'] = trades_list.loc[
            trades_list.pnl <= 0].pnl.min()
        analytics['average_trade_duration'] = trades_list.trade_duration.mean(
        ).round('1min')
        analytics['average_favorable_excursion'] = trades_list.max_favorable_excursion.mean()
        analytics[
            'average_adverse_excursion'] = trades_list.max_adverse_excursion.mean(
        )
        analytics['avg mfe/mae'] = safe_division(
            analytics['average_favorable_excursion'], analytics['average_adverse_excursion'])
        perfect_profit_slope = safe_division(
            analytics['total_net_profit'], len(trades_list))
        perfect_profit_line = pd.Series([
            self.initial_account_balance + perfect_profit_slope * x
            for x in trades_list.index
        ])
        trades_list['perfect_profit_line'] = perfect_profit_line
        analytics['perfect_profit_correlation'] = 100 * \
            trades_list.strategy_equity.corr(perfect_profit_line)
        analytics['max_drawdown'] = -trades_list.drawdown.min()
        # resample the unrealized pnl to daily
        daily_unrealized_returns: pd.DataFrame = self.unrealized.pnl.resample(
            'D').sum()
        daily_unrealized_returns.fillna(0, inplace=True)
        analytics['annualized_sharpe_ratio'] = safe_division(np.mean(
            daily_unrealized_returns), (np.std(daily_unrealized_returns) * np.sqrt(252)))
        analytics['annualized_strategy_ror'] = safe_division(
            trades_list.iloc[-1]['strategy_returns'], number_of_years)
        analytics['annualized_volatility'] = np.std(
            daily_unrealized_returns) * np.sqrt(252)
        analytics['total_commission_paid'] = trades_list.total_commissions.sum()
        analytics['total_slippage_paid'] = trades_list.total_slippage.sum()
        analytics['total_costs'] = analytics['total_commission_paid'] + \
            analytics['total_slippage_paid']
        # round all the analytics values to 2 decimal places
        for key, value in analytics.items():
            if type(value) == float:
                analytics[key] = round(value, 2)
        # round all the values in the trades list to 2 decimal places
        trades_list = trades_list.round(decimals=2)
        return (analytics, trades_list)

    def _get_analytics(self):
        self._get_trades_list()
        if 'position_type' in self.raw_trade_list.columns:
            short_analytics, short_trades = self._get_trade_collection_analytics(
                self.raw_trade_list.loc[self.raw_trade_list.position_type == pos.Short])
            long_analytics, long_trades = self._get_trade_collection_analytics(
                self.raw_trade_list.loc[self.raw_trade_list.position_type == pos.Long])
            all_analytics, all_trades = self._get_trade_collection_analytics(
                self.raw_trade_list)
            df = pd.DataFrame([all_analytics, long_analytics, short_analytics], index=[
                              'All Trades', 'Long Trades', 'Short Trades'])
            self.performance_report = df.transpose()
            self.long_performance_report = long_analytics
            self.short_performance_report = short_analytics
            self.all_trades = all_trades
            self.short_trades = short_trades
            self.long_trade_trades = long_trades
        else:
            self.performance_report = None
            self.long_performance_report = None
            self.short_performance_report = None
            self.all_trades = None
            self.short_trades = None
            self.long_trade_trades = None

    def run_backtest(self):
        self._get_analytics()
        # map the position of the trades to be long or short
        if 'position_type' in self.raw_trade_list.columns:
            self.all_trades['position_type'] = self.all_trades.position_type.apply(
                lambda x: x.name())
        return (self.performance_report, self.all_trades)

    def to_excel(self):
        # create filename with strategy name, symbol, and dates
        filename = self.strategy_name + '_' + self.symbol + '_' + str(
            self.performance_report['All Trades']['start_date']) + '_' + str(
                self.performance_report['All Trades']['end_date']) + '.xlsx'
        with pd.ExcelWriter(filename, mode='w') as writer:
            self.performance_report.to_excel(writer, 'Performance Report')
            self.all_trades.to_excel(writer, 'Trade List')
            writer.save()


def safe_division(dividend: float, divisor: float) -> float:
    """Checks to make sure no divide by 0 error"""
    if divisor == 0:
        return 0
    else:
        return dividend / divisor
