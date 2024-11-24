from flask import Flask, jsonify, request
from flask_cors import CORS
from app import llm

app = Flask(__name__)

# Example route

CORS(app)


@app.route('/')
def home():
    return "Backend!"


@app.route('/html')
def get_html():
    with open('temp/output.html') as file:
        return file.read(), 200, {'Content-Type': 'text/html'}


@app.route('/api/data', methods=['POST'])
def get_data():
    # Get text and standard from JSON

    input_text = request.form.get('text', '')
    standard = request.form.get('standard', '')

    # Check if input_text is empty and try to get it from the uploaded file
    if not input_text and 'file1' in request.files:
        file = request.files['file1']
        if file:
            input_text = file.read().decode('utf-8')  # Assuming the file is a text file

    # Check if standard is empty and try to get it from the uploaded file
    if not standard and 'file2' in request.files:
        file = request.files['file2']
        if file:
            standard = file.read().decode('utf-8')

    processed_data = llm.inspect(input_text, standard)

    file_path = "temp/output.html"

    # Writing the content to the file
    with open(file_path, "w") as file:  # "w" mode overwrites the file; use "a" to append
        file.write(input_text)

    return jsonify(processed_data)


if __name__ == '__main__':
    app.run(debug=True)
