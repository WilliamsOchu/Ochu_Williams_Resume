import unittest
import os
from azure.cosmos import CosmosClient


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

## Establish a class for each of the unittests
class TestCalcls(unittest.TestCase):

    def test_cosmosDB_client(self):
        result = str(client)
        self.assertEqual(result, os.environ["COSMOSDB_CLIENT"])

    def test_cosmosDB_databse_name(self):
        result = str(database)
        self.assertEqual(result, os.environ["COSMOSDB_ACC_NAME"])

    def test_cosmosDB_container_name(self):
        result = str(container)
        self.assertEqual(result, os.environ["COSMOSDB_CONT_NAME"])

    def test_cosmosdb_count(self):
        ## Increase the count value
        existing_item = container.read_item(id, id)
        counts_present = existing_item.get('count', 0)
        count_updated = counts_present + 1
        existing_item['count'] = count_updated
        container.upsert_item(existing_item)
        self.assertTrue(container.upsert_item(existing_item))

        ## Decrease the count value so it does not count as a view
        existing_item2 = container.read_item(id, id)
        counts_present2 = existing_item2.get('count', 0)
        count_updated1 = counts_present2 - 1
        existing_item2['count'] = count_updated1
        container.upsert_item(existing_item2)
        self.assertTrue(container.upsert_item(existing_item2))
        

## Initialize all tests to run simultaneously
if __name__ == '__main__':
    unittest.main()