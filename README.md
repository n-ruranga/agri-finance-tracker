AgriFinance Tracker
Overview
AgriFinance Tracker is a command-line application designed to help small-scale farmers and agricultural businesses manage their finances. The application allows users to track income, expenses, loans, and generate financial reports to gain better insights into their agricultural operations.

Features
Income Management: Track income from various sources (crop sales, livestock, etc.)

Expense Management: Record and categorize farming expenses

Loan Management: Monitor agricultural loans and repayment schedules

Financial Reports: Generate summaries and insights about farm finances

Prerequisites
Before installing AgriFinance Tracker, ensure you have the following:

Python 3.8 or higher

MySQL Server 8.0 or higher

pip (Python package manager)

Installation
1. Clone the Repository
bash
Copy
git clone https://github.com/yourusername/agrifinance-tracker.git
cd agrifinance-tracker
2. Set Up Virtual Environment (Recommended)
bash
Copy
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
3. Install Dependencies
bash
Copy
pip install -r requirements.txt
4. Database Setup
Create a MySQL database for the application:

sql
Copy
CREATE DATABASE agrifinance_tracker;
Create a .env file in the project root with your database credentials:

ini
Copy
DB_HOST=localhost
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_NAME=agrifinance_tracker
Running the Application
To start the AgriFinance Tracker:

bash
Copy
python -m agrifinance.main
Usage
Main Menu
When you launch the application, you'll see the main menu:

Copy
Welcome to AgriFinance Tracker

Main Menu
1. Income Management
2. Expense Management
3. Loan Management
4. Reports
5. Exit
Navigating the Application
Use the number keys to select a menu option

Follow the on-screen prompts to enter information

Use the "Back" or "Exit" options to return to previous menus

Testing
To run the test suite:

bash
Copy
pytest tests/
Troubleshooting
Common Issues
Database Connection Errors:

Verify your MySQL server is running

Check your .env file for correct credentials

Ensure the database agrifinance_tracker exists

Module Not Found Errors:

Ensure you're in the virtual environment

Verify all dependencies are installed (pip install -r requirements.txt)

Date Format Errors:

Always enter dates in YYYY-MM-DD format (e.g., 2023-10-15)

Contributing
We welcome contributions! Please follow these steps:

Fork the repository

Create a feature branch (git checkout -b feature/your-feature)

Commit your changes (git commit -am 'Add some feature')

Push to the branch (git push origin feature/your-feature)

Create a new Pull Request

License
This project is licensed under the Aether Group.

Support
For support or questions, please contact n.ruranga@alustudent.com or open an issue on GitHub.