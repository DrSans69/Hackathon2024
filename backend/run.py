from flask import Flask, jsonify, request
from flask_cors import CORS
from app import llm

app = Flask(__name__)

# Example route

CORS(app)


@app.route('/')
def home():
    return "Backend!"


@app.route('/api/data', methods=['POST'])
def get_data():
    input_text = request.json.get('text', '')
    standart = request.json.get('standart', '')

    history = []
    processed_text = llm.analyze(input_text, standart, history)

    return jsonify({"message": processed_text})


if __name__ == '__main__':
    app.run(debug=True)
