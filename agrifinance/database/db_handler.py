# agrifinance/database/db_handler.py
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

class DBHandler:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DBHandler, cls).__new__(cls)
            cls._instance._initialize_db()
        return cls._instance

    def _initialize_db(self):
        try:
            self.connection = mysql.connector.connect(
                host=os.getenv('DB_HOST'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                database=os.getenv('DB_NAME')
            )
            self._create_tables()
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            raise

    def _create_tables(self):
        cursor = self.connection.cursor()
        
        # Income table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS income (
            id INT AUTO_INCREMENT PRIMARY KEY,
            amount DECIMAL(10, 2) NOT NULL,
            source VARCHAR(255) NOT NULL,
            date DATE NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            updated_at ON UPDATE TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Expense table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS expense (
            id INT AUTO_INCREMENT PRIMARY KEY,
            amount DECIMAL(10, 2) NOT NULL,
            category VARCHAR(255) NOT NULL,
            date DATE NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            updated_at ON UPDATE TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Loan table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS loan (
            id INT AUTO_INCREMENT PRIMARY KEY,
            amount DECIMAL(10, 2) NOT NULL,
            interest_rate DECIMAL(5, 2) NOT NULL,
            term_months INT NOT NULL,
            lender VARCHAR(255) NOT NULL,
            date_issued DATE NOT NULL,
            status VARCHAR(50) DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            updated_at ON UPDATE TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        self.connection.commit()
        cursor.close()

    def get_cursor(self):
        return self.connection.cursor(dictionary=True)

    def commit(self):
        self.connection.commit()

    def close(self):
        if self.connection.is_connected():
            self.connection.close()