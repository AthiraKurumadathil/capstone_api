# Capstone API - Activity Management System

A FastAPI application for managing organizations, activities, trainers, students, batches, and enrollments.

## Prerequisites

- **Python 3.12** or higher
- **SQL Server Express** or Developer Edition
- **SQL Server Management Studio (SSMS)**
- **Git**

## Local Setup Instructions

### Step 1: Clone the Repository
```bash
git clone https://github.com/AthiraKurumadathil/capstone_api.git
cd capstone_api
```

### Step 2: Install Python 3.12 or Higher
Download and install Python 3.12 or higher from [python.org](https://www.python.org/downloads/)

Verify installation:
```bash
python --version
```

### Step 3: Create Virtual Environment
Create the virtual environment in the project root directory:
```bash
python -m venv .venv
```

### Step 4: Activate Virtual Environment

**On Windows:**
```bash
.venv\Scripts\activate
```

**On macOS/Linux:**
```bash
source .venv/bin/activate
```

### Step 5: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 6: Configure Environment Variables
Create a `.env` file in the project root directory and add the following configuration:

```env
# Database Configuration
DATABASE_SERVER=.\
DATABASE_NAME=ActivityDB
DATABASE_USER=SQl User
DATABASE_PASSWORD= SQL Password

# Email SMTP Configuration
GMAIL_ADDRESS="Your email"
GMAIL_PASSWORD="Your google app password"
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_SENDER_NAME=Activity Management System

# Application Configuration
BASE_APP_URL=http://localhost:3000
```

**Note:** Replace the email credentials and database password with your actual values.

### Step 7: Install SQL Server
Download and install **SQL Server Express** or **Developer Edition** from [Microsoft SQL Server Downloads](https://www.microsoft.com/en-us/sql-server/sql-server-downloads)

### Step 8: Install SQL Server Management Studio (SSMS)
Download and install SSMS from [Microsoft SSMS Download](https://learn.microsoft.com/en-us/sql/ssms/download-sql-server-management-studio-ssms)

### Step 9: Create Database and Run Scripts
1. Open **SQL Server Management Studio**
2. Connect to your SQL Server instance
3. Create a new database named `ActivityDB`
4. Open the database script from `dbscript/dbscript.sql`
5. Execute the script to create all required tables

### Step 10: Start the API Server
```bash
python -m uvicorn main:app --reload
```

The API will be available at: `http://localhost:8000`

## API Documentation

Interactive API documentation is available at: `http://localhost:8000/docs`

## Project Structure

```
capstone_api/
├── main.py                      # FastAPI application entry point
├── .env                         # Environment variables (configure this)
├── requirements.txt             # Project dependencies
├── README.md                    # This file
├── model/                       # Pydantic data models
│   ├── usermodel.py
│   ├── organizationmodel.py
│   ├── activitymodel.py
│   ├── trainermodel.py
│   ├── studentmodel.py
│   ├── batchmodel.py
│   ├── enrollmentmodel.py
│   └── ...
├── services/                    # Database CRUD operations
│   ├── usercrud.py
│   ├── orgcrud.py
│   ├── activitycrud.py
│   ├── trainercrud.py
│   ├── studentcrud.py
│   └── ...
├── utils/                       # Utility modules
│   ├── database.py             # Database connection
│   ├── auth.py                 # JWT authentication
│   ├── email_helper.py         # Email sending functionality
│   ├── password_helper.py      # Password hashing and generation
│   └── validation_helper.py    # Input validation
├── dbscript/                    # Database scripts
│   └── dbscript.sql            # SQL Server initialization script
└── __pycache__/                 # Python cache (auto-generated)
```

## Features

- **User Management** - Create users with auto-generated passwords
- **Authentication** - JWT-based authentication
- **Password Management** - Change password and forgot password functionality
- **Email Notifications** - Welcome emails, password reset emails
- **Organization Management** - Manage organizations
- **Activity Tracking** - Track activities and activity trainers
- **Student Management** - Manage student enrollments
- **Batch Management** - Manage training batches and sessions
- **Attendance Tracking** - Track student attendance
- **Invoice & Payment Management** - Manage fees, invoices, and payments

## API Endpoints Overview

### Authentication
- `POST /users/authenticate/login` - User login
- `POST /users/forgot-password` - Request password reset
- `PUT /users/change-password/{email}` - Change password

### Users
- `POST /users` - Create new user
- `GET /users` - Get all users
- `GET /users/{user_id}` - Get user by ID
- `GET /users/email/{email}` - Get user by email
- `PUT /users/{user_id}` - Update user
- `DELETE /users/{user_id}` - Delete user

### Organizations
- `POST /organizations` - Create organization
- `GET /organizations` - Get all organizations
- `GET /organizations/{org_id}` - Get organization by ID
- `PUT /organizations/{org_id}` - Update organization
- `DELETE /organizations/{org_id}` - Delete organization

### And many more endpoints for activities, trainers, students, batches, enrollments, etc.

## Troubleshooting

### Database Connection Issues
- Ensure SQL Server is running
- Verify database credentials in `.env` file
- Check DATABASE_SERVER format (use `.\` for local instance)

### Port Already in Use
If port 8000 is already in use, specify a different port:
```bash
python -m uvicorn main:app --reload --port 8001
```

### Email Configuration Issues
- Verify GMAIL_ADDRESS and GMAIL_PASSWORD in `.env`
- Ensure Gmail account has "App Passwords" enabled
- Check SMTP_SERVER and SMTP_PORT settings

## Support

For issues or questions, please refer to the project repository or contact the development team.
