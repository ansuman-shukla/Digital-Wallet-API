from pydantic import BaseModel
from abc import ABC, abstractmethod
from enum import Enum


class TransactionType(str, Enum):
    CREDIT = "credit"
    DEBIT = "debit"
    TRANSFER_IN = "transfer_in"
    TRANSFER_OUT = "transfer_out"


class User(BaseModel):
    user_id: int
    username: str
    email: str
    phone_number: str
    balance: float


class Transaction(BaseModel):
    transaction_id: int
    user_id: int
    transaction_type: TransactionType
    amount: float
    description: str
    

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

