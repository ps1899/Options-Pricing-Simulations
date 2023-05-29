from enum import Enum

class OptionPricingMethod(Enum):
    blackScholes = 'Black Scholes Model'
    monteCarlo = 'Monte Carlo Simulation'
    binomialTree = 'Binomial Tree Model'
