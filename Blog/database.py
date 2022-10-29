import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb-url")

db = client.Moderton

blog_collection=db['Blog']
user_collection=db['User']