import os
from flask import Flask, jsonify
import read_and_print_bondi  # replace with the actual name of your script, without .py
import today_analysis

app = Flask(__name__)

@app.route("/forecast", methods=["GET"])
def get_forecast():
    forecast_data = read_and_print_bondi.get_forecast()  # assume this returns a dict or list
    return jsonify(forecast_data)

@app.route("/today", methods=["GET"])
def get_today_analysis():
    try:
        analysis = today_analysis.get_cached_today_analysis()
        return jsonify(analysis)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host="0.0.0.0", port=port)