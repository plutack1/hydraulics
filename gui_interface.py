import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import subprocess
import calculation

# import output


def file_exists(file_path):
    return os.path.isfile(file_path)


def feedback():
    if file_exists(file_path="pipe_data.xlsx"):
        messagebox.showinfo("OK", "calculations completed successfully. ")
    else:
        for i, (key, value) in enumerate(values.items()):
            if value == "":
                messagebox.showerror("Error", "Please fill in all all options.")
                return  # Stop calculation if any text box is empty

            if key == "Design area selected (ft²):":
                if not 1500 <= float(value) <= 3000:
                    messagebox.showerror(
                        "Error",
                        "Design area range exceeded. Please refer to NFPA 13 for design area range.",
                    )
                    return
    pass


class Gui(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Hydraulics Calculation App")

        self.rowconfigure(0, minsize=50)
        self.rowconfigure(1, minsize=50)
        self.rowconfigure(2, minsize=50)
        self.rowconfigure(3, minsize=50)

        self.labels = [
            "Design area selected (ft²):",
            "Length of study area (ft):",
            "Width of study area (ft):",
            "Sprinkler coefficient:",
            "Ceiling Elevation:",
            "Distance to Tank location:"
        ]
        self.text_boxes = []

        for i, label_text in enumerate(self.labels):
            label = tk.Label(self, text=label_text)
            label.grid(row=i, column=0, sticky="e", padx=10, pady=10)

            text_box = tk.Entry(self)
            text_box.grid(row=i, column=1, padx=10, pady=10)
            self.text_boxes.append(text_box)

        self.dropdown_labels = [
            "Occupancy hazard type",
        ]
        self.dropdown_boxes = []

        for i, dropdown_label in enumerate(self.dropdown_labels):
            label = tk.Label(self, text=dropdown_label)
            label.grid(
                row=i + (len(self.labels) + 1), column=0, sticky="e", padx=10, pady=10
            )
            if dropdown_label == "Occupancy hazard type":
                dropdown_values = [
                    "",
                    "Ordinary Hazard (group 1)",
                    "Ordinary Hazard (group 2)",
                ]
            dropdown_box = ttk.Combobox(self, values=dropdown_values)
            dropdown_box.current(0)
            dropdown_box.grid(
                row=i + (len(self.labels) + 1), column=1, padx=20, pady=10, sticky="w"
            )
            self.dropdown_boxes.append(dropdown_box)

        button = tk.Button(
            self,
            text="Calculate",
            command=lambda: [
                self.calculate_values(),
            ],
        )
        button.grid(
            row=len(self.labels) + len(self.dropdown_labels) + 1,
            column=0,
            columnspan=4,
            padx=10,
            pady=10,
        )

    def calculate_values(self):
        values = {}
        for i, label in enumerate(self.labels):
            values[label] = self.text_boxes[i].get()
        for i, dropdown_label in enumerate(self.dropdown_labels):
            values[dropdown_label] = self.dropdown_boxes[i].get()
        calculation.full_calc(values=values)


# Create an instance of the Gui class and start the main loop
gui = Gui()
gui.mainloop()
