from flask import Flask, request, make_response
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def proxy():
    try:
        url = 'http://localhost:5000'  # The original URL
        auth = ('admin', 'securepassword')  # Your authentication credentials

        if request.method == 'GET':
            response = requests.get(url, auth=auth)
        elif request.method == 'POST':
            # Forward the POST data and headers
            response = requests.post(
                url, 
                auth=auth,
                data=request.get_data(),  # Get the raw POST data
                headers=request.headers         # Forward all headers
            )
        else: # Handle other methods if needed
            return "Method Not Allowed", 405

        response.raise_for_status()

        flask_response = make_response(response.text, response.status_code)
        flask_response.headers = response.headers

        return flask_response

    except requests.exceptions.RequestException as e:
        return f"Error: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)