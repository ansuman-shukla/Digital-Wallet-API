from pydantic import BaseModel
from abc import ABC, abstractmethod
from enum import Enum
from bson import ObjectId
from datetime import datetime


class TransactionType(str, Enum):
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"
    TRANSFER_IN = "TRANSFER_IN"
    TRANSFER_OUT = "TRANSFER_OUT"



class User(BaseModel):
    username: str
    email: str
    password: str
    phone_number: str | None = None
    balance: float = 0.00
    created_at: datetime | None = None
    updated_at: datetime | None = None


class Transaction(BaseModel):
    user_id: str
    transaction_type: TransactionType
    amount: float
    description: str
    timestamp: datetime

# [
#   {
#     "user_id": 1,
#     "transaction_type": "CREDIT",
#     "amount": 100.00,
#     "description": "Initial wallet load"
#   },
#   {
#     "user_id": 1,
#     "transaction_type": "TRANSFER_OUT",
#     "amount": 25.00,
#     "description": "Transfer to jane_smith",
#     "recipient_user_id": 2
#   }
# ]

# [
#   {
#     "username": "john_doe",
#     "email": "john@example.com",
#     "password": "password123",
#     "phone_number": "+1234567890",
#     "balance": 100.00
#   },
#   {
#     "username": "jane_smith",
#     "email": "jane@example.com",
#     "password": "password456",
#     "phone_number": "+1987654321",
#     "balance": 50.00
#   }
# ]

