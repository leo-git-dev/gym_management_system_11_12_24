from utils.helpers import generate_unique_id
from database.data_loader import DataLoader
from collections import defaultdict
from datetime import datetime


class GymManager:
    @staticmethod
    def add_gym(name, city, manager_name, manager_contact, manager_email):
        gyms = DataLoader.get_data("gyms")

        # Ensure headers are correct
        if gyms and "gym_id" not in gyms[0]:
            print("Error: gyms.csv is missing required fields. Resetting header.")
            DataLoader.save_data("gyms", [])  # Reset the file

        new_gym_id = generate_unique_id(gyms, "gym_id")

        new_gym = {
            "gym_id": str(new_gym_id),
            "gym_name": name,
            "city": city,
            "manager_name": manager_name,
            "manager_contact": manager_contact,
            "manager_email": manager_email
        }
        gyms.append(new_gym)
        DataLoader.save_data("gyms", gyms)

        # Add gym details to locations.json
        locations = DataLoader.get_data("locations")
        locations.append({
            "location_id": str(new_gym_id),
            "city": city,
            "zones": []
        })
        DataLoader.save_data("locations", locations)

        print(f"Gym added successfully with ID: {new_gym_id}")

    @staticmethod
    def update_gym(gym_id, field, new_value):
        gyms = DataLoader.get_data("gyms")
        for gym in gyms:
            if gym["gym_id"] == gym_id:
                gym[field] = new_value
                DataLoader.save_data("gyms", gyms)
                print(f"{field} updated successfully for Gym ID {gym_id}.")
                return
        print(f"Gym with ID {gym_id} not found.")

    @staticmethod
    def delete_gym(gym_id):
        gyms = DataLoader.get_data("gyms")
        updated_gyms = [gym for gym in gyms if gym["gym_id"] != gym_id]
        if len(updated_gyms) < len(gyms):
            DataLoader.save_data("gyms", updated_gyms)
            print(f"Gym with ID {gym_id} deleted successfully.")
        else:
            print(f"Gym with ID {gym_id} not found.")

        # Remove associated zones from locations.json
        locations = DataLoader.get_data("locations")
        updated_locations = [loc for loc in locations if loc["location_id"] != gym_id]
        DataLoader.save_data("locations", updated_locations)

        # Remove associated attendance records
        attendance = DataLoader.get_data("attendance")
        updated_attendance = [
            a for a in attendance if a.get("location_id") != gym_id  # Use .get() to handle missing keys
        ]
        DataLoader.save_data("attendance", updated_attendance)

        # Update members associated with this gym
        members = DataLoader.get_data("members")
        for member in members:
            if member.get("location_id") == gym_id:
                member["location_id"] = "Unknown"
                member["location_name"] = "Unknown"
        DataLoader.save_data("members", members)

        print("Gym deletion process completed.")

    @staticmethod
    def view_zones():
        gyms = DataLoader.get_data("gyms")
        if not gyms:
            print("No gyms available.")
            return

        # Display available gyms
        print("Available Gyms:")
        for gym in gyms:
            print(f"ID: {gym['gym_id']} - Name: {gym['gym_name']}")

        # Prompt user to select a gym
        gym_id = input("Enter Gym ID to view zones: ")

        locations = DataLoader.get_data("locations")
        location = next((loc for loc in locations if loc["location_id"] == gym_id), None)
        if not location:
            print(f"Gym ID {gym_id} not found in locations.")
            return

        zones = location.get("zones", [])
        if zones:
            print(f"Zones at Gym ID {gym_id}: {', '.join(zones)}")
        else:
            print(f"No zones available at Gym ID {gym_id}.")

    @staticmethod
    def delete_zone(gym_id, zone_name):
        locations = DataLoader.get_data("locations")
        location = next((loc for loc in locations if loc["location_id"] == gym_id), None)
        if not location:
            print(f"Gym ID {gym_id} not found.")
            return
        if zone_name not in location["zones"]:
            print(f"Zone {zone_name} not found at Gym ID {gym_id}.")
            return
        location["zones"].remove(zone_name)
        DataLoader.save_data("locations", locations)
        print(f"Zone {zone_name} deleted successfully from Gym ID {gym_id}.")

    @staticmethod
    def add_zone():
        gyms = DataLoader.get_data("gyms")
        if not gyms:
            print("No gyms available.")
            return

        # Display available gyms
        print("Available Gyms:")
        for gym in gyms:
            print(f"ID: {gym['gym_id']} - Name: {gym['gym_name']}")

        # Prompt user to select a gym
        gym_id = input("Enter Gym ID to add a zone: ")

        locations = DataLoader.get_data("locations")
        location = next((loc for loc in locations if loc["location_id"] == gym_id), None)
        if not location:
            print(f"Gym ID {gym_id} not found.")
            return

        zone_name = input("Enter Zone Name: ")
        if zone_name in location.get("zones", []):
            print(f"Zone {zone_name} already exists at Gym ID {gym_id}.")
            return

        location.setdefault("zones", []).append(zone_name)
        DataLoader.save_data("locations", locations)
        print(f"Zone {zone_name} added successfully to Gym ID {gym_id}.")

    @staticmethod
    def view_all_gyms():
        gyms = DataLoader.get_data("gyms")
        if not gyms:
            print("No gyms found.")
            return

        locations = DataLoader.get_data("locations")
        members = DataLoader.get_data("members")
        attendance = DataLoader.get_data("attendance")
        payments = DataLoader.get_data("payments")

        result = []

        for gym in gyms:
            gym_id = gym["gym_id"]

            # Get location zones and city
            location = next((loc for loc in locations if loc["location_id"] == gym_id), None)
            zones = location["zones"] if location else []
            city = location["city"] if location else "Unknown"

            # Count total members
            total_members = sum(1 for member in members if member.get("gym_id") == gym_id)

            # Calculate activities by type and month-year
            activities = defaultdict(lambda: defaultdict(int))
            for record in attendance:
                if record.get("location_id") == gym_id:
                    date = datetime.strptime(record["date"], "%Y-%m-%d")
                    month_year = date.strftime("%B-%Y")
                    activities[record["workout_zone"]][month_year] += 1

            # Calculate revenue by month-year
            revenue = defaultdict(float)
            for payment in payments:
                if payment.get("member_id") in [m["member_id"] for m in members if m.get("gym_id") == gym_id]:
                    if payment["status"] == "Paid":
                        date = datetime.strptime(payment["date"], "%Y-%m-%d")
                        month_year = date.strftime("%B-%Y")
                        revenue[month_year] += float(payment["amount"])

            # Aggregate data
            result.append({
                "gym_id": gym_id,
                "gym_name": gym["gym_name"],
                "manager_name": gym["manager_name"],
                "manager_contact": gym["manager_contact"],
                "zones": zones,
                "city": city,
                "total_members": total_members,
                "activities": activities,
                "revenue": revenue
            })

        # Display formatted results
        for gym_data in result:
            print(f"\nGym ID: {gym_data['gym_id']}")
            print(f"Name: {gym_data['gym_name']}")
            print(f"City: {gym_data['city']}")
            print(f"Manager: {gym_data['manager_name']} | Contact: {gym_data['manager_contact']}")
            print(f"Zones: {', '.join(gym_data['zones']) if gym_data['zones'] else 'No zones available'}")
            print(f"Total Members: {gym_data['total_members']}")

            print("\nActivity Details:")
            for zone, monthly_data in gym_data["activities"].items():
                print(f"  Zone: {zone}")
                for month_year, count in monthly_data.items():
                    print(f"    {month_year}: {count} activities")

            print("\nRevenue Details:")
            for month_year, total in gym_data["revenue"].items():
                print(f"  {month_year}: ${total:.2f}")

        return result

