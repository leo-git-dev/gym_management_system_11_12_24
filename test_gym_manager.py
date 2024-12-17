import unittest
from unittest.mock import patch, MagicMock
from database.data_loader import DataLoader
from core.member_management import MemberManagement  # Or GymManager, depending on your setup

class TestViewAllMembers(unittest.TestCase):

    @staticmethod
    def view_all_members():
        members = DataLoader.get_data("members")
        gyms = DataLoader.get_data("gyms")

        # Map gym_id to gym details for easy lookup
        gym_details = {gym["gym_id"]: gym for gym in gyms}

        # Filter out non-member entries (entries without 'name') and enrich with gym data
        valid_members = [
            {
                **member,
                "gym_name": gym_details[member["gym_id"]]["gym_name"],
                "manager_name": gym_details[member["gym_id"]]["manager_name"],
                "manager_contact": gym_details[member["gym_id"]]["manager_contact"],
                "manager_email": gym_details[member["gym_id"]]["manager_email"],
            }
            for member in members
            if "name" in member  # Filter condition
        ]

        return valid_members


if __name__ == "__main__":
    unittest.main()
