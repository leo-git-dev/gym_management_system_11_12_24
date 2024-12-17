import unittest
from unittest.mock import patch, MagicMock
from core.member_management import MemberManagement


class TestMemberManagement(unittest.TestCase):

    @patch("database.data_loader.DataLoader.get_data")
    @patch("database.data_loader.DataLoader.save_data")
    @patch("utils.helpers.generate_unique_id")
    def test_add_member(self, mock_generate_unique_id, mock_save_data, mock_get_data):
        """
        Test that a new member is successfully added.
        """
        # Mock database responses based on key
        def mock_get_data_side_effect(key):
            if key == "members":
                return []
            elif key == "gyms":
                return [{"gym_id": "G1", "gym_name": "Gym A", "city": "New York"}]
            return []

        mock_get_data.side_effect = mock_get_data_side_effect
        mock_generate_unique_id.return_value = "123"  # Mocked unique ID

        MemberManagement.add_member(
            name="John Doe",
            user_type="Gym User",
            gym_id="G1",
            membership_type="Premium",
            cost=350,
            join_date="2024-06-01"
        )

        # Capture actual saved data
        saved_data = mock_save_data.call_args[0][1][0]

        # Verify the essential fields match
        self.assertEqual(saved_data["name"], "John Doe")
        self.assertEqual(saved_data["user_type"], "Gym User")
        self.assertEqual(saved_data["gym_id"], "G1")
        self.assertEqual(saved_data["gym_name"], "Gym A")
        self.assertEqual(saved_data["city"], "New York")
        self.assertEqual(saved_data["membership_type"], "Premium")
        self.assertEqual(saved_data["cost"], 350)
        self.assertEqual(saved_data["join_date"], "2024-06-01")

    @patch("database.data_loader.DataLoader.get_data")
    @patch("database.data_loader.DataLoader.save_data")
    def test_delete_member_by_id(self, mock_save_data, mock_get_data):
        """
        Test that a member is deleted by their ID.
        """
        def mock_get_data_side_effect(key):
            if key == "members":
                return [
                    {"member_id": "123", "name": "John Doe", "gym_id": "G1"},
                    {"member_id": "456", "name": "Jane Smith", "gym_id": "G2"},
                ]
            return []

        mock_get_data.side_effect = mock_get_data_side_effect

        result = MemberManagement.delete_member_by_id("123")
        self.assertTrue(result)
        mock_save_data.assert_called_once_with("members", [{"member_id": "456", "name": "Jane Smith", "gym_id": "G2"}])

    @patch("database.data_loader.DataLoader.get_data")
    @staticmethod
    def view_all_members():
        all_members = DataLoader.get_data("members")
        gyms = {g["gym_id"]: g for g in DataLoader.get_data("gyms")}

        # Filter out entries that are not actual members. For example:
        all_members = [m for m in all_members if "name" in m]

        # Enrich with gym data
        for member in all_members:
            gym = gyms.get(member.get("gym_id"))
            if gym:
                member["gym_name"] = gym.get("gym_name")
                member["manager_name"] = gym.get("manager_name")
                member["manager_contact"] = gym.get("manager_contact")
                member["manager_email"] = gym.get("manager_email")

        return all_members

    @patch("database.data_loader.DataLoader.get_data")
    def test_search_member_exact_case_insensitive(self, mock_get_data):
        """
        Test searching for a member by name (case insensitive).
        """
        def mock_get_data_side_effect(key):
            if key == "members":
                return [
                    {"member_id": "123", "name": "John Doe"},
                    {"member_id": "456", "name": "Jane Smith"},
                ]
            return []

        mock_get_data.side_effect = mock_get_data_side_effect

        result = MemberManagement.search_member_exact_case_insensitive("jane smith")
        self.assertIsNotNone(result)
        self.assertEqual(result["member_id"], "456")

    @patch("database.data_loader.DataLoader.get_data")
    def test_get_member_by_id(self, mock_get_data):
        """
        Test retrieving a member by ID.
        """
        def mock_get_data_side_effect(key):
            if key == "members":
                return [
                    {"member_id": "123", "name": "John Doe"},
                    {"member_id": "456", "name": "Jane Smith"},
                ]
            return []

        mock_get_data.side_effect = mock_get_data_side_effect

        result = MemberManagement.get_member_by_id("123")
        self.assertIsNotNone(result)
        self.assertEqual(result["name"], "John Doe")

        # Test for non-existent member
        result_none = MemberManagement.get_member_by_id("999")
        self.assertIsNone(result_none)

    @patch("database.data_loader.DataLoader.get_data")
    def test_count_users_by_gym(self, mock_get_data):
        """
        Test counting gym users for a specific gym.
        """
        def mock_get_data_side_effect(key):
            if key == "members":
                return [
                    {"member_id": "123", "gym_id": "G1", "user_type": "Gym User"},
                    {"member_id": "456", "gym_id": "G1", "user_type": "Gym User"},
                    {"member_id": "789", "gym_id": "G2", "user_type": "Wellbeing Staff"},
                ]
            return []

        mock_get_data.side_effect = mock_get_data_side_effect

        count = MemberManagement.count_users_by_gym("G1")
        self.assertEqual(count, 2)

    @patch("database.data_loader.DataLoader.get_data")
    def test_count_staff_by_gym(self, mock_get_data):
        """
        Test counting staff and their costs for a specific gym.
        """
        def mock_get_data_side_effect(key):
            if key == "members":
                return [
                    {"member_id": "123", "gym_id": "G1", "user_type": "Training Staff", "cost": 4000},
                    {"member_id": "456", "gym_id": "G1", "user_type": "Training Staff", "cost": 4500},
                    {"member_id": "789", "gym_id": "G2", "user_type": "Wellbeing Staff", "cost": 5000},
                ]
            return []

        mock_get_data.side_effect = mock_get_data_side_effect

        result = MemberManagement.count_staff_by_gym("G1", "Training")
        self.assertEqual(result["count"], 2)
        self.assertEqual(result["cost"], 8500)


if __name__ == "__main__":
    unittest.main()
