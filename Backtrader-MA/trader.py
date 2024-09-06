import datetime  
import backtrader as bt
from strategies import *

cerebro = bt.Cerebro()

# Create a Data Feed
data = bt.feeds.YahooFinanceCSVData(
    dataname='orcl.csv',
    fromdate=datetime.datetime(1995, 1, 3),
    todate=datetime.datetime(1999, 1,20),
    reverse=False)

# Add the Data Feed to Cerebro
cerebro.adddata(data)

# Set our desired cash start
cerebro.broker.setcash(1000)

# Add a strategy
cerebro.addstrategy(CrossoverMA)
# cerebro.addstrategy(BuyAndHold)

print('Start Portfolio Value: %.2f' % cerebro.broker.getvalue()) # the value is the cash (liquidity) + the invested value

cerebro.run()

# Print out the final result
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

# cerebro.plot() # Plot the results
# python trader.py > out.txt  