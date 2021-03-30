# Implementation of the Monte carlo Simulations on Stocks to make a future price prediction
# Includes an object "MonteCarloStocks" which computes the future stock price Simulations by using Monte carlo formulas
# The price values are then plotted onto a graph

# Finally with the use of GUI, user input of stock Symbol and Number of iterations are taken which
# are passed to the object above.
# The resulting graph is then plotted onto the GUI

import numpy as np
import yfinance as yf
from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)


class MonteCarloStocks:
    """
    This is a class that uses the Monte Carlo formulas using mu, standard deviation and variance.
    Class works on the input of stock_name and number of iterations from user and the final result is in the form of
    a graph which is passed on to the GUI functions.
    """

    def __init__(self, stock_ticket):
        """
        Using the yahoo finance API, adjusted close price for desired stock is stored from 2014-01-1 to present
        """
        self.ticker = stock_ticket
        data = yf.download(self.ticker, start='2014-1-1')
        self.data_adj_close = data['Adj Close']
        # gets the last element from pandas dataset
        self.initial = data['Adj Close'].iloc[-1]

    def mean_std_cal(self):
        """
        Function to return the mean and the standard deviation of the natural logarithmic values
         of the percent change of adjusted close values from one day before
         Yes all of that computation made possible because of numpy. Calculating the percent change, natural log,
         mean and standard deviation
        """
        log_return = np.log(1 + self.data_adj_close.pct_change())
        return (log_return.mean(), log_return.std())

    def stimulated_price(self):
        """
        Using the mean and standard deviation, calculated the simulated returns.
        from a normal Gaussian distribution, a random sample is chosen and the span of 252 represents
        the 252 trading days in a year(excluding holidays)
        """
        mean_std = self.mean_std_cal()
        sim_rets = np.random.normal(mean_std[0], mean_std[1], 252)
        # multiplying the latest stock price to the simulated returns to get
        # a future price and a cumulative product is returned
        return self.initial * ((sim_rets + 1).cumprod())

    def plot_monte_carlo(self, num_iterations):
        """
        plotting the randomly predicted stock price and doing the same num_iterations of times.
        every iteration, a new stock price is plotted because of the randomly picked value.
        A plot is returned which is used by the GUI functions
        """
        fig = Figure()
        plot1 = fig.add_subplot(111)
        for i in range(num_iterations):
            sim_prices = self.stimulated_price()
            plot1.plot(sim_prices)
        return fig


def user_val_plot():
    """
    User input is saved as this function is triggered when the user presses the plot button. Two global variables
    store the stock_symbol and num_iterations and are accessed from outside the function.
    Then Passes the stock symbol is to create a Montee Carlo class instance and the num_iteration to get the graph
    """
    global e, e1
    monte_carlo = MonteCarloStocks(e.get())
    # function call to plot the graph to GUI is made here using the graph as argument
    plot_gui(monte_carlo.plot_monte_carlo(int(e1.get())))


def plot_gui(graph):
    """
    Graph generated from class instance is shown on the GUI here.
    """
    f.destroy()
    graph_f = Frame(window)
    graph_f.pack()
    l_new = Label(graph_f, text="Monte Carlo Simulations for Stock Price Predictions")
    l_new.pack()
    canvas = FigureCanvasTkAgg(graph, master=graph_f)
    canvas.draw()
    canvas.get_tk_widget().pack()
    toolbar = NavigationToolbar2Tk(canvas, window)
    toolbar.update()
    canvas.get_tk_widget().pack()


if __name__ == "__main__":
    # standard tkinter function to initiate a GUI with some text
    window = Tk()
    f = Frame(window)
    f.pack()
    window.title("Monte Carlo Simulations")
    window.geometry("700x550")
    l = Label(f, text="Monte Carlo Simulations for Stock Price Predictions \n\n "
                      "Please enter the stock symbol in CAPS(e.g. TSLA)")
    l.pack()

    e = Entry(f)
    e.pack()
    e.focus_set()

    l1 = Label(f, text="Please enter the amount of simulations you want to run(e.g. 100)")
    l1.pack()

    e1 = Entry(f)
    e1.pack()
    # button press triggers the user_val_plot() function
    plot_button = Button(master=f, command=user_val_plot, text="Plot")
    plot_button.pack()

    # run the gui
    window.mainloop()
