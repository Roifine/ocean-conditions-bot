from flask import Flask, jsonify
import read_and_print_bondi  # replace with the actual name of your script, without .py

app = Flask(__name__)

@app.route("/forecast", methods=["GET"])
def get_forecast():
    forecast_data = read_and_print_bondi.get_forecast()  # assume this returns a dict or list
    return jsonify(forecast_data)

if __name__ == "__main__":
    app.run(debug=True)