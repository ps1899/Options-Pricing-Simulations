from .Binomial_Tree_Pricing import Binomial_Tree_Pricing
from .Black_Scholes_Pricing import Black_Scholes_Pricing
from .Monte_Carlo_Pricing import Monte_Carlo_Pricing
from .Ticker import Ticker

data = Ticker.getHistoricalData('TSLA')
print(Ticker.getHistoricalData(data))
print(Ticker.getLastPrice(data, 'Adj Close'))
Ticker.plotData(data, 'TSLA', 'Adj Close')

BSM = Black_Scholes_Pricing(100, 100, 365, 0.1, 0.2)
print(BSM.calculate_option_price('Call Option'))
print(BSM.calculate_option_price('Put Option'))

BOPM = Binomial_Tree_Pricing(100, 100, 365, 0.1, 0.2, 15000)
print(BSM.calculate_option_price('Call Option'))
print(BSM.calculate_option_price('Put Option'))

MC = Monte_Carlo_Pricing(100, 100, 365, 0.1, 0.2, 10000)
MC.simulatePrices()
print(MC.calculate_option_price('Call Option'))
print(MC.calculate_option_price('Put Option'))
MC.plotSimulation(20)