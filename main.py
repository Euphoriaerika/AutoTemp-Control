from calculation_tap import calculation_tap  # Importing the calculation_tap function from a module
from flask import Flask, request, jsonify  # Importing necessary modules from Flask
from flask_cors import CORS  # Adding CORS support for handling cross-origin requests

app = Flask(__name__)  # Creating a Flask application instance
CORS(app)  # Allowing Cross-Origin Resource Sharing (CORS) for the Flask app

@app.route('/update', methods=['POST'])  # Defining a route for updating water angle via POST request
def update_water_angle():
    try:
        temperature = request.json['temperature']  # Extracting temperature data from the JSON request

        angle = calculation_tap(temperature)  # Calculating the angle needed to achieve comfortable temperature
        return jsonify({'angle': angle})  # Returning the calculated angle as JSON response
    except Exception as e:
        return jsonify({'error': str(e)})  # Returning an error message if an exception occurs

if __name__ == '__main__':
    app.run(debug=True)  # Running the Flask app in debug mode if executed as the main script
