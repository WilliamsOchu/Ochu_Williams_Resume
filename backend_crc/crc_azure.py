import json
import os
import azure.functions as func
from azure.cosmos import CosmosClient


## Initialize and manage database


## Set the Cosmosdb variables by obtaining the env variables
endpoint = os.environ["COSMOS_ENDPOINT"]
account_key = os.environ["COSMOS_KEY"]

## Establish a connection to the cosmosdb container 
client = CosmosClient(url=endpoint, credential=account_key)
database_name = "DB_CRC_Azure"
container_name = "CRC_Azure_Container"
id = "1"

database = client.get_database_client(database_name)
container = database.get_container_client(container_name)

## Define a function to read and increment the count in DB by +1

def item_count_updater(req: func.HttpRequest) -> func.HttpResponse: 
    # Get the current count item in the DB
    existing_item = container.read_item(id, id)

    # Validate the item exists in the DB
    if not existing_item:
        return func.HttpResponse(
            "Count item missing",
            status_code=400  # Bad Request
        )
    
    # Obtain the value of the count dict_key
    counts_present = existing_item.get('count', 0)

    # Increment the count item by +1 
    count_updated = counts_present + 1

    # Proceed to update the count item which was just incremented
    existing_item['count'] = count_updated
    container.upsert_item(existing_item)
    
    # Format the updated dict as a JSON so it can be interpreted by the webpage
    item_json = json.dumps(existing_item, indent=2)

    # Return the full dict as a JSON response
    return func.HttpResponse(
        body=item_json, 
        mimetype='application/json',
        status_code=200
    )


