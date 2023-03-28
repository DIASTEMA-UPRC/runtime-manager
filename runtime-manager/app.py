# Import custom Libraries
from runtime_handler import start_runtime as start_thread
from runtime_handler import stop_runtime as stop_thread
from Executor_Class import Executor_Class

# Import Libraries
import os
from flask import Flask, request, Response, make_response
import threading

""" Environment Variables """
# Flask app Host and Port
HOST = os.getenv("HOST", "localhost")
PORT = int(os.getenv("PORT", 5000))

""" Global variables """
# The name of the flask app
app = Flask(__name__)

# Ports to be used by the jobs
STARTING_PORT = int(os.getenv("STARTING_PORT", 50000))
ENDING_PORT = int(os.getenv("ENDING_PORT", 60000))
PORTS = {
    # "job-id": port (Between STARTING_PORT and ENDING_PORT)
}

""" Flask endpoints """
# GET /start/<job-id>
@app.route("/start/<job_id>", methods=["GET"])
def start(job_id):
    # Get a new port for the job that is not being used
    for port in range(STARTING_PORT, ENDING_PORT):
        if port not in PORTS.values():
            PORTS[job_id] = port
            break

    # Start the job by making a new thread
    thread = threading.Thread(target = start_thread, args = (job_id, PORTS[job_id], ))
    thread.start()

    # Return the response
    return Response("Job started", status=200)

# GET /stop/<job-id>
@app.route("/stop/<job_id>", methods=["GET"])
def stop(job_id):
    # Stop the job by making a new thread
    thread = threading.Thread(target = stop_thread, args = (job_id, PORTS[job_id], ))
    thread.start()

    # Remove the job from the PORTS dictionary
    PORTS.pop(job_id)

    # Return the response
    return Response("Job stopped", status=200)

# POST /predict/<job-id>
@app.route("/predict/<job_id>", methods=["POST"])
def predict(job_id):
    # Get the request body
    data = request.data

    # Get the request headers
    headers = request.headers

    # Make a new request to the job
    executor = Executor_Class(job_id)
    response = executor.predict(PORTS[job_id], data, headers)

    # Return the response
    return Response(response.content, status=response.status_code)

""" Main """
# Main code
if __name__ == "__main__":
    app.run(HOST, PORT, True)