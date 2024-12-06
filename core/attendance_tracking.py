from utils.helpers import generate_unique_id
from database.data_loader import DataLoader


class AttendanceTracker:
    @staticmethod
    def record_attendance(member_id, class_id, date, time, workout_zone=None, equipment_used=None):
        """
        Record attendance for a member with details of workout zone and equipment used.
        """
        attendance_records = DataLoader.get_data("attendance")
        new_attendance_id = generate_unique_id(attendance_records, "attendance_id")

        new_record = {
            "attendance_id": str(new_attendance_id),
            "member_id": member_id,
            "class_id": class_id,
            "date": date,
            "time": time,
            "workout_zone": workout_zone or "General",
            "equipment_used": equipment_used or "None"
        }
        attendance_records.append(new_record)

        # Ensure the file includes all headers before saving
        DataLoader.save_data("attendance", attendance_records)

    @staticmethod
    def view_attendance_records():
        """
        View all attendance records with details of workout zones and equipment used.
        """
        attendance_records = DataLoader.get_data("attendance")
        for record in attendance_records:
            # Add default values for older records
            record.setdefault("workout_zone", "Unknown")
            record.setdefault("equipment_used", "None")
        return attendance_records
