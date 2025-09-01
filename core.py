
import motor.motor_asyncio
from pymongo.server_api import ServerApi

uri = "mongodb+srv://ansuman-shukla:ansuman@cluster0.zkpcq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new async client and connect to the server
client = motor.motor_asyncio.AsyncIOMotorClient(uri, server_api=ServerApi('1'))

# create a db
db = client["digital_wallet"]

# create collections
users_collection = db["users"]
transactions_collection = db["transactions"]
