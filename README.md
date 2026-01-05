# Organization API

A FastAPI application for managing organizations with CRUD operations.

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Database Connection
Edit the `.env` file with your SQL Server credentials:
```env
DATABASE_SERVER=your_server_name
DATABASE_NAME=your_database_name
DATABASE_USER=your_username
DATABASE_PASSWORD=your_password
DATABASE_DRIVER=ODBC Driver 17 for SQL Server
```

### 3. Run the Application
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Documentation

Interactive API documentation is available at `http://localhost:8000/docs`

## Endpoints

### Create Organization
- **POST** `/organizations`
- Request body:
```json
{
  "name": "Company Name",
  "address": "123 Main St",
  "city": "New York",
  "zip": "10001",
  "state": "NY",
  "phone": "555-0123",
  "email": "info@company.com",
  "active": true
}
```

### Get All Organizations
- **GET** `/organizations`
- Returns a list of all organizations

### Get Organization by ID
- **GET** `/organizations/{org_id}`
- Returns a single organization

### Update Organization
- **PUT** `/organizations/{org_id}`
- Request body (all fields optional):
```json
{
  "name": "Updated Name",
  "email": "newemail@company.com"
}
```

### Delete Organization
- **DELETE** `/organizations/{org_id}`
- Returns 204 No Content on success

### Health Check
- **GET** `/health`
- Returns API status

## Prerequisites

- Python 3.8+
- SQL Server
- ODBC Driver 17 for SQL Server (install from Microsoft)

## Project Structure

```
capstone_api/
├── main.py           # FastAPI application and endpoints
├── models.py         # Pydantic data models
├── crud.py           # Database operations
├── database.py       # Database connection
├── requirements.txt  # Project dependencies
├── .env              # Environment variables (configure this)
└── README.md         # This file
```
