from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
from analysis.change_point_analysis import run_analysis

app = Flask(__name__)
CORS(app)

@app.route('/api/oil-prices', methods=['GET'])
def get_oil_prices():
    df = pd.read_csv('data/BrentOilPrices.csv')
    df['Date'] = pd.to_datetime(df['Date'], format='mixed', dayfirst=True, errors='coerce')
    df = df.dropna(subset=['Date'])
    return jsonify(df.to_dict(orient='records'))

@app.route('/api/events', methods=['GET'])
def get_events():
    events = pd.read_csv('data/events.csv')
    events['date'] = pd.to_datetime(events['date'])
    return jsonify(events.to_dict(orient='records'))

@app.route('/api/change-point', methods=['GET'])
def change_point():
    result = run_analysis()  # Run analysis logic
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
