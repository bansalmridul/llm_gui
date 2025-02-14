from flask import Flask, make_response
import requests

app = Flask(__name__)

@app.route('/')  # This defines the URL endpoint (/)
def index():
    try:
        response = requests.get('http://localhost:5000', auth=('admin', 'securepassword'))
        response.raise_for_status()  # Check for HTTP errors (404, 500, etc.)

        # Make a Flask response with the content from localhost:5000
        flask_response = make_response(response.text, response.status_code)
        flask_response.headers = response.headers  # Copy headers (important!)

        return flask_response

    except requests.exceptions.RequestException as e:
        return f"Error: {e}", 500  # Return an error message to the browser

if __name__ == '__main__':
    app.run(debug=True)  # Start the Flask development server