# Strategy Trading
An Algo trading backtesting library.
To install:
```
pip3 install git+https://github.com/numberjuani/strategy.git
```
To use:
Create a pandas dataframe with your trading signals in each row. These must be 1 for long, -1 for short, 0 for hold.
Once you have that, do this:
```
from strategy.performance_report import StrategyPerformanceReport
backtest = StrategyPerformanceReport('SPY','demo_strategy',df,'Signal')
performance_report,trades = backtest.get_backtest()
```
<h1>Performance Reports</h2>
|                           |All Trades         |Long Trades        |Short Trades         |
|---------------------------|-------------------|-------------------|---------------------|
|start_date                 |2017-06-06         |2017-07-20         |2017-06-06           |
|end_date                   |2022-02-08         |2022-01-11         |2022-02-08           |
|trading_period_days        |1708               |1636               |1708                 |
|trading_period_years       |4.67945205479452   |4.482191780821918  |4.67945205479452     |
|total_net_profit           |6719.000000000008  |6233.0000000000055 |486.000000000004     |
|gross_profit               |22738.000000000004 |14271.000000000002 |8467.000000000004    |
|gross_loss                 |-16018.999999999995|-8037.999999999995 |-7980.999999999998   |
|profit_factor              |1.4194394156938643 |1.775441652152278  |1.0608946247337434   |
|total_trades               |91                 |45                 |46                   |
|percent_profitable         |29.67032967032967  |28.88888888888889  |30.434782608695652   |
|winning_trades             |27                 |13                 |14                   |
|losing_trades              |64                 |32                 |32                   |
|avg_trade_net_profit       |73.83516483516493  |138.51111111111123 |10.565217391304435   |
|avg_win_trade_pnl          |842.1481481481483  |1097.769230769231  |604.7857142857146    |
|avg_lose_trade_pnl         |-250.29687499999991|-251.18749999999986|-249.40624999999994  |
|ratio_avg_win_loss         |3.364597133496567  |4.370317912990223  |2.4249019993914134   |
|max_win_trade_pnl          |3809.0000000000005 |3809.0000000000005 |1797.0               |
|max_lose_trade_pnl         |-953.0000000000001 |-953.0000000000001 |-712.9999999999995   |
|average_trade_duration     |18 days 18:28:00   |21 days 02:08:00   |16 days 12:00:00     |
|avg mfe/mae                |-1.4760575792507435|5.805316889950003  |-8.599141299121039   |
|average_favorable_excursion|499.2637362637362  |520.1333333333333  |478.84782608695645   |
|average_adverse_excursion  |-339.53846153846155|-407.3777777777777 |-273.17391304347836  |
|perfect_profit_correlation |47.113805244082855 |39.19153595367113  |45.92621312184276    |
|max_drawdown               |4652.0             |2620.0             |2832.0               |
|annualized_sharpe_ratio    |0.3369222136547682 |0.4099999066550984 |-0.029656852937467643|
|strategy_return            |6.719000000000008  |6.233000000000004  |0.4860000000000042   |
|annualized_return          |1.4358518735363015 |1.390614303178485  |0.10385831381733111  |
|annualized_volatility      |1.6                |1.23               |0.9                  |
|total_commission_paid      |0                  |0                  |0                    |
|total_slippage_paid        |0.0                |0.0                |0.0                  |
|total_costs                |0.0                |0.0                |0.0                  |
<h1>Trades List</h2>
|Trade Number|position|entry_date         |entry_price|exit_date          |exit_price|trade_duration|max_favorable_excursion|max_adverse_excursion|mfemae_ratio       |commissions|slippage|pnl                |strategy_equity|strategy_returns  |high_watermark|drawdown|perfect_profit_line|
|------------|--------|-------------------|-----------|-------------------|----------|--------------|-----------------------|---------------------|-------------------|-----------|--------|-------------------|---------------|------------------|--------------|--------|-------------------|
|0           |short   |2017-06-06 14:00:00|78.61      |2017-07-20 14:00:00|70.6      |44 days       |496.9999999999999      |-801.0000000000005   |0.6204744069912604 |0          |0.0     |801.0000000000005  |100801.0       |0.8010000000000019|100801.0      |-0.0    |100000.0           |
|1           |long    |2017-07-20 14:00:00|70.6       |2017-07-25 14:00:00|69.38     |5 days        |198.0000000000004      |-71.99999999999989   |2.7500000000000098 |0          |0.0     |-121.99999999999989|100679.0       |0.679000000000002 |100801.0      |-122.0  |100073.83516483517 |
|2           |short   |2017-07-25 14:00:00|69.38      |2017-07-26 14:00:00|70.3      |1 days        |112.99999999999955     |-71.99999999999989   |1.5694444444444406 |0          |0.0     |-92.00000000000017 |100587.0       |0.5870000000000033|100801.0      |-214.0  |100147.67032967033 |
|3           |long    |2017-07-26 14:00:00|70.3       |2018-02-05 14:00:00|108.39    |194 days      |826.0000000000005      |-3884.9999999999995  |0.21261261261261274|0          |0.0     |3809.0000000000005 |104396.0       |4.396000000000001 |104396.0      |-0.0    |100221.5054945055  |
|4           |short   |2018-02-05 14:00:00|108.39     |2018-04-05 14:00:00|97.94     |59 days       |1109.0000000000005     |-1250.0              |0.8872000000000003 |0          |0.0     |1045.0000000000002 |105441.0       |5.4410000000000025|105441.0      |-0.0    |100295.34065934065 |
