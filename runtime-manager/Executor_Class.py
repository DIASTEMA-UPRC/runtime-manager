# Import Libraries
import os
import requests
import time

class Executor_Class:
    K8S_COMPONENT_HOST = os.getenv("K8S_COMPONENT_HOST", "localhost")
    K8S_COMPONENT_PORT = int(os.getenv("K8S_COMPONENT_PORT", 5002))

    TIME_TO_WAIT = int(os.getenv("TIME_TO_WAIT", 1))

    def __init__(self, job_id):
        self.job_id = job_id
        return
    
    # Run the job by making a requests and waiting for it to finish
    # Then load the job's model
    def run(self, port):
        # Create the Run URL
        url = "http://"+self.K8S_COMPONENT_HOST+":"+str(self.K8S_COMPONENT_PORT)+"/run/"+str(port)

        # Kill the job by making a GET request to the /run endpoint
        requests.get(url)

        # Wait for the job to start
        while True:
            # Create the Check URL
            url = "http://"+self.K8S_COMPONENT_HOST+":"+str(self.K8S_COMPONENT_PORT)+"/check/"+str(port)

            # Check if status is 200
            response = requests.get(url)
            if response.status_code == 200:
                break
            time.sleep(self.TIME_TO_WAIT)
        
        # Load the job's model
        # Create the Load URL by passing the job-id and port
        url = "http://"+self.K8S_COMPONENT_HOST+":"+str(self.K8S_COMPONENT_PORT)+"/load/"+str(self.job_id)+"/"+str(port)

        # Load the job's model by making a GET request to the /load endpoint
        requests.get(url)

        return
    
    # Kill the job by making a GET request to the /kill endpoint
    def stop(self, port):
        # Create the URL
        url = "http://"+self.K8S_COMPONENT_HOST+":"+str(self.K8S_COMPONENT_PORT)+"/kill/"+str(port)

        # Kill the job by making a GET request to the /kill endpoint
        requests.get(url)
        return
    
    # Predict by making a POST request to the /predict endpoint
    def predict(self, port, data, headers):
        # Create the URL
        url = "http://"+self.K8S_COMPONENT_HOST+":"+str(self.K8S_COMPONENT_PORT)+"/predict/"+str(port)

        # Predict by making a POST request to the /predict endpoint
        response = requests.post(url, data=data, headers=headers)
        return response
