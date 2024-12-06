from utils.helpers import generate_unique_id
from database.data_loader import DataLoader


class MemberManagement:
    @staticmethod
    def add_member(name, membership_type, join_date):
        members = DataLoader.get_data("members")
        gyms = DataLoader.get_data("gyms")  # Fetch gym data

        # Display available gyms
        print("\nAvailable Gyms:")
        for gym in gyms:
            print(f"Gym ID: {gym['gym_id']}, Name: {gym['gym_name']}, Location: {gym['city']}")

        # Prompt for gym ID
        gym_id = input("\nEnter the Gym ID for the new member: ")
        gym = next((g for g in gyms if g["gym_id"] == gym_id), None)

        if not gym:
            print("Error: Invalid Gym ID. Member not added.")
            return

        # Generate a new unique Member ID
        new_member_id = generate_unique_id(members, "member_id")

        # Create the new member record
        new_member = {
            "member_id": str(new_member_id),
            "name": name,
            "membership_type": membership_type,
            "join_date": join_date,
            "gym_id": gym_id,
            "gym_name": gym["gym_name"],  # Gym name from selected gym
            "gym_location": gym["city"]  # Gym city/location
        }

        # Append the new member and save
        members.append(new_member)
        DataLoader.save_data("members", members)
        print(f"Member added successfully with ID: {new_member_id} at Gym: {gym['gym_name']} in {gym['city']}.")


    @staticmethod
    def delete_member(member_id):
        members = DataLoader.get_data("members")
        updated_members = [m for m in members if m["member_id"] != member_id]
        if len(updated_members) < len(members):
            DataLoader.save_data("members", updated_members)
            return True
        return False

    @staticmethod
    def view_all_members():
        return DataLoader.get_data("members")

    @staticmethod
    def search_member(member_id=None, name=None):
        members = DataLoader.get_data("members")
        if member_id:
            return next((m for m in members if m["member_id"] == member_id), None)
        elif name:
            return next((m for m in members if m["name"].lower() == name.lower()), None)
        return None

    @staticmethod
    def get_member_details(member_id):
        payments = DataLoader.get_data("payments")
        attendance = DataLoader.get_data("attendance")
        member = MemberManagement.search_member(member_id=member_id)
        if not member:
            return None
        total_paid = sum(float(p["amount"]) for p in payments if p["member_id"] == member_id)
        attendance_count = len([a for a in attendance if a["member_id"] == member_id])
        member_details = member.copy()
        member_details["total_paid"] = total_paid
        member_details["attendance_count"] = attendance_count
        return member_details

    @staticmethod
    def update_member(member_id, field, new_value):
        """
        Updates a specific field of a member's details.
        :param member_id: The ID of the member to update.
        :param field: The field to update (e.g., 'name', 'membership_type').
        :param new_value: The new value for the field.
        """
        members = DataLoader.get_data("members")
        member = next((m for m in members if m["member_id"] == member_id), None)

        if not member:
            print(f"Error: Member ID {member_id} not found.")
            return

        # Normalize field input to lowercase for comparison
        field = field.lower()
        valid_fields = {k.lower(): k for k in member.keys()}  # Create mapping for case-insensitive validation

        if field not in valid_fields:
            print(f"Error: Invalid field '{field}'. Valid fields are: {', '.join(member.keys())}")
            return

        # Update the field with the correctly cased key
        member[valid_fields[field]] = new_value

        # Save the updated members list
        DataLoader.save_data("members", members)
        print(f"Member ID {member_id}'s {valid_fields[field]} updated successfully to {new_value}.")
'''
from utils.helpers import generate_unique_id
from database.data_loader import DataLoader


class MemberManagement:
    @staticmethod
    def add_member(name, membership_type, join_date):
        members = DataLoader.get_data("members")
        new_member_id = generate_unique_id(members, "member_id")

        new_member = {
            "member_id": str(new_member_id),
            "name": name,
            "membership_type": membership_type,
            "join_date": join_date
        }
        members.append(new_member)
        DataLoader.save_data("members", members)
        print(f"Member added successfully with ID: {new_member_id}")

    @staticmethod
    def delete_member(member_id):
        members = DataLoader.get_data("members")
        updated_members = [m for m in members if m["member_id"] != member_id]
        if len(updated_members) < len(members):
            DataLoader.save_data("members", updated_members)
            return True
        return False

    @staticmethod
    def view_all_members():
        return DataLoader.get_data("members")

    @staticmethod
    def search_member(member_id=None, name=None):
        members = DataLoader.get_data("members")
        if member_id:
            return next((m for m in members if m["member_id"] == member_id), None)
        elif name:
            return next((m for m in members if m["name"].lower() == name.lower()), None)
        return None

    @staticmethod
    def get_member_details(member_id):
        payments = DataLoader.get_data("payments")
        attendance = DataLoader.get_data("attendance")
        member = MemberManagement.search_member(member_id=member_id)
        if not member:
            return None
        total_paid = sum(float(p["amount"]) for p in payments if p["member_id"] == member_id)
        attendance_count = len([a for a in attendance if a["member_id"] == member_id])
        member_details = member.copy()
        member_details["total_paid"] = total_paid
        member_details["attendance_count"] = attendance_count
        return member_details
'''

'''

from database.data_loader import DataLoader

class MemberManagement:
    @staticmethod
    def add_member(member_id, name, membership_type, join_date):
        members = DataLoader.get_data("members")
        members.append({
            "member_id": member_id,
            "name": name,
            "membership_type": membership_type,
            "join_date": join_date
        })
        DataLoader.save_data("members", members)

    @staticmethod
    def delete_member(member_id):
        members = DataLoader.get_data("members")
        updated_members = [member for member in members if member["member_id"] != member_id]
        if len(updated_members) == len(members):  # No member found to delete
            return False
        DataLoader.save_data("members", updated_members)
        return True
'''