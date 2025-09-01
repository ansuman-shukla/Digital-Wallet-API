# // Users Collection
# {
#   "_id": ObjectId,
#   "username": "string",
#   "email": "string",
#   "password": "string",
#   "phone_number": "string",
#   "balance": 0.00,
#   "created_at": Date,
#   "updated_at": Date
# }

# // Transactions Collection
# {
#   "_id": ObjectId,
#   "user_id": ObjectId,
#   "transaction_type": "CREDIT|DEBIT|TRANSFER_IN|TRANSFER_OUT",
#   "amount": 0.00,
#   "description": "string",
#   "reference_transaction_id": ObjectId, // For linking transfers
#   "recipient_user_id": ObjectId, // For transfers
#   "created_at": Date
# }

def user_schema(item):
    return {
        "_id": item.get("_id"),
        "username": item.get("username"),
        "email": item.get("email"),
        "password": item.get("password"),
        "phone_number": item.get("phone_number"),
        "balance": item.get("balance", 0.00),
        "created_at": item.get("created_at"),
        "updated_at": item.get("updated_at")
    }

def transaction_schema(item):
    return {
        "_id": item.get("_id"),
        "user_id": item.get("user_id"),
        "transaction_type": item.get("transaction_type"),
        "amount": item.get("amount", 0.00),
        "description": item.get("description"),
        "reference_transaction_id": item.get("reference_transaction_id"),
        "recipient_user_id": item.get("recipient_user_id"),
        "created_at": item.get("created_at")
    }

def return_users_list(items):
    return [user_schema(item) for item in items]

def return_transactions_list(items):
    return [transaction_schema(item) for item in items]