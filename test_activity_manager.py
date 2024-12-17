# tests/test_class_activity_manager.py

import unittest
from unittest.mock import patch
from core.class_activity_manager import ClassActivityManager

class TestClassActivityManager(unittest.TestCase):
    @patch("core.class_activity_manager.DataLoader.save_data")
    @patch("core.class_activity_manager.MemberManagement.get_member_by_id")
    @patch("core.class_activity_manager.generate_unique_id")
    @patch("core.class_activity_manager.DataLoader.get_data")
    def test_add_class_successful(self, mock_get_data, mock_generate_unique_id, mock_get_member, mock_save_data):
        # Define separate data lists
        classes_data = []
        gyms_data = [{"gym_id": "G001", "gym_name": "Main Gym"}]

        # Define side_effect for get_data
        def mock_get_data_side_effect(key):
            if key == "classes":
                return classes_data
            elif key == "gyms":
                return gyms_data
            else:
                return []

        mock_get_data.side_effect = mock_get_data_side_effect

        # List to capture generate_unique_id call arguments
        generate_unique_id_calls = []

        # Define side_effect for generate_unique_id to capture arguments
        def generate_unique_id_side_effect(classes, field):
            # Capture the state of 'classes' at call time
            generate_unique_id_calls.append((classes.copy(), field))
            return "C001"

        mock_generate_unique_id.side_effect = generate_unique_id_side_effect

        # Mock trainer data
        mock_get_member.return_value = {
            "user_id": "T001",
            "name": "John Doe",
            "user_type": "Training Staff"
        }

        # Input data for adding a class
        class_name = "Yoga"
        trainer_id = "T001"
        schedule = {
            "Monday": ["10:00-11:00"],
            "Wednesday": ["14:00-15:00"]
        }
        capacity = 20
        gym_id = "G001"

        # Call the method under test
        new_class_id = ClassActivityManager.add_class(class_name, trainer_id, schedule, capacity, gym_id)

        # Assertions
        self.assertEqual(new_class_id, "C001")
        mock_get_data.assert_any_call("classes")
        mock_get_data.assert_any_call("gyms")
        self.assertEqual(len(generate_unique_id_calls), 1)
        self.assertEqual(generate_unique_id_calls[0], ([], "class_id"))
        mock_generate_unique_id.assert_called_once()
        mock_get_member.assert_called_once_with("T001")
        mock_save_data.assert_called_once()

        # Verify the saved data
        saved_classes = mock_save_data.call_args[0][1]
        self.assertEqual(len(saved_classes), 1)
        new_class = saved_classes[0]
        self.assertEqual(new_class["class_id"], "C001")
        self.assertEqual(new_class["class_name"], "Yoga")
        self.assertEqual(new_class["trainer_id"], "T001")
        self.assertEqual(new_class["trainer_name"], "John Doe")
        self.assertEqual(new_class["gym_id"], "G001")
        self.assertEqual(new_class["gym_name"], "Main Gym")
        self.assertEqual(new_class["schedule"], schedule)
        self.assertEqual(new_class["capacity"], capacity)
        self.assertEqual(new_class["registered_users"], [])

    @patch("core.class_activity_manager.DataLoader.get_data")
    def test_add_class_invalid_gym_id(self, mock_get_data):
        # Define separate data lists
        classes_data = []
        gyms_data = []  # Empty gyms list to simulate invalid gym_id

        # Define side_effect for get_data
        def mock_get_data_side_effect(key):
            if key == "classes":
                return classes_data
            elif key == "gyms":
                return gyms_data
            else:
                return []

        mock_get_data.side_effect = mock_get_data_side_effect

        # Input data for adding a class
        class_name = "Pilates"
        trainer_id = "T002"
        schedule = {
            "Tuesday": ["09:00-10:00"]
        }
        capacity = 15
        gym_id = "G999"  # Invalid gym_id

        # Call the method under test and assert exception
        with self.assertRaises(ValueError) as context:
            ClassActivityManager.add_class(class_name, trainer_id, schedule, capacity, gym_id)

        self.assertEqual(str(context.exception), "Invalid gym ID provided.")

    @patch("core.class_activity_manager.DataLoader.get_data")
    @patch("core.class_activity_manager.generate_unique_id")
    @patch("core.class_activity_manager.MemberManagement.get_member_by_id")
    def test_add_class_duplicate_class_name(self, mock_get_member, mock_generate_unique_id, mock_get_data):
        # Define separate data lists
        classes_data = [{
            "class_id": "C001",
            "class_name": "Zumba",
            "gym_id": "G001"
        }]
        gyms_data = [{"gym_id": "G001", "gym_name": "Main Gym"}]

        # Define side_effect for get_data
        def mock_get_data_side_effect(key):
            if key == "classes":
                return classes_data
            elif key == "gyms":
                return gyms_data
            else:
                return []

        mock_get_data.side_effect = mock_get_data_side_effect

        # Mock generate_unique_id
        mock_generate_unique_id.return_value = "C002"

        # Mock trainer data
        mock_get_member.return_value = {
            "user_id": "T003",
            "name": "Jane Smith",
            "user_type": "Training Staff"
        }

        # Input data for adding a duplicate class
        class_name = "Zumba"  # Duplicate
        trainer_id = "T003"
        schedule = {
            "Friday": ["16:00-17:00"]
        }
        capacity = 25
        gym_id = "G001"

        # Call the method under test and assert exception
        with self.assertRaises(ValueError) as context:
            ClassActivityManager.add_class(class_name, trainer_id, schedule, capacity, gym_id)

        self.assertEqual(str(context.exception), "A class named 'Zumba' already exists in the selected gym.")

    @patch("core.class_activity_manager.DataLoader.get_data")
    @patch("core.class_activity_manager.generate_unique_id")
    @patch("core.class_activity_manager.MemberManagement.get_member_by_id")
    def test_add_class_invalid_trainer(self, mock_get_member, mock_generate_unique_id, mock_get_data):
        # Define separate data lists
        classes_data = []
        gyms_data = [{"gym_id": "G002", "gym_name": "Secondary Gym"}]

        # Define side_effect for get_data
        def mock_get_data_side_effect(key):
            if key == "classes":
                return classes_data
            elif key == "gyms":
                return gyms_data
            else:
                return []

        mock_get_data.side_effect = mock_get_data_side_effect

        # Mock generate_unique_id
        mock_generate_unique_id.return_value = "C003"

        # Mock trainer data as invalid (non-training staff)
        mock_get_member.return_value = {
            "user_id": "T004",
            "name": "Bob Brown",
            "user_type": "Member"  # Not Training Staff
        }

        # Input data for adding a class with invalid trainer
        class_name = "HIIT"
        trainer_id = "T004"  # Invalid trainer
        schedule = {
            "Thursday": ["18:00-19:00"]
        }
        capacity = 30
        gym_id = "G002"

        # Call the method under test and assert exception
        with self.assertRaises(ValueError) as context:
            ClassActivityManager.add_class(class_name, trainer_id, schedule, capacity, gym_id)

        self.assertEqual(str(context.exception), "Invalid trainer selected.")

    @patch("core.class_activity_manager.DataLoader.get_data")
    @patch("core.class_activity_manager.generate_unique_id")
    @patch("core.class_activity_manager.MemberManagement.get_member_by_id")
    def test_add_class_invalid_capacity(self, mock_get_member, mock_generate_unique_id, mock_get_data):
        # Define separate data lists
        classes_data = []
        gyms_data = [{"gym_id": "G003", "gym_name": "Fitness Center"}]

        # Define side_effect for get_data
        def mock_get_data_side_effect(key):
            if key == "classes":
                return classes_data
            elif key == "gyms":
                return gyms_data
            else:
                return []

        mock_get_data.side_effect = mock_get_data_side_effect

        # Mock generate_unique_id
        mock_generate_unique_id.return_value = "C004"

        # Mock trainer data
        mock_get_member.return_value = {
            "user_id": "T005",
            "name": "Alice Green",
            "user_type": "Training Staff"
        }

        # Input data for adding a class with invalid capacity
        class_name = "CrossFit"
        trainer_id = "T005"
        schedule = {
            "Sunday": ["08:00-09:00"]
        }
        capacity = -5  # Invalid capacity
        gym_id = "G003"

        # Call the method under test and assert exception
        with self.assertRaises(ValueError) as context:
            ClassActivityManager.add_class(class_name, trainer_id, schedule, capacity, gym_id)

        self.assertEqual(str(context.exception), "Capacity must be a positive integer.")

if __name__ == '__main__':
    unittest.main()

