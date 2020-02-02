import os
import json

import pymongo

from pprint import pprint


user = "root"
password = "toor"
host = "localhost"
port = 27017

#
# 1. Create connection
#
conn = pymongo.MongoClient(f"mongodb://{user}:{password}@{host}", port)


#
# 2. Create a database (not initialized until gets some data)
#
test_db = conn["test_db"]

# Get databases names
all_dbs = conn.list_database_names()

print(f"Databases' names: {all_dbs}")


#
# 3. Create a collection (not initialized until gets some data)
#
gps_data = test_db['gps']

# Get collections names
all_collections = test_db.list_collection_names()
print(f"Collections'' names: {all_collections}")


#
# 4.Write a record into collection
#

# Read JSON file from file

json_data = {}
with open("data.json") as file:
    json_data = json.load((file))

record_id = gps_data.insert_one(json_data)
print(f"Assigned record's ID: {record_id.inserted_id}")

#
# 5. Fetching data
#

# Take one record
fetched_record = gps_data.find_one()

print("One record:")
pprint(fetched_record)


# Take all records

fetched_record = gps_data.find()

print("All records:")

for i, record in enumerate(fetched_record):
    pprint(f"{i} : {record} ")


# Return only some fields

only_fields_records = gps_data.find({},{
    "_id":0,
    "device": 1,
})

print("Records with some fields:")

for i, record in enumerate(only_fields_records):
    pprint(f"{i} : {record} ")


# Filter records

query = {"device.type":"smartphone"}

filtered_records = gps_data.find(query)

print("Filtered records:")

for i, record in enumerate(filtered_records):
    pprint(f"{i} : {record} ")
