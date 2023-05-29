import numpy as np
from scipy.stats import norm
from .Base import OptionPricingModel

class Black_Scholes_Pricing(OptionPricingModel):
    def __init__(self, underlyingSpotPrice, strikePrice, daysToMature, riskFreeRate, sigma, timeSteps):
        self.S = underlyingSpotPrice
        self.K = strikePrice
        self.T = daysToMature/365
        self.r = riskFreeRate
        self.sigma = sigma
        self.timeSteps = timeSteps

    def calculate_call_option_price(self):
        d1 = (np.log(self.S/self.K) + (self.r + 0.5 * self.sigma ** 2) * self.T)/(self.sigma * np.sqrt(self.T))
        d2 = d1 - (self.sigma * np.sqrt(self.T))
        # in norm.cdf() --> loc = 0.0 which is mean of distribution, scale = 1.0 which is std deviation of distribution
        calculateCallPrice = self.S * norm.cdf(d1, 0.0, 1.0) - self.K * np.exp(-self.r * self.T) * norm.cdf(d2, 0.0, 1.0)
        return calculateCallPrice
    
    def calculate_put_option_price(self):
        d1 = (np.log(self.S/self.K) + (self.r + 0.5 * self.sigma ** 2) * self.T)/(self.sigma * np.sqrt(self.T))
        d2 = d1 - (self.sigma * np.sqrt(self.T))
        calculatePutPrice =  self.K * np.exp(-self.r * self.T) * norm.cdf(-d2, 0.0, 1.0) - self.S * norm.cdf(-d1, 0.0, 1.0)
        return calculatePutPrice