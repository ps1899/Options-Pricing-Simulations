import numpy as np
from scipy.stats import norm
from .Base import OptionPricingModel
import matplotlib.pyplot as plt

class Monte_Carlo_Pricing(OptionPricingModel):
    def __init__(self, underlyingSpotPrice, strikePrice, daysToMature, riskFreeRate, sigma, noOfSimulations):
        self.S = underlyingSpotPrice
        self.K = strikePrice
        self.T = daysToMature/365
        self.r = riskFreeRate
        self.sigma = sigma
        self.N = noOfSimulations
        self.noOfSteps = daysToMature
        self.dT = self.T/self.noOfSteps

    def simulatePrices(self):
        np.randon.seed(20)
        self.simulationResults = None
        sim = np.zeros((self.noOfSteps, self.N))
        sim[0] = self.S
        for t in range(1, self.noOfSteps):
            Z = np.random.standard_normal(self.N)
            sim[t] = sim[t - 1] * np.exp((self.r - 0.5 * self.sigma ** 2) * self.dT + (self.sigma * np.sqrt(self.dT) * Z))
        self.simulationResults = sim

    def calculate_call_option_price(self):
        if(self.simulationResults is None):
            return -1
        return np.exp(-self.r * self.T) * (1/self.N) * np.sum(np.maximum(self.simulationResults[-1] - self.K, 0))
    
    def calculate_put_option_price(self):
        if(self.simulationResults is None):
            return -1
        return np.exp(-self.r * self.T) * (1/self.N) * np.sum(np.maximum(self.K - self.simulationResults[-1], 0))
    
    def plotSimulation(self, noOfMovements):
        plt.figure(figsize = (12, 8))
        plt.plot(self.simulationResults[:, 0:noOfMovements])
        plt.axhline(self.K, c = 'K', xmin = 0, xmax = self.noOfSteps, label = 'Strike Price')
        plt.xlim([0, self.noOfSteps])
        plt.xlabel('Days in Future')
        plt.ylabel('Simulated price movements')
        plt.title(f'First {noOfMovements}/{self.N} Random Price Movements')
        plt.legend(loc = 'best')
        plt.show()