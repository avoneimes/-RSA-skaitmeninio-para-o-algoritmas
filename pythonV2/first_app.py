import tkinter as tk
from tkinter import messagebox
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
import json
import requests

def generate_rsa_key_pair():
    # Generuoti RSA raktų porą: privatųjį ir viešąjį raktą
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    return private_key, public_key

def sign_message(private_key, message):
    # Pasirašyti pranešimą naudojant privatųjį raktą ir PSS su SHA256
    signature = private_key.sign(
        message.encode('utf-8'),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

def serialize_public_key(public_key):
    # Serializuoti viešąjį raktą PEM formatu
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

def application_1(message):
    # Generuoti raktų porą
    private_key, public_key = generate_rsa_key_pair()
    # Pasirašyti pranešimą
    signature = sign_message(private_key, message)

    # Serializuoti viešąjį raktą ir konvertuoti parašą į šešioliktainę eilutę
    public_key_bytes = serialize_public_key(public_key)
    signature_hex = signature.hex()

    # Paruošti duomenis siuntimui
    data_to_send = {
        'public_key': public_key_bytes.decode('utf-8'),
        'message': message,
        'signature': signature_hex
    }

    # Išsaugoti duomenis į JSON failą
    with open("data.json", "w") as f:
        json.dump(data_to_send, f)

    # Siųsti duomenis į serverį per POST užklausą
    response = requests.post("http://localhost:5001/store", json=data_to_send)
    if response.status_code == 200:
        return "Data sent successfully"
    else:
        return "Failed to send data"

def on_submit():
    # Paimti įvestą pranešimą ir iškviesti application_1 funkciją
    message = entry_message.get()
    status = application_1(message)
    messagebox.showinfo("Status", status)

# GUI nustatymai
root = tk.Tk()
root.title("First Application")

# Pranešimo įvedimo laukas
plaintext_label = tk.Label(root, text="Enter message")
plaintext_label.grid(row=0, column=0, padx=10, pady=5)
entry_message = tk.Entry(root, width=50)
entry_message.grid(row=0, column=1, padx=10, pady=5)

# Pateikimo mygtukas
submit_button = tk.Button(root, text="Submit", command=on_submit)
submit_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
