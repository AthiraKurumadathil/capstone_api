import pyodbc
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DATABASE_CONFIG = {
    'server': os.getenv('DATABASE_SERVER', 'localhost'),
    'database': os.getenv('DATABASE_NAME', 'your_database'),
    'user': os.getenv('DATABASE_USER', 'sa'),
    'password': os.getenv('DATABASE_PASSWORD', 'your_password')
}

def get_db_connection():
    """Create and return a database connection using pyodbc"""
    # Validate that credentials are set
    if DATABASE_CONFIG['server'] in ['localhost', None] or DATABASE_CONFIG['database'] == 'your_database':
        raise Exception(
            "Database configuration not set. Please set the following environment variables:\n"
            "DATABASE_SERVER, DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD\n"
            "Or create a .env file with these variables."
        )
    
    connection_string = (
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={DATABASE_CONFIG["server"]};'
        f'DATABASE={DATABASE_CONFIG["database"]};'
        f'UID={DATABASE_CONFIG["user"]};'
        f'PWD={DATABASE_CONFIG["password"]}'
    )
    conn = pyodbc.connect(connection_string)
    return conn
