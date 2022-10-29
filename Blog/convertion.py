import json
from bson import ObjectId,json_util

def convert_json_to_bson(id:str):
    return ObjectId(oid=id)

def convert_bson_to_json(id:ObjectId):
    json_id = json.loads(json_util.dumps(id))
    return json_id["$oid"]