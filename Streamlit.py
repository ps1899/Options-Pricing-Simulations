from enum import Enum
from datetime import datetime, timedelta
import streamlit as st
from Option_Pricing import Black_Scholes_Pricing, Binomial_Tree_Pricing, Monte_Carlo_Pricing, Ticker
from Option_Pricing.Base import OptionPricingModel

class OptionPricingModel(Enum):
    blackScholes = 'Black Scholes Model'
    monteCarlo = 'Monte Carlo Simulation'
    binomialTree = 'Binomial Tree Model'

    @st.cache
    def getHistoricalData(ticker):
        return Ticker.getHistoricalData(ticker)
    
    st.set_option('deprecation.showPyPlotGlobalUse', False)

    st.title('Option Pricing')

    pricingMethod = st.sidebar.radio('Please select option pricing method', options = [model.value for model in OptionPricingModel])

    st.subheader(f'Pricing method: {pricingMethod}')

    if(pricingMethod == OptionPricingModel.blackScholes.value):
        tickerBS = st.text_input('Ticker Symbol', 'AAPL')
        strikePriceBS = st.number_input('Strike Price', 300)
        riskFreeRateBS = st.slider('Risk-Free Rate (%)', 0, 100, 10)
        sigmaBS = st.slider('Sigma (%)', 0, 100, 20)
        exerciseDataBS = st.date_input('Exercise date', min_value = datetime.today() + timedelta(days = 1), value = datetime.today() + timedelta(days = 365))

        if(st.button(f'Calculate option price for {tickerBS}')):
            dataBS = getHistoricalData(tickerBS)
            st.write(dataBS.tail())
            Ticker.plotData(dataBS, tickerBS, 'Adj Close')
            st.pyplot()

            spotPriceBS = Ticker.getLastPrice(dataBS, 'Adj Close')
            RiskFreeRateBS = riskFreeRateBS/100
            SigmaBS = sigmaBS/100
            daysToMatureBS = (exerciseDataBS - datetime.now().date()).days

            callOptionPriceBS = Black_Scholes_Pricing(spotPriceBS, strikePriceBS, daysToMatureBS, RiskFreeRateBS, SigmaBS).calculate_option_price('Call Option')
            putOptionPriceBS = Black_Scholes_Pricing(spotPriceBS, strikePriceBS, daysToMatureBS, RiskFreeRateBS, SigmaBS).calculate_option_price('Pull Option')

            st.subheader(f'Call Option price: {callOptionPriceBS}')
            st.subheader(f'Put Option price: {putOptionPriceBS}')
        
    elif(pricingMethod == OptionPricingModel.monteCarlo.value):
        tickerMC = st.text_input('Ticker Symbol', 'AAPL')
        strikePriceMC = st.number_input('Strike Price', 300)
        riskFreeRateMC = st.slider('Risk-Free Rate (%)', 0, 100, 10)
        sigmaMC = st.slider('Sigma (%)', 0, 100, 20)
        exerciseDataMC = st.date_input('Exercise date', min_value = datetime.today() + timedelta(days = 1), value = datetime.today() + timedelta(days = 365))
        noOfSimulationsMC = st.slider('Number of simulations', 100, 100000, 10000)
        noOfStepsMC = st.slider('Number of price movements simulations to be visualized', 0, int(noOfSimulationsMC/10), 100)

        if(st.button(f'Calculate option price for {tickerMC}')):
            dataMC = getHistoricalData(tickerMC)
            st.write(dataMC.tail())
            Ticker.plotData(dataMC, tickerMC, 'Adj Close')
            st.pyplot()

            spotPriceMC = Ticker.getLastPrice(dataMC, 'Adj Close')
            RiskFreeRateMC = riskFreeRateMC/100
            SigmaMC = sigmaMC/100
            daysToMatureMC = (exerciseDataMC - datetime.now().date()).days

            Monte_Carlo_Pricing(spotPriceMC, strikePriceMC, daysToMatureMC, RiskFreeRateMC, SigmaMC, noOfSimulationsMC).simulatePrices()
            Monte_Carlo_Pricing(spotPriceMC, strikePriceMC, daysToMatureMC, RiskFreeRateMC, SigmaMC, noOfSimulationsMC).plotSimulation(noOfStepsMC)
            st.pyplot()

            callOptionPriceMC = Monte_Carlo_Pricing(spotPriceMC, strikePriceMC, daysToMatureMC, RiskFreeRateMC, SigmaMC, noOfSimulationsMC).calculate_option_price('Call Option')
            putOptionPriceMC = Monte_Carlo_Pricing(spotPriceMC, strikePriceMC, daysToMatureMC, RiskFreeRateMC, SigmaMC, noOfSimulationsMC).calculate_option_price('Put Option')

            st.subheader(f'Call Option price: {callOptionPriceMC}')
            st.subheader(f'Put Option price: {putOptionPriceMC}')

    elif(pricingMethod == OptionPricingModel.binomialTree.value):
        tickerBT = st.text_input('Ticker Symbol', 'AAPL')
        strikePriceBT = st.number_input('Strike Price', 300)
        riskFreeRateBT = st.slider('Risk-Free Rate (%)', 0, 100, 10)
        sigmaBT = st.slider('Sigma (%)', 0, 100, 20)
        exerciseDataBT = st.date_input('Exercise date', min_value = datetime.today() + timedelta(days = 1), value = datetime.today() + timedelta(days = 365))
        noOfStepsBT = st.slider('Number of time steps', 5000, 100000, 15000)

        if st.button(f'Calculate option price for {tickerBT}'):
            dataBT = getHistoricalData(tickerBT)
            st.write(dataBT.tail())
            Ticker.plotData(dataBT, tickerBT, 'Adj Close')
            st.pyplot()
        
        spotPriceBT = Ticker.getLastPrice(dataBT, 'Adj Close')
        RiskFreeRateBT = riskFreeRateBT/100
        SigmaBT = sigmaBT/100
        daysToMatureBT = (exerciseDataBT - datetime.now().date()).days

        callOptionPriceBT = Binomial_Tree_Pricing(spotPriceBT, strikePriceBT, daysToMatureBT, RiskFreeRateBT, SigmaBT, noOfStepsBT).calculate_option_price('Call Option')
        putOptionPriceBT =  Binomial_Tree_Pricing(spotPriceBT, strikePriceBT, daysToMatureBT, RiskFreeRateBT, SigmaBT, noOfStepsBT).calculate_option_price('Put Option')

        st.subheader(f'Call Option price: {callOptionPriceBT}')
        st.subheader(f'Put Option price: {putOptionPriceBT}')