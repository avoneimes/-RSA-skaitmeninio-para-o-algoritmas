from flask import Flask, request, jsonify

app = Flask(__name__)

# Globali saugykla viešajam raktui, pranešimui ir parašui saugoti
storage = {
    "public_key": None,
    "message": None,
    "signature": None
}

@app.route('/store', methods=['POST'])
def store_data():
    # Gauti duomenis iš POST užklausos ir išsaugoti juos globalioje saugykloje
    data = request.json
    storage["public_key"] = data["public_key"]
    storage["message"] = data["message"]
    storage["signature"] = data["signature"]
    # Grąžinti sėkmės atsakymą
    return jsonify({"status": "success"}), 200

@app.route('/retrieve', methods=['GET'])
def retrieve_data():
    # Grąžinti visą saugyklos turinį JSON formatu
    return jsonify(storage), 200

@app.route('/alter', methods=['POST'])
def alter_data():
    # Gauti duomenis iš POST užklausos ir, jei yra pranešimas, pakeisti saugyklos pranešimą
    data = request.json
    if "message" in data:
        storage["message"] = data["message"]
    # Grąžinti atsakymą, nurodantį, kad duomenys buvo pakeisti
    return jsonify({"status": "altered"}), 200

if __name__ == '__main__':
    # Paleisti serverį, kuris klausosi 5001 prievado
    app.run(host='0.0.0.0', port=5001)
