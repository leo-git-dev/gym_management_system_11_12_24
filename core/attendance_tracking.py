# core/attendance_manager.py

from utils.helpers import generate_unique_id
from database.data_loader import DataLoader
from datetime import datetime


class AttendanceManager:
    @staticmethod
    def add_attendance(class_id, user_id, date=None):
        """
        Add a new attendance record.

        :param class_id: ID of the class.
        :param user_id: ID of the gym user.
        :param date: Date of the class session in 'YYYY-MM-DD' format. Defaults to today.
        """
        attendance_records = DataLoader.get_data("attendance")

        # Generate unique attendance_id
        new_attendance_num = generate_unique_id(attendance_records, "attendance_id", prefix='A')
        new_attendance_id = f"A{new_attendance_num}"

        # If date not provided, use today's date
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")

        # Current timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")

        new_record = {
            "attendance_id": new_attendance_id,
            "class_id": class_id,
            "user_id": user_id,
            "date": date,
            "timestamp": timestamp
        }

        attendance_records.append(new_record)
        DataLoader.save_data("attendance", attendance_records)
        print(f"Attendance recorded: {new_record}")

    @staticmethod
    def get_attendance_by_class(class_id, date=None):
        """
        Retrieve attendance records for a specific class and date.

        :param class_id: ID of the class.
        :param date: Date in 'YYYY-MM-DD' format. If None, retrieves all dates.
        :return: List of attendance records.
        """
        attendance_records = DataLoader.get_data("attendance")
        if date:
            filtered = [record for record in attendance_records if
                        record["class_id"] == class_id and record["date"] == date]
        else:
            filtered = [record for record in attendance_records if record["class_id"] == class_id]
        return filtered

    @staticmethod
    def get_attendance_by_user(user_id, date=None):
        """
        Retrieve attendance records for a specific user and date.

        :param user_id: ID of the gym user.
        :param date: Date in 'YYYY-MM-DD' format. If None, retrieves all dates.
        :return: List of attendance records.
        """
        attendance_records = DataLoader.get_data("attendance")
        if date:
            filtered = [record for record in attendance_records if
                        record["user_id"] == user_id and record["date"] == date]
        else:
            filtered = [record for record in attendance_records if record["user_id"] == user_id]
        return filtered

    @staticmethod
    def view_all_attendance():
        """
        Retrieve all attendance records.

        :return: List of all attendance records.
        """
        return DataLoader.get_data("attendance")
