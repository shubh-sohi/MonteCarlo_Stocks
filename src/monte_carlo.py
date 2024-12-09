import numpy as np
import yfinance as yf

class MonteCarloStocks:
    """
    This is a class that uses the Monte Carlo formulas to simulate future stock prices.
    """

    def __init__(self, stock_ticket):
        """
        Initializes the Monte Carlo model with the stock ticket symbol and fetches the adjusted close price from Yahoo Finance.
        """
        self.ticker = stock_ticket
        data = yf.download(self.ticker, start='2014-1-1')
        self.data_adj_close = data['Adj Close']
        self.initial = data['Adj Close'].iloc[-1]

    def mean_std_cal(self):
        """
        Returns the mean and the standard deviation of the logarithmic returns of the adjusted close prices.
        """
        log_return = np.log(1 + self.data_adj_close.pct_change())
        return log_return.mean(), log_return.std()

    def stimulated_price(self):
        """
        Simulates the stock price using the Monte Carlo method, generating a future stock price using the calculated mean and standard deviation.
        """
        mean_std = self.mean_std_cal()
        sim_rets = np.random.normal(mean_std[0], mean_std[1], 252)
        return self.initial * ((sim_rets + 1).cumprod())

    def plot_monte_carlo(self, num_iterations):
        """
        Plots the simulated stock prices for a specified number of iterations.
        """
        from matplotlib.figure import Figure

        fig = Figure()
        plot1 = fig.add_subplot(111)
        for i in range(num_iterations):
            sim_prices = self.stimulated_price()
            plot1.plot(sim_prices)
        return fig