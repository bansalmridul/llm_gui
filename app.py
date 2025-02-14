from flask import Flask, request, jsonify
from functools import wraps
import os

app = Flask(__name__)

# Basic Authentication
USERNAME = os.getenv("APP_USERNAME", "admin")
PASSWORD = os.getenv("APP_PASSWORD", "password")

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or auth.username != USERNAME or auth.password != PASSWORD:
            return jsonify({"message": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated

@app.route("/")
@require_auth
def home():
    return "Hello World"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
