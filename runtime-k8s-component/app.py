# Import custom Libraries
from command_handler import exec_command as command_thread

# Import Libraries
import os
from flask import Flask, request, Response, make_response
import requests
import random
import threading

""" Environment Variables """
# Flask app Host and Port
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 11112))

# MinIO Data
MINIO_HOST = os.getenv("MINIO_HOST", "10.20.20.191")
MINIO_PORT = int(os.getenv("MINIO_PORT", 9000))
MINIO_USER = os.getenv("MINIO_USER", "diastema")
MINIO_PASS = os.getenv("MINIO_PASS", "diastema")

# Mongo Data
MONGO_HOST = os.getenv("MONGO_HOST", "10.20.20.205")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))

# Kubernetes Data
# KUBERNETES_HOST = os.getenv("KUBERNETES_HOST", "192.168.49.2")
# KUBERNETES_PORT = int(os.getenv("KUBERNETES_PORT", "8443"))

EXECUTOR_HOST = os.getenv("EXECUTOR_HOST", "0.0.0.0")

DUMMY = os.getenv("DUMMY", "FALSE")

""" Global variables """
# The name of the flask app
app = Flask(__name__)

""" Flask endpoints """
# GET /run/<port>
@app.route("/run/<port>", methods=["GET"])
def run(port):
    # Check if the DUMMY environment variable is set to TRUE
    if DUMMY == "TRUE" :
        # Create the response
        response = make_response("Dummy response")
        # Set the response status code
        response.status_code = 200
        # Return the response
        return response

    # Run the job on Terminal
    cmd = 'spark-submit '
    cmd += '--conf spark.executorEnv.FLASK_HOST="'+EXECUTOR_HOST+'" '
    cmd += '--conf spark.executorEnv.FLASK_PORT="'+str(port)+'" '
    cmd += '--conf spark.executorEnv.MINIO_HOST="'+MINIO_HOST+'" '
    cmd += '--conf spark.executorEnv.MINIO_PORT="'+str(MINIO_PORT)+'" '
    cmd += '--conf spark.executorEnv.MINIO_USER="'+MINIO_USER+'" '
    cmd += '--conf spark.executorEnv.MINIO_PASS="'+MINIO_PASS+'" '
    cmd += '--conf spark.executorEnv.MONGO_HOST="'+MONGO_HOST+'" '
    cmd += '--conf spark.executorEnv.MONGO_PORT="'+str(MONGO_PORT)+'" '
    cmd += '/home/ubuntu/daas-analytics-catalogue-executor/src/main.py'

    thread = threading.Thread(target = command_thread, args = (cmd, ))
    thread.start()

    return Response(status=200)

# GET /check/<port>
@app.route("/check/<port>", methods=["GET"])
def check(port):
    # Check if the DUMMY environment variable is set to TRUE
    if DUMMY == "TRUE" :
        # Return 200 with 0.2 probability
        if random.random() < 0.2:
            return Response(status=200)
        else:
            return Response(status=201)

    # Check if the job is running
    url = "http://"+EXECUTOR_HOST+":"+str(port)+"/health"
    response = requests.get(url)
    print("THIS IS THE URL: " + url)
    print("THIS IS THE RESPONSE: " + str(response.status_code))

    return Response(status = response.status_code)

# GET /load/<job_id>/<port>
@app.route("/load/<job_id>/<port>", methods=["GET"])
def load(job_id, port):
    # Check if the DUMMY environment variable is set to TRUE
    if DUMMY == "TRUE" :
        # Create the response
        response = make_response("Dummy response")
        # Set the response status code
        response.status_code = 200
        # Return the response
        return response

    # Load the job's model
    url = "http://"+EXECUTOR_HOST+":"+str(port)+"/start/"+str(job_id)
    response = requests.get(url)
    print(response.content)

    return Response(status=200)

# GET /kill/<port>
@app.route("/kill/<port>", methods=["GET"])
def kill(port):
    # Check if the DUMMY environment variable is set to TRUE
    if DUMMY == "TRUE" :
        # Create the response
        response = make_response("Dummy response")
        # Set the response status code
        response.status_code = 200
        # Return the response
        return response

    # Kill the job
    url = "http://"+EXECUTOR_HOST+":"+str(port)+"/kill"
    requests.get(url)
    return Response(status=200)

# POST /predict/<port>
@app.route("/predict/<port>", methods=["POST"])
def predict(port):
    # Check if the DUMMY environment variable is set to TRUE
    if DUMMY == "TRUE" :
        # Create the response
        response = make_response("Dummy response")
        # Set the response status code
        response.status_code = 200
        # Return the response
        return response

    # Get the request body
    data = request.data

    # Get the request headers
    headers = request.headers

    # Predict the job
    url = "http://"+EXECUTOR_HOST+":"+str(port)+"/predict"

    # Send the request
    response = requests.post(url, data=data, headers=headers)

    return Response(response.content, status=response.status_code)

""" Main """
# Main code
if __name__ == "__main__":
    app.run(HOST, PORT, True)
