Digital Wallet API
Problem Overview
Build a backend application using FastAPI that functions as a digital wallet system. It should allow users to manage their wallets, maintain transaction records, and simulate money transfers between users. Note: This is only a backend simulation; no real money will be transferred.


Core Requirements
Backend Development (FastAPI + Python)
Build a RESTful API with the following CRUD operations and business logic:
User Management
User Profile: Retrieve and update user information
Initial Balance: Users start with a balance of 0
Transaction Management
Create Transaction: Record debit/credit transactions for users
Transaction History: Retrieve user's transaction history with pagination
Transaction Details: Get specific transaction information
Transaction Types: Support DEBIT, CREDIT, TRANSFER_IN, TRANSFER_OUT
Wallet Operations
Balance Inquiry: Get current wallet balance for a user
Add Money: Credit money to user's wallet (CREDIT transaction)
Withdraw Money: Debit money from user's wallet (DEBIT transaction)
Money Transfer: Transfer money between two users
Transfer System
Peer-to-Peer Transfer: Transfer money from one user to another
Transfer Validation: Ensure sender has sufficient balance
Atomic Transactions: Ensure transfer operations are atomic (both debit and credit succeed or fail together)
Database Schema
Choose ONE Database Option:
Option A: SQL Database (PostgreSQL/MySQL/SQLite)
-- Users Table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone_number VARCHAR(15),
    balance DECIMAL(10,2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Transactions Table
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    transaction_type VARCHAR(20) NOT NULL, -- 'CREDIT', 'DEBIT', 'TRANSFER_IN', 'TRANSFER_OUT'
    amount DECIMAL(10,2) NOT NULL,
    description TEXT,
    reference_transaction_id INTEGER REFERENCES transactions(id), -- For linking transfer transactions
    recipient_user_id INTEGER REFERENCES users(id), -- For transfers
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

Option B: NoSQL Database (MongoDB)
// Users Collection
{
  "_id": ObjectId,
  "username": "string",
  "email": "string",
  "password": "string",
  "phone_number": "string",
  "balance": 0.00,
  "created_at": Date,
  "updated_at": Date
}

// Transactions Collection
{
  "_id": ObjectId,
  "user_id": ObjectId,
  "transaction_type": "CREDIT|DEBIT|TRANSFER_IN|TRANSFER_OUT",
  "amount": 0.00,
  "description": "string",
  "reference_transaction_id": ObjectId, // For linking transfers
  "recipient_user_id": ObjectId, // For transfers
  "created_at": Date
}

API Endpoints Specification
User Profile Endpoints
GET /users/{user_id}
Response: 200 OK
{
  "user_id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "phone_number": "+1234567890",
  "balance": 150.50,
  "created_at": "2024-01-01T00:00:00Z"
}

PUT /users/{user_id}
Request Body:
{
  "username": "string",
  "phone_number": "string"
}
Response: 200 OK

Wallet Endpoints
GET /wallet/{user_id}/balance
Response: 200 OK
{
  "user_id": 1,
  "balance": 150.50,
  "last_updated": "2024-01-01T12:30:00Z"
}

POST /wallet/{user_id}/add-money
Request Body:
{
  "amount": 100.00,
  "description": "Added money to wallet"
}
Response: 201 Created
{
  "transaction_id": 123,
  "user_id": 1,
  "amount": 100.00,
  "new_balance": 250.50,
  "transaction_type": "CREDIT"
}

POST /wallet/{user_id}/withdraw
Request Body:
{
  "amount": 50.00,
  "description": "Withdrew money from wallet"
}
Response: 201 Created / 400 Bad Request (insufficient balance)

Transaction Endpoints
GET /transactions/{user_id}?page=1&limit=10
Response: 200 OK
{
  "transactions": [
    {
      "transaction_id": 123,
      "transaction_type": "CREDIT",
      "amount": 100.00,
      "description": "Added money",
      "created_at": "2024-01-01T12:30:00Z"
    }
  ],
  "total": 50,
  "page": 1,
  "limit": 10
}

GET /transactions/detail/{transaction_id}
Response: 200 OK
{
  "transaction_id": 123,
  "user_id": 1,
  "transaction_type": "TRANSFER_OUT",
  "amount": 25.00,
  "description": "Transfer to jane_doe",
  "recipient_user_id": 2,
  "reference_transaction_id": 124,
  "created_at": "2024-01-01T12:30:00Z"
}

POST /transactions
Request Body:
{
  "user_id": 1,
  "transaction_type": "CREDIT|DEBIT",
  "amount": 100.00,
  "description": "Manual transaction"
}
Response: 201 Created

Transfer Endpoints
POST /transfer
Request Body:
{
  "sender_user_id": 1,
  "recipient_user_id": 2,
  "amount": 25.00,
  "description": "Payment for dinner"
}
Response: 201 Created
{
  "transfer_id": "unique_transfer_id",
  "sender_transaction_id": 123,
  "recipient_transaction_id": 124,
  "amount": 25.00,
  "sender_new_balance": 125.50,
  "recipient_new_balance": 75.00,
  "status": "completed"
}

Response: 400 Bad Request
{
  "error": "Insufficient balance",
  "current_balance": 10.00,
  "required_amount": 25.00
}

GET /transfer/{transfer_id}
Response: 200 OK
{
  "transfer_id": "unique_transfer_id",
  "sender_user_id": 1,
  "recipient_user_id": 2,
  "amount": 25.00,
  "description": "Payment for dinner",
  "status": "completed",
  "created_at": "2024-01-01T12:30:00Z"
}

Technical Specifications
Backend Stack
Framework: FastAPI
Database: Choose one - PostgreSQL, MySQL, SQLite, or MongoDB
ORM/ODM: SQLAlchemy (for SQL) or Motor/PyMongo (for MongoDB
Business Logic Requirements
1. Balance Management
User balance should always be calculated and updated correctly
Balance cannot go negative (validate before debit operations)
Balance updates should be atomic
2. Transaction Integrity
All transactions must be recorded with proper timestamps
Transfer operations must create two linked transactions (debit + credit)
Failed transfers should not partially update balances
3. Data Validation
Amounts must be positive and have max 2 decimal places
4. Error Handling
Handle insufficient balance scenarios
Handle invalid user IDs
Handle database connection errors
Return appropriate HTTP status codes
Sample Data
Sample Users
[
  {
    "username": "john_doe",
    "email": "john@example.com",
    "password": "password123",
    "phone_number": "+1234567890",
    "balance": 100.00
  },
  {
    "username": "jane_smith",
    "email": "jane@example.com",
    "password": "password456",
    "phone_number": "+1987654321",
    "balance": 50.00
  }
]

Sample Transactions
[
  {
    "user_id": 1,
    "transaction_type": "CREDIT",
    "amount": 100.00,
    "description": "Initial wallet load"
  },
  {
    "user_id": 1,
    "transaction_type": "TRANSFER_OUT",
    "amount": 25.00,
    "description": "Transfer to jane_smith",
    "recipient_user_id": 2
  }
]

Deliverables
FastAPI Backend with all specified endpoints
Database setup with sample data (5+ users, 20+ transactions)
API Documentation
README.md with setup and run instructions
Requirements.txt or pyproject.toml
Success Criteria
All API endpoints work as specified
Balance calculations are accurate
Money transfers work atomically
Transaction history displays correctly
Proper error handling and validation
Database operations are efficient
API documentation is accessible
Guidelines
No AI assistance for coding (ChatGPT, Claude, Gemini, etc.)
Tab completion and IntelliSense are allowed (Copilot tab suggestions, Cursor tab, IDE autocomplete)
No copy-pasting large code blocks from tutorials
No pre-built wallet/payment libraries
No Google Search, you can use the reference documentation
Turning off the proctoring will lead to disqualification
Reference Documentation
FastAPI Documentation
SQLAlchemy Documentation
Sqlite3
MongoDB
PyMongo
Motor Documentation
Pydantic Documentation
Submission
Create a repository at the start of the evaluation
Keep pushing the code every 30 minutes
