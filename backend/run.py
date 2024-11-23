from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

# Example route

CORS(app)


@app.route('/')
def home():
    return "Backend!"


@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({"message": "Hello from Flask!"})


if __name__ == '__main__':
    app.run(debug=True)
