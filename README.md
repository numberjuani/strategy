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
<table class="table table-bordered table-hover table-condensed">
<thead><tr><th title="Field #1"></th>
<th title="Field #2">All Trades</th>
<th title="Field #3">Long Trades</th>
<th title="Field #4">Short Trades</th>
</tr></thead>
<tbody><tr>
<td>start_date</td>
<td>2017-06-06</td>
<td>2017-07-20</td>
<td>2017-06-06</td>
</tr>
<tr>
<td>end_date</td>
<td>2022-02-08</td>
<td>2022-01-11</td>
<td>2022-02-08</td>
</tr>
<tr>
<td>trading_period_days</td>
<td>1708</td>
<td>1636</td>
<td>1708</td>
</tr>
<tr>
<td>trading_period_years</td>
<td>4.67945205479452</td>
<td>4.482191780821918</td>
<td>4.67945205479452</td>
</tr>
<tr>
<td>total_net_profit</td>
<td>6719.000000000008</td>
<td>6233.0000000000055</td>
<td>486.000000000004</td>
</tr>
<tr>
<td>gross_profit</td>
<td>22738.000000000004</td>
<td>14271.000000000002</td>
<td>8467.000000000004</td>
</tr>
<tr>
<td>gross_loss</td>
<td>-16018.999999999995</td>
<td>-8037.999999999995</td>
<td>-7980.999999999998</td>
</tr>
<tr>
<td>profit_factor</td>
<td>1.4194394156938643</td>
<td>1.775441652152278</td>
<td>1.0608946247337434</td>
</tr>
<tr>
<td>total_trades</td>
<td>91</td>
<td>45</td>
<td>46</td>
</tr>
<tr>
<td>percent_profitable</td>
<td>29.67032967032967</td>
<td>28.88888888888889</td>
<td>30.434782608695652</td>
</tr>
<tr>
<td>winning_trades</td>
<td>27</td>
<td>13</td>
<td>14</td>
</tr>
<tr>
<td>losing_trades</td>
<td>64</td>
<td>32</td>
<td>32</td>
</tr>
<tr>
<td>avg_trade_net_profit</td>
<td>73.83516483516493</td>
<td>138.51111111111123</td>
<td>10.565217391304435</td>
</tr>
<tr>
<td>avg_win_trade_pnl</td>
<td>842.1481481481483</td>
<td>1097.769230769231</td>
<td>604.7857142857146</td>
</tr>
<tr>
<td>avg_lose_trade_pnl</td>
<td>-250.29687499999991</td>
<td>-251.18749999999986</td>
<td>-249.40624999999994</td>
</tr>
<tr>
<td>ratio_avg_win_loss</td>
<td>3.364597133496567</td>
<td>4.370317912990223</td>
<td>2.4249019993914134</td>
</tr>
<tr>
<td>max_win_trade_pnl</td>
<td>3809.0000000000005</td>
<td>3809.0000000000005</td>
<td>1797.0</td>
</tr>
<tr>
<td>max_lose_trade_pnl</td>
<td>-953.0000000000001</td>
<td>-953.0000000000001</td>
<td>-712.9999999999995</td>
</tr>
<tr>
<td>average_trade_duration</td>
<td>18 days 18:28:00</td>
<td>21 days 02:08:00</td>
<td>16 days 12:00:00</td>
</tr>
<tr>
<td>avg mfe/mae</td>
<td>-1.4760575792507435</td>
<td>5.805316889950003</td>
<td>-8.599141299121039</td>
</tr>
<tr>
<td>average_favorable_excursion</td>
<td>499.2637362637362</td>
<td>520.1333333333333</td>
<td>478.84782608695645</td>
</tr>
<tr>
<td>average_adverse_excursion</td>
<td>-339.53846153846155</td>
<td>-407.3777777777777</td>
<td>-273.17391304347836</td>
</tr>
<tr>
<td>perfect_profit_correlation</td>
<td>47.113805244082855</td>
<td>39.19153595367113</td>
<td>45.92621312184276</td>
</tr>
<tr>
<td>max_drawdown</td>
<td>4652.0</td>
<td>2620.0</td>
<td>2832.0</td>
</tr>
<tr>
<td>annualized_sharpe_ratio</td>
<td>0.3369222136547682</td>
<td>0.4099999066550984</td>
<td>-0.029656852937467643</td>
</tr>
<tr>
<td>strategy_return</td>
<td>6.719000000000008</td>
<td>6.233000000000004</td>
<td>0.4860000000000042</td>
</tr>
<tr>
<td>annualized_return</td>
<td>1.4358518735363015</td>
<td>1.390614303178485</td>
<td>0.10385831381733111</td>
</tr>
<tr>
<td>annualized_volatility</td>
<td>1.6</td>
<td>1.23</td>
<td>0.9</td>
</tr>
<tr>
<td>total_commission_paid</td>
<td>0</td>
<td>0</td>
<td>0</td>
</tr>
<tr>
<td>total_slippage_paid</td>
<td>0.0</td>
<td>0.0</td>
<td>0.0</td>
</tr>
<tr>
<td>total_costs</td>
<td>0.0</td>
<td>0.0</td>
<td>0.0</td>
</tr>
</tbody></table>
<h1>Trades List</h2>
<table class="table table-bordered table-hover table-condensed">
<thead><tr><th title="Field #1">Trade Number</th>
<th title="Field #2">position</th>
<th title="Field #3">entry_date</th>
<th title="Field #4">entry_price</th>
<th title="Field #5">exit_date</th>
<th title="Field #6">exit_price</th>
<th title="Field #7">trade_duration</th>
<th title="Field #8">max_favorable_excursion</th>
<th title="Field #9">max_adverse_excursion</th>
<th title="Field #10">mfemae_ratio</th>
<th title="Field #11">commissions</th>
<th title="Field #12">slippage</th>
<th title="Field #13">pnl</th>
<th title="Field #14">strategy_equity</th>
<th title="Field #15">strategy_returns</th>
<th title="Field #16">high_watermark</th>
<th title="Field #17">drawdown</th>
<th title="Field #18">perfect_profit_line</th>
</tr></thead>
<tbody><tr>
<td align="right">0</td>
<td>short</td>
<td>2017-06-06 14:00:00</td>
<td align="right">78.61</td>
<td>2017-07-20 14:00:00</td>
<td align="right">70.6</td>
<td>44 days</td>
<td>496.9999999999999</td>
<td>-801.0000000000005</td>
<td>0.6204744069912604</td>
<td>0</td>
<td align="right">0.0</td>
<td>801.0000000000005</td>
<td align="right">100801.0</td>
<td>0.8010000000000019</td>
<td align="right">100801.0</td>
<td align="right">-0.0</td>
<td>100000.0</td>
</tr>
<tr>
<td align="right">1</td>
<td>long</td>
<td>2017-07-20 14:00:00</td>
<td align="right">70.6</td>
<td>2017-07-25 14:00:00</td>
<td align="right">69.38</td>
<td>5 days</td>
<td>198.0000000000004</td>
<td>-71.99999999999989</td>
<td>2.7500000000000098</td>
<td>0</td>
<td align="right">0.0</td>
<td>-121.99999999999989</td>
<td align="right">100679.0</td>
<td>0.679000000000002</td>
<td align="right">100801.0</td>
<td align="right">-122.0</td>
<td>100073.83516483517</td>
</tr>
<tr>
<td align="right">2</td>
<td>short</td>
<td>2017-07-25 14:00:00</td>
<td align="right">69.38</td>
<td>2017-07-26 14:00:00</td>
<td align="right">70.3</td>
<td>1 days</td>
<td>112.99999999999955</td>
<td>-71.99999999999989</td>
<td>1.5694444444444406</td>
<td>0</td>
<td align="right">0.0</td>
<td>-92.00000000000017</td>
<td align="right">100587.0</td>
<td>0.5870000000000033</td>
<td align="right">100801.0</td>
<td align="right">-214.0</td>
<td>100147.67032967033</td>
</tr>
<tr>
<td align="right">3</td>
<td>long</td>
<td>2017-07-26 14:00:00</td>
<td align="right">70.3</td>
<td>2018-02-05 14:00:00</td>
<td align="right">108.39</td>
<td>194 days</td>
<td>826.0000000000005</td>
<td>-3884.9999999999995</td>
<td>0.21261261261261274</td>
<td>0</td>
<td align="right">0.0</td>
<td>3809.0000000000005</td>
<td align="right">104396.0</td>
<td>4.396000000000001</td>
<td align="right">104396.0</td>
<td align="right">-0.0</td>
<td>100221.5054945055</td>
</tr>
<tr>
<td align="right">4</td>
<td>short</td>
<td>2018-02-05 14:00:00</td>
<td align="right">108.39</td>
<td>2018-04-05 14:00:00</td>
<td align="right">97.94</td>
<td>59 days</td>
<td>1109.0000000000005</td>
<td>-1250.0</td>
<td>0.8872000000000003</td>
<td>0</td>
<td align="right">0.0</td>
<td>1045.0000000000002</td>
<td align="right">105441.0</td>
<td>5.4410000000000025</td>
<td align="right">105441.0</td>
<td align="right">-0.0</td>
<td>100295.34065934065</td>
</tr>
</tbody></table>
