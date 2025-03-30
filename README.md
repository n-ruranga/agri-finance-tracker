Here's a comprehensive **README.md** file for your AgriFinance Tracker application, including setup instructions for XAMPP/MySQL, Python environment configuration, and troubleshooting:

```markdown
# AgriFinance Tracker

![AgriFinance Logo](https://via.placeholder.com/150x50?text=AgriFinance+Tracker)  
*A command-line application for managing agricultural finances*

## Features

- 📊 **Income Tracking**: Record crop sales, livestock income, and other revenue
- 💰 **Expense Management**: Log farming inputs, equipment costs, and labor expenses
- 🏦 **Loan Monitoring**: Track agricultural loans and repayment schedules
- 📈 **Financial Reports**: Generate profit/loss statements and cash flow analysis

## Prerequisites

- 🐍 Python 3.8+
- ⚙️ XAMPP with MySQL (or standalone MySQL Server)
- 📦 pip package manager

## Installation Guide

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/agrifinance-tracker.git
cd agrifinance-tracker
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup (Using XAMPP)

1. Start XAMPP Control Panel
2. Start **Apache** and **MySQL** services
3. Create database:
   ```bash
   mysql -u root -h localhost -e "CREATE DATABASE agrifinance_tracker;"
   ```
   (No password required by default in XAMPP)

### 5. Configuration
Create `.env` file in project root:
```ini
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=agrifinance_tracker
```

## Running the Application

```bash
python -m agrifinance.main
```

## Testing

Run all tests:
```bash
pytest tests/
```

Run specific test module:
```bash
pytest tests/test_income.py -v
```

## Troubleshooting

### Common Issues

1. **MySQL Connection Errors**:
   - Verify XAMPP's MySQL is running
   - Check `.env` file credentials
   - Try adding `port=3306` to `.env`

2. **Python Package Errors**:
   ```bash
   pip install --force-reinstall -r requirements.txt
   ```

3. **Permission Errors on Windows**:
   - Run Command Prompt as Administrator
   - Add Python to PATH: `set PATH=%PATH%;C:\Python312\Scripts`

4. **pytest Installation Issues**:
   ```bash
   python -m pip install --user --ignore-installed pytest
   ```

## Project Structure

```
agrifinance_tracker/
├── agrifinance/          # Core application
│   ├── models/           # Data models
│   ├── services/         # Business logic
│   ├── database/         # DB connection
│   └── utils/            # Helpers
├── tests/                # Test cases
├── requirements.txt      # Dependencies
└── .env                  # Configuration
```

