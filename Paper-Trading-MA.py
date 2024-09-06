from ib_insync import *
import datetime
import time
# util.startLoop()  # uncomment this line when in a notebook

def crossover(a,b):
    if a.iloc[-1]>b.iloc[-1] and a.iloc[-2]<b.iloc[-2]:
        return 1
    elif a.iloc[-1]<b.iloc[-1] and a.iloc[-2]>b.iloc[-2]:
        return -1
    else: 
        return 0

# Connect to IBKR paper trading.
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)

# Create a contract to trade.
# contract=Contract(symbol='VWRP',exchange='SMART',currency='GBP',secType="STK")
contract=Forex('EURUSD')
print(ib.qualifyContracts(contract)) # Check whether the contract is valid/exists.

# LSE opens at 0900 and close at 1730 in simulation.
# That means the first and last prices occur within the specified timeframe.

b=datetime.datetime(    
    year=2024,
    month=1,
    day=1,
    hour=1,
    minute=1,
    second=1 )
bars = ib.reqHistoricalData(
    contract, endDateTime=b, durationStr='2 D',
    barSizeSetting='5 mins', whatToShow='MIDPOINT', useRTH=True)

# Convert to pandas dataframe (pandas needs to be installed):
df = util.df(bars)
close=df.close

# Define the fast and slow moving averages
n1=5
n2=20

# Calculate the matrices of the moving averages.
MA1=close.rolling(window=n1).mean()
MA2=close.rolling(window=n2).mean()

# Infinite loop that repeats at a defined time interval.
while True:
    print('runnng')
    if crossover(MA1,MA2)==1:
        print('Buy order placed')
        order=MarketOrder('BUY',1)
        ib.placeOrder(contract,order)
    elif crossover(MA1,MA2)==-1:
        print('Sell order placed')
        order=MarketOrder('SELL',1)
        ib.placeOrder(contract,order)
    time.sleep(5*60) # sec







