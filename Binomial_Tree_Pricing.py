import numpy as np
from scipy.stats import norm
from .Base import OptionPricingModel

class Binomial_Tree_Pricing(OptionPricingModel):
    def __init__(self, underlyingSpotPrice, strikePrice, daysToMature, riskFreeRate, sigma, timeSteps) -> None:
        self.S = underlyingSpotPrice
        self.K = strikePrice
        self.T = daysToMature/365
        self.r = riskFreeRate
        self.sigma = sigma
        self.timeSteps = timeSteps

    def calculate_call_option_price(self):
        dT = self.T/self.timeSteps
        u = np.exp(self.sigma * np.sqrt(dT))
        d = 1.0/u

        V = np.zeros(self.timeSteps + 1)

        sT = np.array([(self.S * u**j * d**(self.timeSteps - j)) for j in range(self.timeSteps + 1)])

        a = np.exp(self.r * dT)
        p = (a - d)/(u - d)
        q = 1.0 - p

        V[:] = np.maximum(sT - self.k, 0.0)

        for i in range(self.timeSteps - 1, -1, -1):
            V[:-1] = np.exp(-self.r * dT) * (p * V[1:] + q * V[:-1])
        return V[0]
    
    def calculate_put_option_price(self):
        dT = self.T/self.timeSteps
        u = np.exp(self.sigma * np.sqrt(dT))
        d = 1.0/u

        V = np.zeros(self.timeSteps + 1)

        sT = np.array([(self.S * u**j * d**(self.timeSteps - j)) for j in range(self.timeSteps + 1)])

        a = np.exp(self.r * dT)
        p = (a - d)/(u - d)
        q = 1.0 - p

        V[:] = np.maximum(self.k - sT, 0.0)

        for i in range(self.timeSteps - 1, -1, -1):
            V[:-1] = np.exp(-self.r * dT) * (p * V[1:] + q * V[:-1])
        return V[0]