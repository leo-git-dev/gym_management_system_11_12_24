import matplotlib.pyplot as plt
from database.data_loader import DataLoader
from datetime import datetime
from collections import Counter

class MembershipGrowthReport:
    @staticmethod
    def generate_growth_chart(output_file="membership_growth.png"):
        members = DataLoader.get_data("members")
        join_dates = [datetime.strptime(member["join_date"], "%Y-%m-%d").date() for member in members]
        join_dates.sort()

        monthly_counts = Counter(date.strftime("%Y-%m") for date in join_dates)
        months = sorted(monthly_counts.keys())
        counts = [monthly_counts[month] for month in months]

        plt.figure(figsize=(10, 6))
        plt.plot(months, counts, marker="o")
        plt.xlabel("Month")
        plt.ylabel("New Members")
        plt.title("Membership Growth Over Time")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(output_file)
        return output_file
