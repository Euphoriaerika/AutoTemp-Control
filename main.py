from calculation_tap import calculation_tap
from flask import Flask, request, jsonify
from flask_cors import CORS  # Додайте цей імпорт

app = Flask(__name__)
CORS(app)  # Додайте це для вирішення проблеми CORS

@app.route('/update', methods=['POST'])
def update_water_angle():
    try:
        temperature = request.json['temperature']
        # Викликайте функцію для визначення кута відповідно до температури
        angle = calculation_tap(temperature)
        return jsonify({'angle': angle})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)

