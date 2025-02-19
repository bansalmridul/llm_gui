from flask import Flask, request, jsonify
from flask_cors import CORS
import elasticsearch


app = Flask(__name__)

# Allow CORS for the specific origin (localhost:80 for frontend)
CORS(app, origins="http://localhost", methods=["GET", "POST", "OPTIONS"])

@app.route('/reverse', methods=['POST'])
def reverse_text():
    data = request.get_json()
    text = data.get('message', '')
    if not text:
        return jsonify({"error": "No text provided"}), 400
    
    reversed_text = text[::-1]
    return jsonify({"message": reversed_text})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
