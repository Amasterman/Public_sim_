import tkinter as tk

class HeuristicSelector(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        # create a dynamic on/off variable
        self.dynamic = tk.BooleanVar(value=True)

        # create a dropdown menu for selecting a heuristic
        self.heuristic = tk.StringVar()
        self.heuristic_menu = tk.OptionMenu(self, self.heuristic, "heuristic1", "heuristic2", "heuristic3")
        self.heuristic_menu.pack(side="top")

        # create a checkbutton for turning dynamic on/off
        self.dynamic_checkbutton = tk.Checkbutton(self, text="Dynamic", variable=self.dynamic)
        self.dynamic_checkbutton.pack(side="top")

        # create a submit button
        self.submit_button = tk.Button(self, text="Submit", command=self.submit)
        self.submit_button.pack(side="bottom")

        # Create the a slider for amount of passengers
        self.passenger_amount_label = tk.Label(self,text='Passenger amount:')
        self.passenger_amount_label.pack(side="top")
        self.passenger_amount = tk.Entry(self, width=5)
        self.passenger_amount.pack(side="top")

        # Create the a slider for amount of buses
        self.bus_amount_label = tk.Label(self, text='Bus amount:')
        self.bus_amount_label.pack(side="top")
        self.bus_amount = tk.Entry(self, width=5)
        self.bus_amount.pack(side="top")

        # Simulator setup
        self.sim_label = tk.Label(self, text='Simulator settings')
        self.sim_label.pack(side='top')

        self.sim_runs_label = tk.Label(self, text='Number of Runs:')
        self.sim_runs_label.pack(side='top')
        self.sim_runs = tk.Entry(self, width=5)
        self.sim_runs.pack(side='top')


    def submit(self):
        # handle the submission of the form here
        print("Selected heuristic:", self.heuristic.get())
        print("Dynamic mode:", self.dynamic.get())
        print("Passenger amount: ", self.passenger_amount.get())
        print("Bus amount: ", self.bus_amount.get())

def main():
    root = tk.Tk()
    root.geometry("500x500")
    HeuristicSelector(root).pack(side="top", fill="both", expand=True)
    root.mainloop()

if __name__ == "__main__":
    main()