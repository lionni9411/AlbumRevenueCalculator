from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def home():
    return "L'API est en ligne !"

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.json

        # Récupérer les données avec des valeurs par défaut
        streams = float(data.get("streams", 0))
        physicalSales = float(data.get("physicalSales", 0))
        digitalSales = float(data.get("digitalSales", 0))
        productionCost = float(data.get("productionCost", 0))
        labelShare = min(max(float(data.get("labelShare", 0)) / 100, 0), 1)  # Limiter entre 0 et 100%
        taxRate = float(data.get("taxRate", 20)) / 100  # Par défaut à 20%

        # Prix par album physique et digital
        physicalPrice = float(data.get("physicalPrice", 10))  # Par défaut à 10 €
        digitalPrice = float(data.get("digitalPrice", 5))  # Par défaut à 5 €

        # Valider les valeurs
        if streams < 0 or physicalSales < 0 or digitalSales < 0 or productionCost < 0 or physicalPrice <= 0 or digitalPrice <= 0:
            return jsonify({"error": "Les valeurs ne peuvent pas être négatives ou nulles."}), 400

        # Calcul des revenus
        streamsRevenue = streams * 0.004  # Moyenne réaliste pour les streams
        physicalRevenue = physicalSales * physicalPrice
        digitalRevenue = digitalSales * digitalPrice
        totalRevenue = streamsRevenue + physicalRevenue + digitalRevenue

        revenueAfterLabel = totalRevenue * (1 - labelShare)
        revenueAfterTax = revenueAfterLabel * (1 - taxRate)
        netRevenue = revenueAfterTax - productionCost

        return jsonify({
            "netRevenue": round(netRevenue, 2),
            "taxRate": taxRate * 100,
            "totalRevenue": round(totalRevenue, 2),
            "revenueAfterLabel": round(revenueAfterLabel, 2),
            "streamsRevenue": round(streamsRevenue, 2),
            "physicalRevenue": round(physicalRevenue, 2),
            "digitalRevenue": round(digitalRevenue, 2),
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
