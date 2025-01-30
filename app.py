from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Active CORS pour toutes les routes

@app.route('/')
def home():
    return "L'API est en ligne !"

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid input"}), 400

    # Exemple de calcul
    revenue = (
        (data["streams"] * 0.004) +
        (data["physicalSales"] * 10) +
        (data["digitalSales"] * 8)
        - data["productionCost"]
    ) * ((100 - data["labelShare"]) / 100)

    return jsonify({"revenue": revenue})

from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "L'API est en ligne !"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
