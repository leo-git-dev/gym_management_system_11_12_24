import csv
import os
import matplotlib.pyplot as plt
from database.data_loader import DataLoader

class AttendanceAnalysis:
    @staticmethod
    def generate_attendance_report():
        # Load attendance data
        attendance = DataLoader.get_data("attendance")

        if not attendance:
            print("No attendance data available for analysis.")
            return

        # Process attendance data by date
        attendance_by_date = {}
        for record in attendance:
            date = record["date"]
            if date in attendance_by_date:
                attendance_by_date[date] += 1
            else:
                attendance_by_date[date] = 1

        # Sort attendance data by date
        sorted_attendance = sorted(attendance_by_date.items())

        # Generate line chart
        dates = [item[0] for item in sorted_attendance]
        counts = [item[1] for item in sorted_attendance]

        plt.figure(figsize=(10, 6))
        plt.plot(dates, counts, marker='o')
        plt.title("Attendance Analysis by Date")
        plt.xlabel("Date")
        plt.ylabel("Attendance Count")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("../gym_management_system/reports/attendance_report.png")
        plt.show()

        print("Attendance analysis report generated and saved as 'attendance_report.png'.")
