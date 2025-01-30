from flask import Flask, request, jsonify
from flask_cors import CORS  # ✅ Import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # ✅ Autoriser toutes les requêtes

@app.route('/')
def home():
    return "L'API est en ligne !"

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.json

        streams = float(data.get("streams", 0))
        physicalSales = float(data.get("physicalSales", 0))
        digitalSales = float(data.get("digitalSales", 0))
        productionCost = float(data.get("productionCost", 0))
        labelShare = float(data.get("labelShare", 0)) / 100
        taxRate = float(data.get("taxRate", 20)) / 100  # Par défaut à 20%

        # Calcul des revenus
        streamsRevenue = streams * 0.003  # 0.003 € par stream
        physicalRevenue = physicalSales * 10  # 10 € par vente physique
        digitalRevenue = digitalSales * 5  # 5 € par vente digitale
        totalRevenue = streamsRevenue + physicalRevenue + digitalRevenue

        revenueAfterLabel = totalRevenue * (1 - labelShare)
        revenueAfterTax = revenueAfterLabel * (1 - taxRate)
        netRevenue = revenueAfterTax - productionCost

        return jsonify({
            "netRevenue": round(netRevenue, 2),
            "taxRate": taxRate * 100,
            "totalRevenue": round(totalRevenue, 2),
            "revenueAfterLabel": round(revenueAfterLabel, 2),
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
