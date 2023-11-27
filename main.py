import subprocess
import os
import tempfile
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/hello', methods=['GET'])
def hello():
    return jsonify({"content": "hello"})

@app.route('/upload', methods=['POST'])
def upload_files():
    print(request.headers)
    if 'file1' not in request.files or 'file2' not in request.files:
        return jsonify({"error": "No file part"})

    file1 = request.files['file1']
    file2 = request.files['file2']

    if file1.filename == '' or file2.filename == '':
        return jsonify({"error": "No selected file"})

    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        filepath1 = os.path.join(temp_dir, file1.filename)
        filepath2 = os.path.join(temp_dir, file2.filename)

        file1.save(filepath1)
        file2.save(filepath2)

        # Run git diff with --no-index
        diff_result = subprocess.run(['git', 'diff', '--no-index', filepath1, filepath2], cwd=temp_dir, text=True, capture_output=True)

        # Return the diff result in JSON format
        return jsonify({"diff-result": diff_result.stdout})

if __name__ == '__main__':
    app.run(debug=True)
