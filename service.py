from bson import ObjectId
from datetime import datetime
from typing import List, Optional
from core import db , users_collection, transactions_collection
from model import User
from schema import *



async def create_user(user: User):
    user_data = user.model_dump()
    user_data["balance"] = 0.00
    user_data["created_at"] = datetime.now()
    user_data["updated_at"] = datetime.now()
    
    result = await users_collection.insert_one(user_data)
    return {
        "user_id": str(result.inserted_id),
        "username": user_data.get("username"),
        "email": user_data.get("email"),
        "phone_number": user_data.get("phone_number"),
        "balance": user_data.get("balance", 0.00),
        "created_at": user_data.get("created_at"),
        "updated_at": user_data.get("updated_at")
    }

async def get_all_users():
    users = []
    cursor = users_collection.find()
    async for user in cursor:
        users.append({
            "user_id": str(user["_id"]),
            "username": user.get("username"),
            "email": user.get("email"),
            "phone_number": user.get("phone_number"),
            "balance": user.get("balance", 0.00),
            "created_at": user.get("created_at"),
            "updated_at": user.get("updated_at")
        })
    return users

async def get_user(user_id):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return {
            "user_id": str(user["_id"]),
            "username": user.get("username"),
            "email": user.get("email"),
            "phone_number": user.get("phone_number"),
            "balance": user.get("balance", 0.00),
            "created_at": user.get("created_at"),
            "updated_at": user.get("updated_at")
        }
    return {"error": "User not found"}

async def update_user(user_id, user_data: dict):
    # Logic to update a user by ID
    await users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": user_data})
    return {"user_id": user_id, **user_data}



# wallet service 

async def withdraw_money(user_id, amount: float, description: Optional[str] = None):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        if user["balance"] >= amount:
            new_balance = user["balance"] - amount
            await users_collection.update_one(
                {"_id": ObjectId(user_id)}, 
                {"$set": {"balance": new_balance}}
            )
            transaction = {
                "user_id": str(user_id),
                "amount": -amount,
                "description": description,
                "timestamp": datetime.now()
            }
            await transactions_collection.insert_one(transaction)
            return {"message": "Withdrawal successful", "new_balance": user["balance"]}
        return {"error": "Insufficient funds"}
    return {"error": "User not found"}


async def add_money(user_id, amount: float, description: Optional[str] = None):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        user["balance"] += amount
        await users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": {"balance": user["balance"]}})
        transaction = {
            "user_id": user_id,
            "amount": amount,
            "description": description,
            "timestamp": datetime.now()
        }
        await transactions_collection.insert_one(transaction)
        return {"message": "Deposit successful", "new_balance": user["balance"]}
    return {"error": "User not found"}


async def get_balance(user_id):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return {"user_id": user_id, "balance": user["balance"], "last_updated": user.get("updated_at", datetime.now())}
    return {"error": "User not found"}


# transaction service

async def create_transaction(transaction_data: dict):
    result = await transactions_collection.insert_one(transaction_data)
    return {"transaction_id": str(result.inserted_id), **transaction_data}

async def get_transaction(transaction_id: str):
    transaction = await transactions_collection.find_one({"_id": ObjectId(transaction_id)})
    if transaction:
        return {"transaction_id": transaction["_id"], **transaction}
    return {"error": "Transaction not found"}


async def get_user_transactions(user_id):
    transactions = await transactions_collection.find({"user_id": user_id}).to_list(length=None)
    return {"user_id": user_id, "transactions": transactions}


# transfer service

async def transfer_money(sender_id, recipient_id, amount: float, description: Optional[str] = None):
    sender = await users_collection.find_one({"_id": ObjectId(sender_id)})
    recipient = await users_collection.find_one({"_id": ObjectId(recipient_id)})

    if not sender:
        return {"error": "Sender not found"}
    if not recipient:
        return {"error": "Recipient not found"}
    if sender["balance"] < amount:
        return {"error": "Insufficient funds"}

    # Deduct from sender
    sender["balance"] -= amount
    await users_collection.update_one({"_id": ObjectId(sender_id)}, {"$set": {"balance": sender["balance"]}})

    # Add to recipient
    recipient["balance"] += amount
    await users_collection.update_one({"_id": ObjectId(recipient_id)}, {"$set": {"balance": recipient["balance"]}})

    # Create transactions for both users
    sender_transaction = {
        "user_id": sender_id,
        "amount": -amount,
        "description": f"Transfer to {recipient_id}. {description or ''}",
        "timestamp": datetime.now()
    }
    recipient_transaction = {
        "user_id": recipient_id,
        "amount": amount,
        "description": f"Transfer from {sender_id}. {description or ''}",
        "timestamp": datetime.now()
    }

    await transactions_collection.insert_one(sender_transaction)
    await transactions_collection.insert_one(recipient_transaction)

    return {
        "message": "Transfer successful",
        "sender_new_balance": sender["balance"],
        "recipient_new_balance": recipient["balance"]
    }


async def get_transfer_history(user_id):
    transfers = await transactions_collection.find({"user_id": user_id}).to_list(length=None)
    return {"user_id": user_id, "transfers": transfers}