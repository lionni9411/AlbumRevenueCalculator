from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    streams = float(data['streams']) * 0.003  # 0.003 € par stream
    physical_sales = float(data['physicalSales']) * 10  # 10 € par vente physique
    digital_sales = float(data['digitalSales']) * 5  # 5 € par vente digitale
    revenue = streams + physical_sales + digital_sales
    return jsonify({'revenue': round(revenue, 2)})

if __name__ == '__main__':
    app.run(debug=True)
