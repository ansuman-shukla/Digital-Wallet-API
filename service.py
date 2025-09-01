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

async def update_user(user_id: str, user_data: dict):
    try:
        user = await users_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            return {"error": "User not found"}

        allowed_updates = {"username", "phone_number"}
        update_data = {k: v for k, v in user_data.items() if k in allowed_updates}
        update_data["updated_at"] = datetime.now()

        await users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )

        updated_user = await users_collection.find_one({"_id": ObjectId(user_id)})
        return {
            "user_id": str(updated_user["_id"]),
            "username": updated_user["username"],
            "email": updated_user["email"],
            "phone_number": updated_user.get("phone_number"),
            "updated_at": updated_user["updated_at"]
        }
    except Exception as e:
        return {"error": str(e)}



# wallet service 

async def withdraw_money(user_id: str, amount: float, description: Optional[str] = None):
    if amount <= 0:
        return {"error": "Amount must be positive"}

    try:
        user = await users_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            return {"error": "User not found"}
        
        if user["balance"] < amount:
            return {
                "error": "Insufficient balance",
                "current_balance": user["balance"],
                "required_amount": amount
            }

        # Create transaction first
        transaction = {
            "user_id": ObjectId(user_id),
            "transaction_type": "DEBIT",
            "amount": amount,
            "description": description,
            "created_at": datetime.now()
        }
        tx_result = await transactions_collection.insert_one(transaction)

        # Update balance atomically
        await users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$inc": {"balance": -amount}}
        )

        updated_user = await users_collection.find_one({"_id": ObjectId(user_id)})
        return {
            "transaction_id": str(tx_result.inserted_id),
            "user_id": str(user_id),
            "amount": amount,
            "new_balance": updated_user["balance"],
            "transaction_type": "DEBIT"
        }
    except Exception as e:
        return {"error": str(e)}

async def add_money(user_id: str, amount: float, description: Optional[str] = None):
    if amount <= 0:
        return {"error": "Amount must be positive"}

    try:
        user = await users_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            return {"error": "User not found"}

        # Create transaction first
        transaction = {
            "user_id": ObjectId(user_id),
            "transaction_type": "CREDIT",
            "amount": amount,
            "description": description,
            "created_at": datetime.now()
        }
        tx_result = await transactions_collection.insert_one(transaction)

        # Update balance atomically
        await users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$inc": {"balance": amount}}
        )

        updated_user = await users_collection.find_one({"_id": ObjectId(user_id)})
        return {
            "transaction_id": str(tx_result.inserted_id),
            "user_id": str(user_id),
            "amount": amount,
            "new_balance": updated_user["balance"],
            "transaction_type": "CREDIT"
        }
    except Exception as e:
        return {"error": str(e)}


async def get_balance(user_id):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return {"user_id": user_id, "balance": user["balance"], "last_updated": user.get("updated_at", datetime.now())}
    return {"error": "User not found"}


# transaction service

async def create_transaction(transaction_data: dict):
    if transaction_data.get("amount", 0) <= 0:
        return {"error": "Amount must be positive"}

    result = await transactions_collection.insert_one({
        **transaction_data,
        "created_at": datetime.now()
    })
    return {"transaction_id": str(result.inserted_id), **transaction_data}

async def get_transaction(transaction_id: str):
    try:
        transaction = await transactions_collection.find_one({"_id": ObjectId(transaction_id)})
        if transaction:
            return {
                "transaction_id": str(transaction["_id"]),
                "user_id": str(transaction["user_id"]),
                "transaction_type": transaction["transaction_type"],
                "amount": transaction["amount"],
                "description": transaction.get("description"),
                "recipient_user_id": str(transaction.get("recipient_user_id")) if transaction.get("recipient_user_id") else None,
                "reference_transaction_id": str(transaction.get("reference_transaction_id")) if transaction.get("reference_transaction_id") else None,
                "created_at": transaction["created_at"]
            }
    except Exception:
        return {"error": "Invalid transaction ID"}
    return {"error": "Transaction not found"}

async def get_user_transactions(user_id: str, page: int = 1, limit: int = 10):
    skip = (page - 1) * limit
    total = await transactions_collection.count_documents({"user_id": ObjectId(user_id)})
    
    cursor = transactions_collection.find({"user_id": ObjectId(user_id)})
    cursor.sort("created_at", -1).skip(skip).limit(limit)
    
    transactions = []
    async for tx in cursor:
        transactions.append({
            "transaction_id": str(tx["_id"]),
            "transaction_type": tx["transaction_type"],
            "amount": tx["amount"],
            "description": tx.get("description"),
            "created_at": tx["created_at"]
        })
    
    return {
        "transactions": transactions,
        "total": total,
        "page": page,
        "limit": limit
    }

# transfer service

async def transfer_money(sender_id: str, recipient_id: str, amount: float, description: Optional[str] = None):
    if amount <= 0:
        return {"error": "Amount must be positive"}
    
    try:
        sender = await users_collection.find_one({"_id": ObjectId(sender_id)})
        recipient = await users_collection.find_one({"_id": ObjectId(recipient_id)})

        if not sender:
            return {"error": "Sender not found"}
        if not recipient:
            return {"error": "Recipient not found"}
        if sender["balance"] < amount:
            return {
                "error": "Insufficient balance",
                "current_balance": sender["balance"],
                "required_amount": amount
            }

        # Create sender's transaction (TRANSFER_OUT)
        sender_tx = await transactions_collection.insert_one({
            "user_id": ObjectId(sender_id),
            "transaction_type": "TRANSFER_OUT",
            "amount": amount,
            "description": description,
            "recipient_user_id": ObjectId(recipient_id),
            "created_at": datetime.now()
        })

        # Create recipient's transaction (TRANSFER_IN)
        recipient_tx = await transactions_collection.insert_one({
            "user_id": ObjectId(recipient_id),
            "transaction_type": "TRANSFER_IN",
            "amount": amount,
            "description": description,
            "reference_transaction_id": sender_tx.inserted_id,
            "created_at": datetime.now()
        })

        # Update sender's transaction with reference
        await transactions_collection.update_one(
            {"_id": sender_tx.inserted_id},
            {"$set": {"reference_transaction_id": recipient_tx.inserted_id}}
        )

        # Update balances atomically
        await users_collection.update_one(
            {"_id": ObjectId(sender_id)},
            {"$inc": {"balance": -amount}}
        )
        await users_collection.update_one(
            {"_id": ObjectId(recipient_id)},
            {"$inc": {"balance": amount}}
        )

        # Get updated balances
        updated_sender = await users_collection.find_one({"_id": ObjectId(sender_id)})
        updated_recipient = await users_collection.find_one({"_id": ObjectId(recipient_id)})

        return {
            "transfer_id": str(sender_tx.inserted_id),
            "sender_transaction_id": str(sender_tx.inserted_id),
            "recipient_transaction_id": str(recipient_tx.inserted_id),
            "amount": amount,
            "sender_new_balance": updated_sender["balance"],
            "recipient_new_balance": updated_recipient["balance"],
            "status": "completed"
        }
    except Exception as e:
        return {"error": str(e)}
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