from utils.helpers import generate_unique_id
from database.data_loader import DataLoader
from core.gym_management import GymManager
import os
import logging

# Ensure log directory exists
log_directory = 'logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Configure logging
logging.basicConfig(
    filename=os.path.join(log_directory, 'class_activity_manager.log'),
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Initialize logger
logger = logging.getLogger(__name__)



class MemberManagement:
    @staticmethod
    def add_member(name, user_type, gym_id, **kwargs):
        """
        Add a new member to the gym with specific roles and schedules.
        :param name: Name of the member.
        :param user_type: Type of user (e.g., Gym User, Training Staff, etc.).
        :param gym_id: ID of the gym.
        :param kwargs: Additional arguments like membership_type, cost, activities, schedule, role, or join_date.
        """
        members = DataLoader.get_data("members")
        gyms = DataLoader.get_data("gyms")

        # Verify gym_id exists
        gym = next((g for g in gyms if g["gym_id"] == gym_id), None)
        if not gym:
            raise ValueError("Invalid gym ID provided.")

        # Generate a unique member ID
        new_member_id = generate_unique_id(members, "member_id")

        # Base structure for a new member
        new_member = {
            "member_id": str(new_member_id),
            "name": name,
            "user_type": user_type,
            "gym_id": gym_id,
            "gym_name": gym["gym_name"],
            "city": gym["city"],
            "membership_type": kwargs.get("membership_type", "N/A"),
            "cost": kwargs.get("cost", 0),
            "join_date": kwargs.get("join_date", "N/A"),
            "schedule": kwargs.get("schedule", {}),
            "activity": kwargs.get("activity", "N/A"),
            "expertise": kwargs.get("expertise", "N/A"),
            "role": kwargs.get("role", "N/A"),
        }

        # Additional handling for specific user types
        if user_type == "Training Staff":
            new_member["expertise"] = kwargs.get("expertise", "General")
            new_member["schedule"] = MemberManagement.validate_schedule(kwargs.get("schedule", {}))
            new_member["cost"] = 4000

        elif user_type == "Wellbeing Staff":
            new_member["activity"] = kwargs.get("activity", "General")
            new_member["schedule"] = MemberManagement.validate_schedule(kwargs.get("schedule", {}))
            new_member["cost"] = 4500

        elif user_type == "Management Staff":
            new_member["role"] = kwargs.get("role", "Unknown")
            new_member["cost"] = 2500

        members.append(new_member)
        DataLoader.save_data("members", members)
        print(f"Member added successfully with ID: {new_member_id}.")

    @staticmethod
    def validate_schedule(schedule):
        """
        Validate the new schedule format:
        schedule = {
          "Monday": [{"start_time": "07:00", "end_time": "10:30"}],
          "Tuesday": [],
          ...
        }
        """
        if not isinstance(schedule, dict):
            raise ValueError("Schedule must be a dictionary.")

        # Validate each day's intervals
        for day, intervals in schedule.items():
            if not isinstance(intervals, list):
                raise ValueError(f"Expected a list of intervals for {day}.")
            for interval in intervals:
                if "start_time" not in interval or "end_time" not in interval:
                    raise ValueError(f"Interval missing start_time or end_time for {day}.")

                start = interval["start_time"]
                end = interval["end_time"]

                # Basic validation: ensure HH:MM format
                if not (MemberManagement.is_valid_time_format(start) and MemberManagement.is_valid_time_format(end)):
                    raise ValueError(f"Invalid time format in schedule for {day}: {start}-{end}.")

                # Check times order
                if end <= start:
                    raise ValueError(f"End time must be later than start time for {day}: {start}-{end}")

        return schedule

    @staticmethod
    def is_valid_time_format(t):
        # Simple check for HH:MM format
        import re
        return bool(re.match(r"^\d{2}:\d{2}$", t))

    @staticmethod
    def delete_member_by_id(member_id):
        """
        Delete a member from the database by ID.
        """
        members = DataLoader.get_data("members")
        updated_members = [m for m in members if m["member_id"] != member_id]
        if len(updated_members) < len(members):
            DataLoader.save_data("members", updated_members)
            print(f"Member ID {member_id} deleted successfully.")
            return True
        print(f"Member ID {member_id} not found.")
        return False

    @staticmethod
    def delete_member_by_name(name):
        """
        Delete a member from the database by their name.
        :param name: The name of the member to delete.
        :return: True if the member was deleted, False otherwise.
        """
        try:
            members = DataLoader.get_data("members")
            # Find the member by name (case-insensitive)
            updated_members = [m for m in members if m.get("name", "").lower() != name.lower()]

            if len(updated_members) < len(members):
                DataLoader.save_data("members", updated_members)
                print(f"Member with name '{name}' deleted successfully.")
                return True

            print(f"Member with name '{name}' not found.")
            return False
        except Exception as e:
            print(f"Error deleting member by name: {e}")
            return False

    @staticmethod
    def view_all_members():
        """
        Retrieve all members from the database.
        """
        members = DataLoader.get_data("members")
        # Enrich members with gym_name based on gym_id
        gyms = GymManager.view_all_gyms()
        gym_dict = {gym["gym_id"]: gym["gym_name"] for gym in gyms}
        for member in members:
            member["gym_name"] = gym_dict.get(member.get("gym_id"), "Unknown")
        return members

    @staticmethod
    def search_member_exact_case_insensitive(name):
        """
        Search for a member by exact name (case-insensitive).

        :param name: The exact name of the member to search for.
        :return: Member dictionary or None if not found.
        """
        members = DataLoader.get_data("members")
        return next((m for m in members if m["name"].strip().lower() == name.strip().lower()), None)

    @staticmethod
    def get_member_by_id(member_id):
        """
        Retrieve member details by member_id.

        :param member_id: ID of the member.
        :return: Member dictionary or None.
        """
        try:
            members = DataLoader.get_data("members")
            member = next((m for m in members if m["member_id"] == member_id), None)
            if member:
                logger.debug(f"Member found: {member}")
            else:
                logger.debug(f"No member found with member_id: {member_id}")
            return member
        except Exception as e:
            logger.error(f"Error retrieving member by ID '{member_id}': {e}")
            raise


    @staticmethod
    def get_all_member_ids():
        """
        Retrieve all member IDs from the database.
        """
        try:
            members = MemberManagement.view_all_members()
            return [member.get("member_id") for member in members if member.get("member_id")]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch member IDs: {e}")
            return []

    @staticmethod
    def get_all_member_names():
        """
        Retrieve all member names from the database.
        """
        try:
            members = MemberManagement.view_all_members()
            return [member.get("name") for member in members if member.get("name")]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch member names: {e}")
            return []

    @staticmethod
    def search_member(member_id=None, name=None):
        """
        Search for a member by ID or name.
        :param member_id: The ID of the member to search for.
        :param name: The name of the member to search for.
        :return: The member's details if found, otherwise None.
        """
        members = DataLoader.get_data("members")
        if member_id:
            return next((m for m in members if m["member_id"] == member_id), None)
        elif name:
            return next((m for m in members if m["name"].lower() == name.lower()), None)
        return None

    @staticmethod
    def update_member(member_id, updates):
        """
        Update multiple fields of a member's details.
        """
        members = DataLoader.get_data("members")
        member = next((m for m in members if m["member_id"] == member_id), None)

        if not member:
            raise ValueError(f"Member ID {member_id} not found.")

        # Debugging: Print the current state before updates
        print(f"Current Member Data: {member}")
        print(f"Requested Updates: {updates}")

        # Validate and apply updates
        valid_fields = set(member.keys())
        for field, new_value in updates.items():
            if field in valid_fields:
                member[field] = new_value
            else:
                raise ValueError(f"Invalid field '{field}' for member updates.")

        DataLoader.save_data("members", members)
        print(f"Member ID {member_id} updated successfully with changes: {updates}")
        return True

    @staticmethod
    def calculate_membership_cost(membership_type):
        """
        Calculate the cost of the membership based on the type.
        :param membership_type: The type of membership.
        :return: Cost of the membership.
        """
        membership_costs = {
            "Trial": 10,
            "Standard": 200,
            "Weekender": 80,
            "Premium": 350,
        }
        return membership_costs.get(membership_type, 0)


    @staticmethod
    def count_users_by_gym(gym_id):
        """
        Count the total number of gym users for a specific gym.
        :param gym_id: The ID of the gym.
        :return: Total number of gym users for the gym.
        """
        members = DataLoader.get_data("members")  # Load all members from the database
        return sum(1 for member in members if member["gym_id"] == gym_id and member["user_type"] == "Gym User")

    @staticmethod
    def count_staff_by_gym(gym_id, staff_type):
        """
        Count the total number of staff and their associated costs by type for a specific gym.
        :param gym_id: The gym ID.
        :param staff_type: The type of staff ("Wellbeing", "Training", or "Management").
        :return: A dictionary with 'count' and 'cost'.
        """
        members = DataLoader.get_data("members")
        staff = [
            member for member in members
            if member["gym_id"] == gym_id and member["user_type"] == f"{staff_type} Staff"
        ]
        total_cost = sum(member.get("cost", 0) for member in staff)
        return {"count": len(staff), "cost": total_cost}

    @staticmethod
    def calculate_staff_totals_by_gym(gym_id):
        members = DataLoader.get_data("members")
        staff_totals = {
            "Wellbeing Staff": {"count": 0, "cost": 0.0},
            "Training Staff": {"count": 0, "cost": 0.0},
            "Management Staff": {"count": 0, "cost": 0.0},
        }

        for member in members:
            if member["gym_id"] == gym_id and member["user_type"] in staff_totals:
                user_type = member["user_type"]
                staff_totals[user_type]["count"] += 1
                staff_totals[user_type]["cost"] += float(member.get("cost", 0))

        return staff_totals