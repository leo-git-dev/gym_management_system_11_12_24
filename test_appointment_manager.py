import unittest
from unittest.mock import patch, MagicMock
from core.appointments import AppointmentManager


class TestAppointmentManager(unittest.TestCase):
    @patch("database.data_loader.DataLoader.get_data")
    @patch("database.data_loader.DataLoader.save_data")
    @patch("utils.helpers.generate_unique_id")
    def test_schedule_appointment(self, mock_generate_unique_id, mock_save_data, mock_get_data):
        mock_get_data.return_value = []
        mock_generate_unique_id.return_value = "bb0e99ec"

        AppointmentManager.schedule_appointment(
            member_id="M1",
            trainer_id="T1",
            date="2024-12-20",
            time="10:00",
            cost=100.0,
            status="Confirmed"
        )

        mock_save_data.assert_called_once()
        saved_appointment = mock_save_data.call_args[0][1][0]
        self.assertEqual(saved_appointment["member_id"], "M1")
        self.assertEqual(saved_appointment["trainer_id"], "T1")
        self.assertEqual(saved_appointment["date"], "2024-12-20")
        self.assertEqual(saved_appointment["time"], "10:00")
        self.assertEqual(saved_appointment["cost"], 100.0)
        self.assertEqual(saved_appointment["status"], "Confirmed")

    @patch("database.data_loader.DataLoader.get_data")
    @patch("core.member_management.MemberManagement.view_all_members")
    @patch("core.gym_management.GymManager.view_all_gyms")
    def test_view_all_appointments_enriched(self, mock_view_all_gyms, mock_view_all_members, mock_get_data):
        mock_get_data.return_value = [
            {"appointment_id": "1", "member_id": "M1", "trainer_id": "T1", "date": "2024-12-20", "time": "10:00"}
        ]
        mock_view_all_members.return_value = [
            {"member_id": "M1", "name": "John Doe", "user_type": "Gym User"},
            {"member_id": "T1", "name": "Jane Smith", "user_type": "Wellbeing Staff", "activity": "Yoga"}
        ]
        mock_view_all_gyms.return_value = [
            {"gym_id": "G1", "gym_name": "Fitness Center"}
        ]

        enriched_appointments = AppointmentManager.view_all_appointments_enriched()
        self.assertEqual(len(enriched_appointments), 1)
        self.assertEqual(enriched_appointments[0]["wellbeing_staff_name"], "Jane Smith")
        self.assertEqual(enriched_appointments[0]["specialty"], "Yoga")
        self.assertEqual(enriched_appointments[0]["gym_user_name"], "John Doe")
        self.assertEqual(enriched_appointments[0]["gym_name"], "Unknown")  # No gym_id linked to trainer

    # Remaining tests remain unchanged


if __name__ == "__main__":
    unittest.main()
