# GET /users/{user_id}
# Response: 200 OK
# {
#   "user_id": 1,
#   "username": "john_doe",
#   "email": "john@example.com",
#   "phone_number": "+1234567890",
#   "balance": 150.50,
#   "created_at": "2024-01-01T00:00:00Z"
# }

# PUT /users/{user_id}
# Request Body:
# {
#   "username": "string",
#   "phone_number": "string"
# }
# Response: 200 OK


from fastapi import APIRouter, HTTPException
from typing import Optional , List 
from service import *
from model import *


router = APIRouter()

@router.post("/users", response_model=dict , status_code=201)
async def create_new_user(user_data: User):
    user = await create_user(user_data)
    if user:
        return user
    raise HTTPException(status_code=400, detail="User creation failed")

@router.get("/users" , status_code=200)
async def list_all_users_detail():
    users = await get_all_users()
    return users

@router.get("/users/{user_id}", response_model=dict , status_code=200)
async def get_user_details(user_id):
    user = await get_user(user_id)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")


@router.put("/users/{user_id}", response_model=dict , status_code=200)
async def update_user_details(user_id, user_data: User):
    updated_user = await update_user(user_id, user_data)
    if updated_user:
        return updated_user
    raise HTTPException(status_code=404, detail="User not found")


#wallet endpoint 

# POST /wallet/{user_id}/withdraw
# Request Body:
# {
#   "amount": 50.00,
#   "description": "Withdrew money from wallet"
# }
# Response: 201 Created / 400 Bad Request (insufficient balance)

# POST /wallet/{user_id}/add-money
# Request Body:
# {
#   "amount": 100.00,
#   "description": "Added money to wallet"
# }
# Response: 201 Created
# {
#   "transaction_id": 123,
#   "user_id": 1,
#   "amount": 100.00,
#   "new_balance": 250.50,
#   "transaction_type": "CREDIT"
# }

# GET /wallet/{user_id}/balance
# Response: 200 OK
# {
#   "user_id": 1,
#   "balance": 150.50,
#   "last_updated": "2024-01-01T12:30:00Z"
# }

@router.post("/wallet/{user_id}/withdraw", response_model=dict , status_code=201)
async def withdraw_money(user_id, transaction_data: dict):
    amount = transaction_data.get("amount")
    description = transaction_data.get("description")
    result = await withdraw_money(user_id, amount, description)
    if result:
        return result
    raise HTTPException(status_code=400, detail="Withdrawal failed")


@router.post("/wallet/{user_id}/add-money", response_model=dict , status_code=201)
async def add_money(user_id, transaction_data: dict):
    amount = transaction_data.get("amount")
    description = transaction_data.get("description")
    result = await add_money(user_id, amount, description)
    if result:
        return result
    raise HTTPException(status_code=400, detail="Deposit failed")

@router.get("/wallet/{user_id}/balance", response_model=dict , status_code=200)
async def get_balance(user_id):
    result = await get_balance(user_id)
    if result:
        return result
    raise HTTPException(status_code=404, detail="User not found")



#transaction endpoint

# POST /transactions
# Request Body:
# {
#   "user_id": 1,
#   "transaction_type": "CREDIT|DEBIT",
#   "amount": 100.00,
#   "description": "Manual transaction"
# }
# Response: 201 Created


# GET /transactions/detail/{transaction_id}
# Response: 200 OK
# {
#   "transaction_id": 123,
#   "user_id": 1,
#   "transaction_type": "TRANSFER_OUT",
#   "amount": 25.00,
#   "description": "Transfer to jane_doe",
#   "recipient_user_id": 2,
#   "reference_transaction_id": 124,
#   "created_at": "2024-01-01T12:30:00Z"
# }

# GET /transactions/{user_id}?page=1&limit=10
# Response: 200 OK
# {
#   "transactions": [
#     {
#       "transaction_id": 123,
#       "transaction_type": "CREDIT",
#       "amount": 100.00,
#       "description": "Added money",
#       "created_at": "2024-01-01T12:30:00Z"
#     }
#   ],
#   "total": 50,
#   "page": 1,
#   "limit": 10
# }


@router.post("/transactions", response_model=dict , status_code=201)
async def create_transaction(transaction_data: Transaction):
    result = await create_transaction(transaction_data)
    if result:
        return result
    raise HTTPException(status_code=400, detail="Transaction creation failed")

@router.get("/transactions/detail/{transaction_id}", response_model=dict , status_code=200)
async def get_transaction_detail(transaction_id):
    result = await get_transaction(transaction_id)
    if result:
        return result
    raise HTTPException(status_code=404, detail="Transaction not found")

@router.get("/transactions/{user_id}", response_model=dict , status_code=200) 
async def list_transactions(user_id, page: int = 1, limit: int = 10):
    result = await get_user_transactions(user_id, page, limit)
    if result:
        return result
    raise HTTPException(status_code=404, detail="User not found")



# Transaction Endpoints

# POST /transfer
# Request Body:
# {
#   "sender_user_id": 1,
#   "recipient_user_id": 2,
#   "amount": 25.00,
#   "description": "Payment for dinner"
# }
# Response: 201 Created
# {
#   "transfer_id": "unique_transfer_id",
#   "sender_transaction_id": 123,
#   "recipient_transaction_id": 124,
#   "amount": 25.00,
#   "sender_new_balance": 125.50,
#   "recipient_new_balance": 75.00,
#   "status": "completed"
# }

# Response: 400 Bad Request
# {
#   "error": "Insufficient balance",
#   "current_balance": 10.00,
#   "required_amount": 25.00
# }

# GET /transfer/{transfer_id}
# Response: 200 OK
# {
#   "transfer_id": "unique_transfer_id",
#   "sender_user_id": 1,
#   "recipient_user_id": 2,
#   "amount": 25.00,
#   "description": "Payment for dinner",
#   "status": "completed",
#   "created_at": "2024-01-01T12:30:00Z"
# }


@router.post("/transfer", response_model=dict , status_code=201)
async def create_transfer(transfer_data: dict):
    # Logic to create a new transfer
    result = await transfer_money(
        sender_id=transfer_data["sender_user_id"],
        recipient_id=transfer_data["recipient_user_id"],
        amount=transfer_data["amount"],
        description=transfer_data.get("description")
    )
    if result:
        return result
    raise HTTPException(status_code=400, detail="Transfer creation failed")

@router.get("/transfer/{transfer_id}", response_model=dict , status_code=200)
async def get_transfer_detail(transfer_id):
    # Logic to retrieve transfer details by transfer_id
    result = await get_transaction(transfer_id)
    if result:
        return result
    raise HTTPException(status_code=404, detail="Transfer not found")