# Import Libraries
import os
import requests
from flask import Flask, request, Response, make_response

""" Environment Variables """
# Flask app Host and Port
HOST = os.getenv("HOST", "localhost")
PORT = int(os.getenv("PORT", 5001))

RUNTIME_MANAGER_HOST = os.getenv("RUNTIME_MANAGER_HOST", "localhost")
RUNTIME_MANAGER_PORT = int(os.getenv("RUNTIME_MANAGER_PORT", 5000))

""" Global variables """
# The name of the flask app
app = Flask(__name__)

""" Flask endpoints """
# POST /predict/<job-id>
@app.route("/predict/<job_id>", methods=["POST"])
def predict(job_id):
    # Send the same request to the runtime-manager
    # Get the request body
    data = request.data

    # Get the request headers
    headers = request.headers

    # Make a new request to the runtime-manager
    response = requests.post(f"http://{RUNTIME_MANAGER_HOST}:{str(RUNTIME_MANAGER_PORT)}/predict/{job_id}", data=data, headers=headers)

    # Return the response
    return Response(response.content, status=response.status_code)

""" Main """
# Main code
if __name__ == "__main__":
    app.run(HOST, PORT, True)