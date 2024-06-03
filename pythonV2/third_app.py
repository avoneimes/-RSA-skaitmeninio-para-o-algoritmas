import tkinter as tk
from tkinter import messagebox
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
import json
import requests

def deserialize_public_key(public_key_bytes):
    # Deserializuoti viešąjį raktą iš PEM formato
    return serialization.load_pem_public_key(public_key_bytes)

def verify_signature(public_key, message, signature):
    try:
        # Patikrinti parašą naudojant viešąjį raktą, pranešimą ir PSS su SHA256
        public_key.verify(
            signature,
            message.encode('utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception:
        return False

def application_3():
    # Gauti duomenis iš serverio per GET užklausą
    response = requests.get("http://localhost:5001/retrieve")
    if response.status_code == 200:
        data = response.json()
        # Išsaugoti gautus duomenis į JSON failą
        with open("data.json", "w") as f:
            json.dump(data, f)
        
        # Ištraukti viešąjį raktą, pranešimą ir parašą iš gautų duomenų
        public_key_str = data['public_key']
        message = data['message']
        signature_hex = data['signature']

        # Deserializuoti viešąjį raktą ir konvertuoti parašą iš šešioliktainio formato
        public_key = deserialize_public_key(public_key_str.encode('utf-8'))
        signature = bytes.fromhex(signature_hex)

        # Patikrinti parašą ir grąžinti rezultatą
        is_valid = verify_signature(public_key, message, signature)
        return f"Signature valid: {is_valid}"
    else:
        return "Failed to retrieve data"

def on_submit():
    # Iškvietus application_3 funkciją, parodyti rezultatą
    status = application_3()
    messagebox.showinfo("Verification Result", status)

def alter_data():
    # Gauti naują pranešimą iš įvesties lauko ir siųsti jį į serverį per POST užklausą
    new_message = entry_message.get()
    response = requests.post("http://localhost:5001/alter", json={"message": new_message})
    if response.status_code == 200:
        messagebox.showinfo("Status", "Data altered successfully")
    else:
        messagebox.showinfo("Status", "Failed to alter data")

# GUI nustatymai
root = tk.Tk()
root.title("Third Application")

# Pranešimo įvedimo laukas duomenų pakeitimui
plaintext_label = tk.Label(root, text="Enter new message to alter data")
plaintext_label.grid(row=0, column=0, padx=10, pady=5)
entry_message = tk.Entry(root, width=50)
entry_message.grid(row=0, column=1, padx=10, pady=5)

# Mygtukas duomenų pakeitimui
alter_button = tk.Button(root, text="Alter Data", command=alter_data)
alter_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Mygtukas parašo patikrinimui
submit_button = tk.Button(root, text="Verify Data", command=on_submit)
submit_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()

