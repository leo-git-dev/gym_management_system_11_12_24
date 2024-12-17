from unittest import TestCase
from unittest.mock import patch
from core.attendance_tracking import AttendanceManager

class TestAttendanceManager(TestCase):

    @patch("core.attendance_tracking.generate_unique_id")  # Corrected patch target
    @patch("database.data_loader.DataLoader.save_data")
    @patch("database.data_loader.DataLoader.get_data")
    def test_add_attendance(self, mock_get_data, mock_save_data, mock_generate_unique_id):
        # Mock data for attendance
        mock_attendance_records = []
        mock_get_data.return_value = mock_attendance_records

        # Mock generate_unique_id to return a valid ID
        mock_generate_unique_id.return_value = "001"

        # Call the method under test
        AttendanceManager.add_attendance("C001", "U123")

        # Verify the attendance record was added correctly
        self.assertEqual(len(mock_attendance_records), 1)
        self.assertEqual(mock_attendance_records[0]["attendance_id"], "A001")  # Prefix added in implementation
        self.assertEqual(mock_attendance_records[0]["class_id"], "C001")
        self.assertEqual(mock_attendance_records[0]["user_id"], "U123")
        self.assertIn("date", mock_attendance_records[0])
        self.assertIn("timestamp", mock_attendance_records[0])

        # Ensure save_data was called with the updated attendance records
        mock_save_data.assert_called_once_with("attendance", mock_attendance_records)


    @patch("database.data_loader.DataLoader.get_data")
    def test_get_attendance_by_class(self, mock_get_data):
        mock_attendance_records = [
            {"attendance_id": "A001", "class_id": "C001", "user_id": "U123", "date": "2024-06-01"},
            {"attendance_id": "A002", "class_id": "C002", "user_id": "U456", "date": "2024-06-02"},
        ]
        mock_get_data.return_value = mock_attendance_records

        # Retrieve attendance by class
        result = AttendanceManager.get_attendance_by_class("C001")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["attendance_id"], "A001")

    @patch("database.data_loader.DataLoader.get_data")
    def test_get_attendance_by_class_with_date(self, mock_get_data):
        mock_attendance_records = [
            {"attendance_id": "A001", "class_id": "C001", "user_id": "U123", "date": "2024-06-01"},
            {"attendance_id": "A002", "class_id": "C001", "user_id": "U456", "date": "2024-06-02"},
        ]
        mock_get_data.return_value = mock_attendance_records

        # Retrieve attendance by class and date
        result = AttendanceManager.get_attendance_by_class("C001", "2024-06-01")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["attendance_id"], "A001")

    @patch("database.data_loader.DataLoader.get_data")
    def test_get_attendance_by_user(self, mock_get_data):
        mock_attendance_records = [
            {"attendance_id": "A001", "class_id": "C001", "user_id": "U123", "date": "2024-06-01"},
            {"attendance_id": "A002", "class_id": "C002", "user_id": "U123", "date": "2024-06-02"},
        ]
        mock_get_data.return_value = mock_attendance_records

        # Retrieve attendance by user
        result = AttendanceManager.get_attendance_by_user("U123")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["attendance_id"], "A001")
        self.assertEqual(result[1]["attendance_id"], "A002")

    @patch("database.data_loader.DataLoader.get_data")
    def test_view_all_attendance(self, mock_get_data):
        mock_attendance_records = [
            {"attendance_id": "A001", "class_id": "C001", "user_id": "U123", "date": "2024-06-01"},
            {"attendance_id": "A002", "class_id": "C002", "user_id": "U456", "date": "2024-06-02"},
        ]
        mock_get_data.return_value = mock_attendance_records

        # Retrieve all attendance records
        result = AttendanceManager.view_all_attendance()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["attendance_id"], "A001")
        self.assertEqual(result[1]["attendance_id"], "A002")


if __name__ == "__main__":
    unittest.main()
