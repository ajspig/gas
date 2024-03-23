import os
import json
from pymongo import MongoClient


client = MongoClient(host=os.environ.get("ATLAS_URI"))


def lambda_handler(event, context):
    city = event["queryStringParameters"]["city"]
    state = event["queryStringParameters"]["state"]
    print(f"City: {city}, State: {state}")

    # Name of database
    db = client.city_state_request 
    # Name of collection
    collection = db.city_state_request 
    location_query = {
        "city": city,
        "state": state
    }
    # Insert document
    result = collection.insert_one(location_query)
    if not result.inserted_id:
        return "Failed to insert document"
    
    # build http response object
    response = {}
    response['statusCode'] = 200
    response['headers'] = {}
    response['headers']['Content-Type'] = 'application/json'
    response['body'] = json.dumps(location_query)

    return response