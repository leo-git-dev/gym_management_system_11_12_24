import matplotlib.pyplot as plt
from database.data_loader import DataLoader
from collections import defaultdict
from datetime import datetime

class RevenueAnalysis:
    @staticmethod
    def generate_revenue_report():
        # Load payment data
        payments = DataLoader.get_data("payments")

        if not payments:
            print("No payment data available for revenue analysis.")
            return

        # Process revenue data by month
        revenue_by_month = {}
        for payment in payments:
            month = payment["date"][:7]  # Extract YYYY-MM
            amount = float(payment["amount"])
            if month in revenue_by_month:
                revenue_by_month[month] += amount
            else:
                revenue_by_month[month] = amount

        # Sort revenue data by month
        sorted_revenue = sorted(revenue_by_month.items())

        # Generate bar chart
        months = [item[0] for item in sorted_revenue]
        revenue = [item[1] for item in sorted_revenue]

        plt.figure(figsize=(10, 6))
        plt.bar(months, revenue)
        plt.title("Revenue Analysis by Month")
        plt.xlabel("Month")
        plt.ylabel("Total Revenue ($)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("../gym_management_system/reports/revenue_report.png")
        plt.show()

        print("Revenue analysis report generated and saved as 'revenue_report.png'.")
