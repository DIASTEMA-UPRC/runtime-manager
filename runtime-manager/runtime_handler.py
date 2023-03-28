# Import custom Libraries
from MongoDB_Class import MongoDB_Class
from Executor_Class import Executor_Class

# All possible states of a job
STATES = {
    "RUNNING": "Running",
    "PENDING": "Pending",
    "DOWN": "Down"
}

def start_runtime(job_id, port):
    # Create a MongoDB_Class object
    mongo = MongoDB_Class()

    # Change the state of the job to "Pending"
    mongo.change_state(job_id, STATES["PENDING"])

    # Run the job
    executor = Executor_Class(job_id)
    executor.run(port)

    # Change the state of the job to "Running"
    mongo.change_state(job_id, STATES["RUNNING"])

    return

def stop_runtime(job_id, port):
    # Create a MongoDB_Class object
    mongo = MongoDB_Class()

    # Stop the job
    executor = Executor_Class(job_id)
    executor.stop(port)

    # Change the state of the job to "Down"
    mongo.change_state(job_id, STATES["DOWN"])

    return