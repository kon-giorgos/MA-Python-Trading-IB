import backtrader as bt
import math

# Moving average crossover strategy
class CrossoverMA(bt.Strategy):
    params = (('pfast',10),('pslow',30),) 

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders
        self.order = None
        self.slow_sma = bt.indicators.MovingAverageSimple(self.datas[0], 
                        period=self.params.pslow)
        self.fast_sma = bt.indicators.MovingAverageSimple(self.datas[0], 
                        period=self.params.pfast)
        self.crossover = bt.indicators.CrossOver(self.fast_sma, self.slow_sma)
        self.size=self.broker.getcash()/self.dataclose

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, %.2f' % order.executed.price)
            elif order.issell():
                self.log('SELL EXECUTED, %.2f' % order.executed.price)

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def next(self):
        size=int(self.broker.get_cash()/self.dataclose[0]*0.9)
        self.log('Close, %.2f' % self.dataclose[0])

        if self.order: # Check if an order is pending . If yes, we cannot send a 2nd one
            return

        # Check if we are in the market. We can only go long, so if a position exists, then we have an asset to sell.
        if not self.position: # self.position does not exist, we can create a position. (buy an asset)

            if self.crossover>0:
            # if self.dataclose[0]>self.dataclose[-1]:

                        self.log('BUY CREATE, %.2f' % self.dataclose[0])
                        self.ex_order=size
                        self.order = self.buy(size=size)

        else: # self position exists. we have an asset to sell.

            if self.crossover<0:
            # if self.dataclose[0]<self.dataclose[-1]:

                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                self.order = self.sell(size=self.ex_order)

# Simple buy and hold strategy
class BuyAndHold(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):

        self.dataclose = self.datas[0].close

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, %.2f' % order.executed.price)
            elif order.issell():
                self.log('SELL EXECUTED, %.2f' % order.executed.price)

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def next(self):
        # Buy all the available cash
        
        size = int(self.broker.get_cash() / math.ceil(self.dataclose[0]))
        self.buy(size=size)



