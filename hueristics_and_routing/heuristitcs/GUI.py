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

    def submit(self):
        # handle the submission of the form here
        print("Selected heuristic:", self.heuristic.get())
        print("Dynamic mode:", self.dynamic.get())

def main():
    root = tk.Tk()
    root.geometry("500x500")
    HeuristicSelector(root).pack(side="top", fill="both", expand=True)
    root.mainloop()

if __name__ == "__main__":
    main()