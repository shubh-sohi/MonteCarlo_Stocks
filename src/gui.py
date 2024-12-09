from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from monte_carlo import MonteCarloStocks

def user_val_plot(e, e1, window):
    """
    Triggered when the user presses the plot button.
    Retrieves the stock symbol and the number of iterations, then uses the Monte Carlo class to generate the plot.
    """
    monte_carlo = MonteCarloStocks(e.get())
    plot_gui(monte_carlo.plot_monte_carlo(int(e1.get())), window)

def plot_gui(graph, window):
    """
    Displays the generated plot in the tkinter GUI.
    """
    for widget in window.winfo_children():
        widget.destroy()  # Clear existing widgets for a clean slate

    # Create a frame for the graph
    graph_f = Frame(window)
    graph_f.pack()

    # Add a title label
    l_new = Label(graph_f, text="Monte Carlo Simulations for Stock Price Predictions")
    l_new.pack()

    # Display the graph
    canvas = FigureCanvasTkAgg(graph, master=graph_f)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Add a navigation toolbar
    toolbar = NavigationToolbar2Tk(canvas, graph_f)
    toolbar.update()
    canvas.get_tk_widget().pack()

def run_gui_app():
    """
    Initializes and runs the tkinter GUI application.
    """
    window = Tk()
    window.title("Monte Carlo Simulations")
    window.geometry("700x550")

    # Create the input frame
    f = Frame(window)
    f.pack()

    # Add instructions and input fields
    l = Label(f, text="Monte Carlo Simulations for Stock Price Predictions \n\nPlease enter the stock symbol in CAPS (e.g., TSLA)")
    l.pack()

    e = Entry(f)
    e.pack()
    e.focus_set()

    l1 = Label(f, text="Please enter the number of simulations you want to run (e.g., 100)")
    l1.pack()

    e1 = Entry(f)
    e1.pack()

    # Add a plot button
    plot_button = Button(master=f, command=lambda: user_val_plot(e, e1, window), text="Plot")
    plot_button.pack()

    # Run the tkinter main loop
    window.mainloop()
