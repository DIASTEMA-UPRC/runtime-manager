# Import Libraries
import os
from pymongo import MongoClient

class MongoDB_Class:
    MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
    MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))

    DATABASE = os.getenv("DATABASE", "UIDB")
    COLLECTION = os.getenv("COLLECTION", "podstates")

    def __init__(self):
        mongo_host = MongoDB_Class.MONGO_HOST+":"+str(MongoDB_Class.MONGO_PORT)
        self.mongo_client = MongoClient("mongodb://"+mongo_host+"/")
        return
    
    def change_state(self, job_id, state):
        self.mongo_client[self.DATABASE][self.COLLECTION].update_one(
            {"job-id": job_id},
            {"$set": {"state": state}}
        )
        return