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
    # Get text and standart from JSON
    input_text = request.json.get('text', '')
    standart = request.json.get('standart', '')

    # Check if input_text is empty and try to get it from the uploaded file
    if not input_text and 'file1' in request.files:
        file = request.files['file1']
        if file:
            input_text = file.read().decode('utf-8')  # Assuming the file is a text file

    # Check if standart is empty and try to get it from the uploaded file
    if not standart and 'file2' in request.files:
        file = request.files['file2']
        if file:
            standart = file.read().decode('utf-8')

    processed_text = llm.analyze(input_text, standart)

    return jsonify({"message": processed_text})


if __name__ == '__main__':
    app.run(debug=True)
