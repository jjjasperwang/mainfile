import backtrader as bt
import yfinance as yf

# 策略逻辑（仅需10行核心代码）
class SimpleStrategy(bt.Strategy):
    params = (
        ('short_period', 5),
        ('long_period', 20)
    )

    def __init__(self):
        self.short_ma = bt.indicators.SMA(period=self.params.short_period)
        self.long_ma = bt.indicators.SMA(period=self.params.long_period)
        self.crossover = bt.indicators.CrossOver(self.short_ma, self.long_ma)

    def next(self):
        if not self.position:  # 无持仓时
            if self.crossover > 0:  # 短期均线上穿
                self.buy(size=100)  # 买入100股
        elif self.crossover < 0:  # 短期均线下穿
            self.close()  # 平仓

# 主程序（仅需5行代码）
cerebro = bt.Cerebro()
data = bt.feeds.PandasData(dataname=yf.download('AAPL', '2025-01-01', '2025-03-01'))
cerebro.adddata(data)
cerebro.addstrategy(SimpleStrategy)
cerebro.run()
cerebro.plot()