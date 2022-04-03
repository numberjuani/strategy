import pandas as pd
import numpy as np
import yfinance as yf
from strategy.fills import FillType as fill
from strategy.positions import PositionType as pos,position_from_value
class StrategyPerformanceReport:

    def __init__(self,
                 symbol: str,
                 strategy_name: str,
                 strategy_data: pd.DataFrame,
                 signal_column_name: str,
                 trade_amount: int = 100,
                 entry_fill: fill = fill.NextBarOpen,
                 exit_fill: fill = fill.NextBarOpen,
                 point_value: int = 1,
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

    def _get_trades_list(self):
        #we copy the data to prevent getting the pandas error "SettingWithCopyWarning"
        self.strategy_data = self.strategy_data.copy()
        #we start analysis in the user provided index, given that some strategies need to start at a specific index
        self.strategy_data = self.strategy_data.iloc[self.start_at_index:]
        #make all the strategy data columns lower case in case input is upper case or mixed case
        self.strategy_data.columns = [
            x.lower() for x in self.strategy_data.columns
        ]
        #make sure the signal column is a numeric column since its multiplied by the price difference
        if self.strategy_data[self.signal_column_name].dtype != 'float64':
            self.strategy_data[self.signal_column_name] = self.strategy_data[
                self.signal_column_name].astype('float')
        #if the strategy does not contain a datetime column, we create it for we need it to calculate trade durations with timedelta
        if 'datetime' not in self.strategy_data.columns:
            #combine date and time columns
            if 'time' in self.strategy_data.columns:
                self.strategy_data[
                    'datetime'] = self.strategy_data['date'].map(
                        str) + ' ' + self.strategy_data['time'].map(str)
            else:
                self.strategy_data['datetime'] = self.strategy_data[
                    'date'].map(str) + ' 00:00:00'
            self.strategy_data['datetime'] = pd.to_datetime(
                self.strategy_data['datetime'])
        # this multiplier will be used in the pnl for every trade, and its the point value (helpful for futures) times the quantity of the trade
        multiplier = self.point_value * self.trade_amount
        costs = (2 * (self.commission_per_trade + self.slippage))
        #calculate relevant values for the simulated entry fill
        match self.entry_fill:
            case fill.NextBarOpen:
                self.strategy_data['next_bar_open'] = self.strategy_data['open'].shift(-1)
                self.strategy_data['next_bar_datetime'] = self.strategy_data['datetime'].shift(-1)
                entry_fill_price = 'next_bar_open'
                entry_fill_date = 'next_bar_datetime'
                entry_index_adjustment = 1
            case fill.SameBarClose:
                entry_fill_price = 'close'
                entry_fill_date = 'datetime'
                entry_index_adjustment = 0 
                entry_fill_price = 'close'
            case fill.SameBarOpen:
                entry_fill_price = 'open'
                entry_fill_date = 'datetime'
                entry_index_adjustment = 0 
            case fill.AdjustedClose:
                entry_fill_price = 'adjusted_close'
                entry_fill_date = 'datetime'
                entry_index_adjustment = 0
        #calculate relevant values for the simulated exit fill
        match self.exit_fill:
            case fill.NextBarOpen:
                if 'next_bar_open' not in self.strategy_data.columns:
                    self.strategy_data['next_bar_open'] = self.strategy_data['open'].shift(-1)
                self.strategy_data['next_bar_datetime'] = self.strategy_data['datetime'].shift(-1)
                exit_fill_price = 'next_bar_open'
                exit_fill_date = 'next_bar_datetime'
                exit_index_adjustment = 1
            case fill.SameBarClose:
                exit_fill_price = 'close'
                exit_fill_date = 'datetime'
                exit_index_adjustment = 0
            case fill.SameBarOpen:
                exit_fill_price = 'open'
                exit_fill_date = 'datetime'
                exit_index_adjustment = 0
            case fill.AdjustedClose:
                exit_fill_price = 'adjusted_close'
                exit_fill_date = 'datetime'
                exit_index_adjustment = 0
        current_position = 0
        trades_list = []
        unrealized_pnls = []
        entry_date = None
        entry_index = None
        for i in range(len(self.strategy_data)):
            new_position = position_from_value(self.strategy_data.iloc[i][self.signal_column_name])
            unrealized_pnl = 0
            if entry_index:
                trade_period = self.strategy_data.iloc[entry_index:i+exit_index_adjustment, :]
                max_high = trade_period['high'].max()
                min_low = trade_period['low'].min()
                # in this match statement we calculate open trade stats
                match current_position:
                    case pos.Long:
                        max_adverse_excursion = multiplier*(entry_price - min_low)
                        max_favorable_excursion = multiplier*(max_high - entry_price)
                        diff = self.strategy_data.iloc[i][exit_fill_price] - entry_price
                        unrealized_pnl = diff /entry_price
                        pnl = multiplier*diff - costs
                    case pos.Short:
                        max_adverse_excursion = multiplier*(max_high - entry_price)
                        max_favorable_excursion = multiplier*(entry_price - min_low)
                        diff = entry_price - self.strategy_data.iloc[i][exit_fill_price]
                        unrealized_pnl = diff /entry_price
                        pnl = multiplier*diff - costs
                    case pos.Flat:
                        max_adverse_excursion = 0
                        max_favorable_excursion = 0
            
            unrealized_pnls.append({'date':self.strategy_data.iloc[i]['datetime'],'pnl':unrealized_pnl})    
            if new_position != current_position:
                if entry_index:
                    entry_price = self.strategy_data.iloc[i][entry_fill_price]
                    trade.update({
                        'exit_date': self.strategy_data.iloc[i][exit_fill_date],
                        'exit_price': self.strategy_data.iloc[i][exit_fill_price],
                        'trade_duration': self.strategy_data.iloc[i][exit_fill_date] - entry_date,
                        'max_favorable_excursion': max_favorable_excursion,
                        'max_adverse_excursion': -max_adverse_excursion,
                        'mfemae_ratio': safe_division(max_favorable_excursion,max_adverse_excursion),
                        'commissions': 2 * self.commission_per_trade,
                        'slippage': 2 * self.slippage,
                        'pnl':pnl
                    }),
                    trades_list.append(trade)
                    entry_date = None
                    del trade
                if new_position != 0:
                    entry_index = i + entry_index_adjustment
                    current_position = new_position
                    entry_price = self.strategy_data.iloc[i][entry_fill_price]
                    entry_date = self.strategy_data.iloc[i][entry_fill_date]
                    trade = {
                        'position': current_position,
                        'entry_date': self.strategy_data.iloc[i][entry_fill_date],
                        'entry_price': entry_price
                    }
        frame = pd.DataFrame(trades_list)
        frame.index.name = 'Trade Number'
        self.raw_trade_list = frame
        upl_frame = pd.DataFrame(unrealized_pnls)
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
        analytics['percent_profitable'] = 100 * \
            len(trades_list.loc[trades_list.pnl > 0]
                )/analytics['total_trades']
        analytics['winning_trades'] = len(trades_list.loc[trades_list.pnl > 0])
        analytics['losing_trades'] = len(trades_list.loc[trades_list.pnl <= 0])
        analytics['avg_trade_net_profit'] = trades_list.pnl.mean()
        analytics['avg_win_trade_pnl'] = trades_list.loc[
            trades_list.pnl > 0].pnl.mean()
        analytics['avg_lose_trade_pnl'] = trades_list.loc[
            trades_list.pnl <= 0].pnl.mean()
        analytics['ratio_avg_win_loss'] = analytics['avg_win_trade_pnl']/- \
            analytics['avg_lose_trade_pnl']
        analytics['max_win_trade_pnl'] = trades_list.loc[
            trades_list.pnl > 0].pnl.max()
        analytics['max_lose_trade_pnl'] = trades_list.loc[
            trades_list.pnl <= 0].pnl.min()
        analytics['average_trade_duration'] = trades_list.trade_duration.mean(
        ).round('1min')
        analytics['avg mfe/mae'] = trades_list.mfemae_ratio.mean()
        analytics[
            'average_favorable_excursion'] = trades_list.max_favorable_excursion.mean(
            )
        analytics[
            'average_adverse_excursion'] = trades_list.max_adverse_excursion.mean(
            )
        perfect_profit_slope = (analytics['total_net_profit']) / (
            len(trades_list))
        perfect_profit_line = pd.Series([
            self.initial_account_balance + perfect_profit_slope * x
            for x in trades_list.index
        ])
        trades_list['perfect_profit_line'] = perfect_profit_line
        analytics['perfect_profit_correlation'] = 100 * \
            trades_list.strategy_equity.corr(perfect_profit_line)
        analytics['max_drawdown'] = -trades_list.drawdown.min()
        #resample the unrealized pnl to daily
        daily_unrealized_returns:pd.DataFrame = self.unrealized.pnl.resample('D').sum()
        daily_unrealized_returns.fillna(0, inplace=True)
        analytics['annualized_sharpe_ratio'] = (np.mean(daily_unrealized_returns) - self.risk_free_ror)/ (np.std(daily_unrealized_returns) * np.sqrt(252))
        analytics['annualized_risk_free_ror'] = self.risk_free_ror
        analytics['annualized_strategy_ror'] = (
            trades_list.iloc[-1]['strategy_returns'] / number_of_years)
        analytics['annualized_volatility'] = np.std(daily_unrealized_returns) * np.sqrt(252)
        analytics['total_commission_paid'] = trades_list.commissions.sum()
        analytics['total_slippage_paid'] = trades_list.slippage.sum()
        analytics['total_costs'] = analytics['total_commission_paid'] + \
            analytics['total_slippage_paid']
        #round all the analytics values to 2 decimal places
        for key, value in analytics.items():
            if type(value) == float:
                analytics[key] = round(value, 2)
        #round all the values in the trades list to 2 decimal places
        trades_list = trades_list.round(decimals=2)
        return (analytics, trades_list)

    def _get_analytics(self):
        self._get_trades_list()
        ticker_yahoo = yf.Ticker('^IRX')
        data = ticker_yahoo.history()
        #the rate is for 13 weeks, so we divide it by the number of days and then divide by 100 so its in ratio form like our unrealized pnl list
        self.risk_free_ror = ((data['Close'].iloc[-1]/(13*5)))/100
        short_analytics, short_trades = self._get_trade_collection_analytics(self.raw_trade_list.loc[self.raw_trade_list.position == pos.Short])
        long_analytics, long_trades = self._get_trade_collection_analytics(self.raw_trade_list.loc[self.raw_trade_list.position == pos.Long])
        all_analytics, all_trades = self._get_trade_collection_analytics(self.raw_trade_list)
        df = pd.DataFrame([all_analytics, long_analytics, short_analytics],index=['All Trades', 'Long Trades', 'Short Trades'])
        self.performance_report = df.transpose()
        self.long_performance_report = long_analytics
        self.short_performance_report = short_analytics
        self.all_trades = all_trades
        self.short_trades = short_trades
        self.long_trade_trades = long_trades

    def run_backtest(self):
        self._get_analytics()
        #map the position of the trades to be long or short
        self.all_trades['position'] = self.all_trades.position.apply(lambda x: x.name())
        return (self.performance_report, self.all_trades)

    def to_excel(self):
        #create filename with strategy name, symbol, and dates
        filename = self.strategy_name + '_' + self.symbol + '_' + str(
            self.performance_report['All Trades']['start_date']) + '_' + str(
                self.performance_report['All Trades']['end_date']) + '.xlsx'
        with pd.ExcelWriter(filename, mode='w') as writer:
            self.performance_report.to_excel(writer, 'Performance Report')
            self.all_trades.to_excel(writer, 'Trade List')
            writer.save()


def safe_division(dividend:float, divisor:float)->float:
    if divisor == 0:
        return 0
    else:
        return dividend / divisor