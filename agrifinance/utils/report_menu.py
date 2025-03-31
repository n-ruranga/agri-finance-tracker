# agrifinance/utils/report_menu.py
from datetime import datetime, date
from datetime import timedelta  
from agrifinance.services.report_service import ReportService
from agrifinance.models.report import TimePeriodReport

class ReportMenu:
    def __init__(self):
        self.service = ReportService()

    def display_menu(self):
        while True:
            print("\nReports")
            print("1. Generate Period Report")
            print("2. Generate Monthly Report")
            print("3. Generate Annual Report")
            print("4. Back to Main Menu")
            
            choice = input("Enter your choice: ")
            
            if choice == '1':
                self._generate_period_report()
            elif choice == '2':
                self._generate_monthly_report()
            elif choice == '3':
                self._generate_annual_report()
            elif choice == '4':
                break
            else:
                print("Invalid choice. Please try again.")

    def _generate_period_report(self):
        print("\nGenerate Custom Period Report")
        try:
            start_date_str = input("Enter start date (YYYY-MM-DD): ")
            end_date_str = input("Enter end date (YYYY-MM-DD): ")
            
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            
            report = self.service.generate_time_period_report(start_date, end_date)
            self._display_report(report)
        except ValueError as e:
            print(f"Error: {e}. Please enter valid dates in YYYY-MM-DD format.")

    def _generate_monthly_report(self):
        print("\nGenerate Monthly Report")
        try:
            year = int(input("Enter year: "))
            month = int(input("Enter month (1-12): "))
            
            start_date = date(year, month, 1)
            end_date = date(year, month + 1, 1) - timedelta(days=1) if month < 12 else date(year, 12, 31)
            
            report = self.service.generate_time_period_report(start_date, end_date)
            self._display_report(report)
        except ValueError as e:
            print(f"Error: {e}. Please enter valid year and month.")

    def _generate_annual_report(self):
        print("\nGenerate Annual Report")
        try:
            year = int(input("Enter year: "))
            reports = self.service.generate_annual_report(year)
            
            for month_name, report in reports.items():
                print(f"\n=== {month_name} {year} ===")
                self._display_report_summary(report.financial_summary)
        except ValueError as e:
            print(f"Error: {e}. Please enter a valid year.")

    def _display_report(self, report: TimePeriodReport):
        print(f"\n=== Financial Report: {report.start_date} to {report.end_date} ===")
        
        # Display financial summary
        self._display_report_summary(report.financial_summary)
        
        # Display income breakdown
        print("\nIncome by Source:")
        for item in report.income_by_category:
            print(f"- {item.category}: ${item.amount:.2f} ({item.percentage:.1f}%)")
        
        # Display expense breakdown
        print("\nExpenses by Category:")
        for item in report.expenses_by_category:
            print(f"- {item.category}: ${item.amount:.2f} ({item.percentage:.1f}%)")

    def _display_report_summary(self, summary):
        print("\nFinancial Summary:")
        print(f"- Total Income: ${summary.total_income:.2f}")
        print(f"- Total Expenses: ${summary.total_expenses:.2f}")
        print(f"- Net Profit: ${summary.net_profit:.2f}")
        print(f"- Active Loans: {summary.active_loans}")
        print(f"- Loan Payments Due: ${summary.loan_payments_due:.2f}")
