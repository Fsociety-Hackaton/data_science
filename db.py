from pymongo import MongoClient
import json

def connection():
    """
    This function connect to the MongoDB
    """
    client = MongoClient('mongodb+srv://carlos:fxjIeeoQRrf2CLRK@cluster0.pqec0.mongodb.net/')
    db = client.data

    return db

def insert_jobs():
    pass