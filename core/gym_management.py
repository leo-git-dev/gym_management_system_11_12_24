# core/gym_management.py
# core/gym_management.py

import os
import logging
from utils.helpers import generate_unique_id
from database.data_loader import DataLoader
from datetime import datetime

# Configure logging for this module
log_directory = 'logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

logging.basicConfig(
    filename=os.path.join(log_directory, 'gym_manager.log'),
    level=logging.DEBUG,  # Set to DEBUG for detailed logs
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

class GymManager:
    @staticmethod
    def add_gym(name, city, manager_name, manager_contact, manager_email):
        try:
            gyms = DataLoader.get_data("gyms")
            logger.debug(f"Current gyms before addition: {gyms}")

            # Ensure headers are correct
            if gyms and "gym_id" not in gyms[0]:
                logger.error("gyms.json is missing required fields. Resetting gym data.")
                DataLoader.save_data("gyms", [])  # Reset the file
                gyms = []

            new_gym_id = generate_unique_id(gyms, "gym_id")
            new_gym_id = str(new_gym_id)  # Ensure gym_id is a string

            new_gym = {
                "gym_id": new_gym_id,
                "gym_name": name,
                "city": city,
                "manager_name": manager_name,
                "manager_contact": manager_contact,
                "manager_email": manager_email
            }
            gyms.append(new_gym)
            DataLoader.save_data("gyms", gyms)
            logger.info(f"Gym '{name}' added successfully with ID: {new_gym_id}")

            # Add gym details to locations.json
            locations = DataLoader.get_data("locations")
            logger.debug(f"Current locations before addition: {locations}")

            locations.append({
                "location_id": new_gym_id,
                "city": city,
                "zones": []
            })
            DataLoader.save_data("locations", locations)
            logger.info(f"Location for Gym ID '{new_gym_id}' added successfully.")

            print(f"Gym added successfully with ID: {new_gym_id}")
        except Exception as e:
            logger.error(f"Failed to add gym '{name}': {e}")
            print(f"Failed to add gym '{name}': {e}")

    @staticmethod
    def update_gym(gym_id, field, new_value):
        """
        Update a specific field for a gym in the database.

        :param gym_id: The ID of the gym to update.
        :param field: The field to update (e.g., "gym_name", "manager_name", "city").
        :param new_value: The new value for the field.
        :raises ValueError: If the gym is not found or the field is invalid.
        """
        try:
            gyms = DataLoader.get_data("gyms")
            logger.debug(f"Current gyms before update: {gyms}")

            # Locate the gym by ID
            gym = next((g for g in gyms if g["gym_id"] == gym_id), None)
            if not gym:
                logger.error(f"Gym with ID {gym_id} not found.")
                raise ValueError(f"Gym with ID {gym_id} not found.")

            # Validate the field exists in the gym data
            if field not in gym:
                logger.error(f"Invalid field: {field}.")
                raise ValueError(f"Invalid field: {field}.")

            # Update the field in gyms.json
            old_value = gym[field]
            gym[field] = new_value
            DataLoader.save_data("gyms", gyms)
            logger.info(f"Gym ID {gym_id} updated: {field} changed from '{old_value}' to '{new_value}' in gyms.json.")
            print(f"Gym ID {gym_id} updated: {field} changed from '{old_value}' to '{new_value}' in gyms.json.")

            # If the updated field is 'city', also update it in locations.json
            if field == "city":
                locations = DataLoader.get_data("locations")
                logger.debug(f"Current locations before city update: {locations}")

                location = next((loc for loc in locations if loc["location_id"] == gym_id), None)
                if location:
                    old_city = location.get("city", "Unknown")
                    location["city"] = new_value
                    DataLoader.save_data("locations", locations)
                    logger.info(f"City updated in locations.json for Gym ID {gym_id}: '{old_city}' -> '{new_value}'.")
                    print(f"City updated in locations.json for Gym ID {gym_id}: '{old_city}' -> '{new_value}'.")
                else:
                    logger.warning(f"No location found for Gym ID {gym_id} in locations.json.")
                    print(f"No location found for Gym ID {gym_id} in locations.json.")
        except Exception as e:
            logger.error(f"Failed to update gym '{gym_id}': {e}")
            print(f"Failed to update gym '{gym_id}': {e}")

    @staticmethod
    def delete_gym(gym_id):
        """
        Delete a gym from the system along with all associated data.

        :param gym_id: The ID of the gym to delete.
        """
        try:
            gym_id = str(gym_id).strip()  # Ensure gym_id is a clean string
            logger.debug(f"Starting deletion process for Gym ID: '{gym_id}'")
            gyms = DataLoader.get_data("gyms")
            logger.debug(f"Loaded gyms: {gyms}")

            if not gyms:
                logger.warning("No gyms found to delete.")
                print("No gyms found to delete.")
                return

            # Log all existing gym IDs
            existing_gym_ids = [gym["gym_id"] for gym in gyms]
            logger.debug(f"Existing Gym IDs: {existing_gym_ids}")
            print(f"Existing Gym IDs: {existing_gym_ids}")

            # Check if gym exists
            gym_exists = any(gym["gym_id"] == gym_id for gym in gyms)
            if not gym_exists:
                logger.error(f"Gym with ID {gym_id} not found.")
                print(f"Gym with ID {gym_id} not found.")
                return

            # Remove the gym from gyms.json
            updated_gyms = [gym for gym in gyms if gym["gym_id"] != gym_id]
            DataLoader.save_data("gyms", updated_gyms)
            logger.info(f"Gym with ID {gym_id} deleted successfully from gyms.json.")
            print(f"Gym with ID {gym_id} deleted successfully.")

            # Remove associated zones from locations.json
            locations = DataLoader.get_data("locations")
            logger.debug(f"Current locations before deletion: {locations}")

            updated_locations = [loc for loc in locations if loc["location_id"] != gym_id]
            DataLoader.save_data("locations", updated_locations)
            logger.info(f"Location with ID {gym_id} deleted successfully from locations.json.")

            # Remove associated attendance records
            attendance = DataLoader.get_data("attendance")
            updated_attendance = [
                a for a in attendance if a.get("location_id") != gym_id  # Use .get() to handle missing keys
            ]
            DataLoader.save_data("attendance", updated_attendance)
            logger.info(f"Attendance records associated with Gym ID {gym_id} deleted successfully.")

            # Remove associated classes from classes.json
            classes = DataLoader.get_data("classes")
            updated_classes = [cls for cls in classes if cls.get("gym_id") != gym_id]
            DataLoader.save_data("classes", updated_classes)
            logger.info(f"Classes associated with Gym ID {gym_id} deleted successfully from classes.json.")

            # Update members associated with this gym
            members = DataLoader.get_data("members")
            updated_members = []
            for member in members:
                if member.get("gym_id") == gym_id:
                    member["gym_id"] = "Unknown"
                    member["gym_name"] = "Unknown"
                updated_members.append(member)
            DataLoader.save_data("members", updated_members)
            logger.info(f"Members associated with Gym ID {gym_id} updated to 'Unknown' gym.")

            print("Gym deletion process completed successfully.")
        except Exception as e:
            logger.error(f"Failed to delete gym '{gym_id}': {e}")
            print(f"Failed to delete gym '{gym_id}': {e}")

    @staticmethod
    def view_zones(gym_id):
        """
        Returns the zones for a given gym.
        :param gym_id: The ID of the gym to view zones for.
        :return: List of zones for the gym.
        """
        try:
            locations = DataLoader.get_data("locations")
            location = next((loc for loc in locations if loc["location_id"] == gym_id), None)
            if not location:
                logger.error(f"Gym ID {gym_id} not found in locations.")
                raise ValueError(f"Gym ID {gym_id} not found in locations.")

            zones = location.get("zones", [])
            logger.info(f"Zones for Gym ID {gym_id}: {zones}")
            return zones
        except Exception as e:
            logger.error(f"Failed to view zones for Gym ID {gym_id}: {e}")
            raise

    @staticmethod
    def add_zone(gym_id, zone_name):
        """
        Adds a new zone to the specified gym.

        :param gym_id: The ID of the gym.
        :param zone_name: The name of the new zone.
        :raises ValueError: If the zone already exists or inputs are invalid.
        """
        try:
            logger.debug(f"Attempting to add zone '{zone_name}' to Gym ID '{gym_id}'")
            # Load locations data
            locations = DataLoader.get_data("locations")
            location = next((loc for loc in locations if loc["location_id"] == gym_id), None)
            if not location:
                logger.error(f"Location for Gym ID '{gym_id}' not found.")
                raise ValueError("Selected gym's location not found.")

            # Check if zone already exists (case-insensitive)
            existing_zones = [zone.lower() for zone in location.get("zones", [])]
            if zone_name.lower() in existing_zones:
                logger.warning(f"Zone '{zone_name}' already exists in Gym ID '{gym_id}'.")
                raise ValueError(f"Zone '{zone_name}' already exists in the selected gym.")

            # Add the new zone
            location["zones"].append(zone_name)
            DataLoader.save_data("locations", locations)
            logger.info(f"Zone '{zone_name}' added successfully to Gym ID '{gym_id}'.")
        except ValueError as ve:
            logger.error(f"ValueError in add_zone: {ve}")
            raise
        except Exception as e:
            logger.error(f"Exception in add_zone: {e}")
            raise

    @staticmethod
    def update_zone(gym_id, old_zone_name, new_zone_name):
        """
        Updates the name of an existing zone in the specified gym.

        :param gym_id: The ID of the gym.
        :param old_zone_name: The current name of the zone.
        :param new_zone_name: The new name for the zone.
        :raises ValueError: If the old zone doesn't exist or the new zone name is already taken.
        """
        try:
            logger.debug(f"Attempting to update zone '{old_zone_name}' to '{new_zone_name}' in Gym ID '{gym_id}'")
            # Load locations data
            locations = DataLoader.get_data("locations")
            location = next((loc for loc in locations if loc["location_id"] == gym_id), None)
            if not location:
                logger.error(f"Location for Gym ID '{gym_id}' not found.")
                raise ValueError("Selected gym's location not found.")

            # Check if old zone exists
            zones = location.get("zones", [])
            if old_zone_name not in zones:
                logger.warning(f"Zone '{old_zone_name}' does not exist in Gym ID '{gym_id}'.")
                raise ValueError(f"Zone '{old_zone_name}' does not exist in the selected gym.")

            # Check if new zone name already exists
            if new_zone_name.lower() in [zone.lower() for zone in zones]:
                logger.warning(f"Zone '{new_zone_name}' already exists in Gym ID '{gym_id}'.")
                raise ValueError(f"Zone '{new_zone_name}' already exists in the selected gym.")

            # Update the zone name
            index = zones.index(old_zone_name)
            location["zones"][index] = new_zone_name
            DataLoader.save_data("locations", locations)
            logger.info(f"Zone '{old_zone_name}' updated to '{new_zone_name}' in Gym ID '{gym_id}'.")
        except ValueError as ve:
            logger.error(f"ValueError in update_zone: {ve}")
            raise
        except Exception as e:
            logger.error(f"Exception in update_zone: {e}")
            raise

    @staticmethod
    def delete_zone(gym_id, zone_name):
        """
        Deletes a zone from the specified gym.

        :param gym_id: The ID of the gym.
        :param zone_name: The name of the zone to delete.
        :raises ValueError: If the zone doesn't exist.
        """
        try:
            logger.debug(f"Attempting to delete zone '{zone_name}' from Gym ID '{gym_id}'")
            # Load locations data
            locations = DataLoader.get_data("locations")
            location = next((loc for loc in locations if loc["location_id"] == gym_id), None)
            if not location:
                logger.error(f"Location for Gym ID '{gym_id}' not found.")
                raise ValueError("Selected gym's location not found.")

            # Check if zone exists
            zones = location.get("zones", [])
            if zone_name not in zones:
                logger.warning(f"Zone '{zone_name}' does not exist in Gym ID '{gym_id}'.")
                raise ValueError(f"Zone '{zone_name}' does not exist in the selected gym.")

            # Delete the zone
            location["zones"].remove(zone_name)
            DataLoader.save_data("locations", locations)
            logger.info(f"Zone '{zone_name}' deleted successfully from Gym ID '{gym_id}'.")
        except ValueError as ve:
            logger.error(f"ValueError in delete_zone: {ve}")
            raise
        except Exception as e:
            logger.error(f"Exception in delete_zone: {e}")
            raise

    @staticmethod
    def view_all_gyms():
        """
        Retrieve and return all gyms with comprehensive details.
        :return: List of dictionaries containing gym details.
        """
        try:
            gyms = DataLoader.get_data("gyms")
            locations = DataLoader.get_data("locations")
            members = DataLoader.get_data("members")
            attendance = DataLoader.get_data("attendance")
            payments = DataLoader.get_data("payments")
            classes = DataLoader.get_data("classes")

            result = []

            for gym in gyms:
                gym_id = gym["gym_id"]

                # Get location zones and city
                location = next((loc for loc in locations if loc["location_id"] == gym_id), None)
                zones = location.get("zones", []) if location else []
                city = location.get("city", "Unknown") if location else "Unknown"

                # Count total members
                total_members = sum(1 for member in members if member.get("gym_id") == gym_id)

                # Calculate revenue by status
                revenue = {"Total Paid": 0.0, "Total Pending": 0.0}
                relevant_member_ids = [m["member_id"] for m in members if m.get("gym_id") == gym_id]
                for payment in payments:
                    if payment.get("member_id") in relevant_member_ids:
                        if payment["status"] == "Paid":
                            revenue["Total Paid"] += float(payment["amount"])
                        elif payment["status"] == "Pending":
                            revenue["Total Pending"] += float(payment["amount"])

                # Calculate staff totals (example logic)
                activities = {
                    "Wellbeing Staff": {"count": 2, "cost": 3000.0},
                    "Training Staff": {"count": 5, "cost": 7500.0},
                    "Management Staff": {"count": 3, "cost": 4500.0},
                }

                # Aggregate data
                result.append({
                    "gym_id": gym_id,
                    "gym_name": gym["gym_name"],
                    "city": city,
                    "manager_name": gym["manager_name"],
                    "manager_contact": gym["manager_contact"],
                    "manager_email": gym["manager_email"],
                    "total_members": total_members,
                    "revenue": revenue,
                    "activities": activities,
                    "zones": zones,
                })

            logger.info("All gyms retrieved successfully.")
            return result
        except Exception as e:
            logger.error(f"Failed to retrieve gyms: {e}")
            raise

    @staticmethod
    def view_gym_by_id(gym_id):
        """
        Retrieve gym details by gym_id, including city and zones.

        :param gym_id: The ID of the gym.
        :return: Dictionary containing gym details or None if not found.
        """
        try:
            gyms = DataLoader.get_data("gyms")
            gym = next((g for g in gyms if g["gym_id"] == gym_id), None)
            if gym:
                # Retrieve city and zones from locations.json
                locations = DataLoader.get_data("locations")
                location = next((loc for loc in locations if loc["location_id"] == gym_id), None)
                if location:
                    gym["city"] = location.get("city", "Unknown")
                    gym["zones"] = location.get("zones", [])
                else:
                    gym["city"] = "Unknown"
                    gym["zones"] = []
                logger.info(f"Gym details retrieved for Gym ID {gym_id}.")
            else:
                logger.warning(f"Gym ID {gym_id} not found.")
            return gym
        except Exception as e:
            logger.error(f"Failed to retrieve gym by ID '{gym_id}': {e}")
            raise



'''from utils.helpers import generate_unique_id
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
        """
        Update a specific field for a gym in the database.

        :param gym_id: The ID of the gym to update.
        :param field: The field to update (e.g., "gym_name", "manager_name", "city").
        :param new_value: The new value for the field.
        :raises ValueError: If the gym is not found or the field is invalid.
        """
        gyms = DataLoader.get_data("gyms")

        # Locate the gym by ID
        gym = next((g for g in gyms if g["gym_id"] == gym_id), None)
        if not gym:
            raise ValueError(f"Gym with ID {gym_id} not found.")

        # Validate the field exists in the gym data
        if field not in gym:
            raise ValueError(f"Invalid field: {field}.")

        # Update the field in gyms.json
        old_value = gym[field]
        gym[field] = new_value
        DataLoader.save_data("gyms", gyms)
        print(f"Gym ID {gym_id} updated: {field} changed from '{old_value}' to '{new_value}' in gyms.json.")

        # If the updated field is 'city', also update it in locations.json
        if field == "city":
            locations = DataLoader.get_data("locations")
            location = next((loc for loc in locations if loc["location_id"] == gym_id), None)
            if location:
                old_city = location.get("city", "Unknown")
                location["city"] = new_value
                DataLoader.save_data("locations", locations)
                print(f"City updated in locations.json for Gym ID {gym_id}: '{old_city}' -> '{new_value}'.")
            else:
                print(f"No location found for Gym ID {gym_id} in locations.json.")

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
            if member.get("gym_id") == gym_id:  # Changed from 'location_id' to 'gym_id'
                member["gym_id"] = "Unknown"
                member["gym_name"] = "Unknown"
        DataLoader.save_data("members", members)

        print("Gym deletion process completed.")

    @staticmethod
    def view_zones(gym_id):
        """
        Returns the zones for a given gym.
        :param gym_id: The ID of the gym to view zones for.
        :return: List of zones for the gym.
        """
        locations = DataLoader.get_data("locations")
        location = next((loc for loc in locations if loc["location_id"] == gym_id), None)
        if not location:
            raise ValueError(f"Gym ID {gym_id} not found in locations.")

        return location.get("zones", [])

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
    def add_zone(gym_id, zone_name):
        """
        Adds a new zone to a gym.
        :param gym_id: The ID of the gym where the zone will be added.
        :param zone_name: The name of the zone to be added.
        """
        locations = DataLoader.get_data("locations")
        location = next((loc for loc in locations if loc["location_id"] == gym_id), None)
        if not location:
            raise ValueError(f"Gym ID {gym_id} not found.")

        if zone_name in location.get("zones", []):
            raise ValueError(f"Zone {zone_name} already exists at Gym ID {gym_id}.")

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
                "manager_email": gym["manager_email"],
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

    @staticmethod
    def view_gym_by_id(gym_id):
        """
        Retrieve gym details by gym_id, including city and zones.

        :param gym_id: The ID of the gym.
        :return: Dictionary containing gym details or None if not found.
        """
        gyms = DataLoader.get_data("gyms")
        gym = next((g for g in gyms if g["gym_id"] == gym_id), None)
        if gym:
            # Retrieve city and zones from locations.json
            locations = DataLoader.get_data("locations")
            location = next((loc for loc in locations if loc["location_id"] == gym_id), None)
            if location:
                gym["city"] = location.get("city", "Unknown")
                gym["zones"] = location.get("zones", [])
            else:
                gym["city"] = "Unknown"
                gym["zones"] = []
        return gym
'''