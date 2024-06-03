import tkinter as tk
from tkinter import messagebox
import json
import requests

def application_2():
    # Gauti duomenis iš serverio per GET užklausą
    response = requests.get("http://localhost:5001/retrieve")
    if response.status_code == 200:
        data = response.json()
        # Išsaugoti gautus duomenis į JSON failą
        with open("data.json", "w") as f:
            json.dump(data, f)
        return "Data received and saved successfully"
    else:
        return "Failed to retrieve data"

def on_submit():
    # Iškvietus application_2 funkciją, parodyti rezultatą
    status = application_2()
    messagebox.showinfo("Status", status)

# GUI nustatymai
root = tk.Tk()
root.title("Second Application")

# Pateikimo mygtukas
submit_button = tk.Button(root, text="Retrieve Data", command=on_submit)
submit_button.grid(row=0, column=0, padx=10, pady=10)

root.mainloop()

