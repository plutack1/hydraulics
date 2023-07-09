import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def file_exists(file_path):
    return os.path.isfile(file_path)

# Example usage





def calculate():
    # Check if any text box is blank
    for text_box in text_boxes:
        if text_box.get().strip() == "":
            messagebox.showerror("Error", "Please fill in all the text boxes.")
            return  # Stop calculation if any text box is empty

    # Check if any dropdown box has no selection
    for dropdown_box in dropdown_boxes:
        if dropdown_box.get().strip() == "":
            messagebox.showerror("Error", "Please select an option from all dropdown boxes.")
            return  # Stop calculation if any dropdown box has no selection

    # Continue with your calculation logic here
    
    
    if file_exists(file_path="pipe_data.xlsx"):
        messagebox.showinfo("OK", "calculations completed successfully. ")
    else:
        messagebox.showerror("Error", "calculations did not complete successfully. Please check your inputs and try again.")

    pass









# Create the main window
window = tk.Tk()
window.title("GUI Example")

# Set the window size and position
# window.geometry("500x600")

# Set the vertical spacing between rows
window.rowconfigure(0, minsize=50)
window.rowconfigure(1, minsize=50)
window.rowconfigure(2, minsize=50)
window.rowconfigure(3, minsize=50)

labels = [
    "Design area selected (ft²):",
    "Length of study area (ft):",
    "Width of study area (ft):",
    "Sprinkler coefficient:",
]
# Create the labels and text boxes
text_boxes = []

for i, label_text in enumerate(labels):
    label = tk.Label(window, text=label_text)
    label.grid(row=i, column=0, sticky="e", padx=10, pady=10)

    text_box = tk.Entry(window)
    text_box.grid(row=i, column=1, padx=10, pady=10)
    text_boxes.append(text_box)

# Create the dropdown boxes
dropdown_labels = [
    "occupancy hazard type",
]
dropdown_boxes = []

for i, dropdown_label in enumerate(dropdown_labels):
    label = tk.Label(window, text=dropdown_label)
    label.grid(row=i + (len(text_boxes) + 1), column=0, sticky="e", padx=10, pady=10)
    if dropdown_label == "occupancy hazard type":
        dropdown_values = [
            "",
            "Ordinary Hazard (group 1)",
            "Ordinary Hazard (group 2)",
        ]
    dropdown_box = ttk.Combobox(window, values=dropdown_values)
    dropdown_box.current(0)  # Set the default selection
    dropdown_box.grid(row=i + (len(text_boxes) + 1), column=1, padx=20, pady=10, sticky="w")
    dropdown_boxes.append(dropdown_box)

# Create the calculate button
button = tk.Button(window, text="Calculate", command=calculate)
button.grid(row=len(text_boxes) + len(dropdown_boxes) + 1, column=0, columnspan=4, padx=10, pady=10)

# Start the main loop
window.mainloop()
