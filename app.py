from flask import Flask, request, jsonify
from flask_cors import CORS
from elasticsearch import Elasticsearch
from datetime import datetime

es = Elasticsearch(["http://localhost:9200"])
if es.ping():
    print("pinged")
else:
    print("no pinged")
conn_document = {
    "timestamp": datetime.now(),
    "text": "This is a test to see if the connection works",
    "userID": "test_conn"
}
response = es.index(index="test", body=conn_document)
app = Flask(__name__)

# Allow CORS for the specific origin (localhost:80 for frontend)
CORS(app, origins="http://localhost", methods=["GET", "POST", "OPTIONS"])

@app.route('/reverse', methods=['POST'])
def reverse_text():
    data = request.get_json()
    text = data.get('message', '')
    if not text:
        return jsonify({"error": "No text provided"}), 400
    
    user_document = {
        "timestamp": datetime.now(),
        "text": text,
        "userID": "default_user" #can be expanded to handle a generic user, in my case it will always be me
    }
    response = es.index(index="test", body=user_document)
    
    reversed_text = text[::-1]
    bot_document = {
        "timestamp": datetime.now(),
        "text": text,
        "userID": "bot" #can be expanded to match the id of the llm if you are running multiple
    }
    response = es.index(index="test", body=bot_document)
    
    return jsonify({"message": reversed_text})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
