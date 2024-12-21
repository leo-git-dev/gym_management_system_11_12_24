# core/class_activity_manager.py
# core/class_activity_manager.py
import os
import logging
from utils.helpers import generate_unique_id
from database.data_loader import DataLoader
from core.member_management import MemberManagement
from core.gym_management import GymManager
import re

# Ensure log directory exists
log_directory = 'logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Configure logging for this module
logging.basicConfig(
    filename=os.path.join(log_directory, 'class_activity_manager.log'),
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Get a logger for this module
logger = logging.getLogger(__name__)

class ClassActivityManager:
    @staticmethod
    def add_class(class_name, trainer_id, schedule, capacity, gym_id):
        """
        Add a new class to the system.

        :param class_name: Name of the class.
        :param trainer_id: ID of the training staff.
        :param schedule: Schedule of the class (e.g., {'Monday': ['10:00-11:00']}).
        :param capacity: Maximum number of gym users that can attend.
        :param gym_id: ID of the gym where the class is held.
        """
        try:
            classes = DataLoader.get_data("classes")
            gyms = DataLoader.get_data("gyms")

            # Verify gym_id exists
            gym = next((g for g in gyms if g["gym_id"] == gym_id), None)
            if not gym:
                logger.error("Invalid gym ID provided.")
                raise ValueError("Invalid gym ID provided.")

            # Validate schedule format
            validated_schedule = ClassActivityManager.validate_schedule(schedule)

            # Validate capacity
            if not isinstance(capacity, int) or capacity <= 0:
                logger.error("Capacity must be a positive integer.")
                raise ValueError("Capacity must be a positive integer.")

            # Check for duplicate class names within the same gym
            duplicate = next((c for c in classes if c["class_name"].lower() == class_name.lower() and c["gym_id"] == gym_id), None)
            if duplicate:
                logger.warning(f"Duplicate class name '{class_name}' found in gym '{gym_id}'.")
                raise ValueError(f"A class named '{class_name}' already exists in the selected gym.")

            # Generate a unique class ID
            new_class_id = generate_unique_id(classes, "class_id")

            # Retrieve trainer details
            trainer = MemberManagement.get_member_by_id(trainer_id)
            if not trainer or trainer["user_type"] != "Training Staff":
                logger.error("Invalid trainer selected.")
                raise ValueError("Invalid trainer selected.")

            new_class = {
                "class_id": str(new_class_id),
                "class_name": class_name,
                "trainer_id": trainer_id,
                "trainer_name": trainer["name"],
                "gym_id": gym_id,
                "gym_name": gym["gym_name"],
                "schedule": validated_schedule,
                "capacity": capacity,
                "registered_users": []  # List to hold member_ids
            }

            classes.append(new_class)
            DataLoader.save_data("classes", classes)
            logger.info(f"Class '{class_name}' added successfully with ID: {new_class_id}")
            return new_class_id
        except Exception as e:
            logger.error(f"Failed to add class '{class_name}': {e}")
            raise

    @staticmethod
    def view_all_classes():
        """
        Retrieve all classes from the database.

        :return: List of class dictionaries.
        """
        try:
            classes = DataLoader.get_data("classes")
            logger.info(f"Retrieved {len(classes)} classes from the system.")
            return classes
        except Exception as e:
            logger.error(f"Failed to retrieve classes: {e}")
            return []

    @staticmethod
    def update_class(class_id, updates):
        """
        Update details of an existing class.

        :param class_id: ID of the class to update.
        :param updates: Dictionary containing fields to update.
        """
        try:
            classes = DataLoader.get_data("classes")
            class_to_update = next((c for c in classes if c["class_id"] == class_id), None)

            if not class_to_update:
                logger.error(f"Class ID {class_id} not found.")
                raise ValueError(f"Class ID {class_id} not found.")

            # Allowed fields to update
            allowed_fields = {"class_name", "trainer_id", "schedule", "capacity"}

            for field, value in updates.items():
                if field not in allowed_fields:
                    logger.warning(f"Attempted to update unauthorized field '{field}' in class '{class_id}'.")
                    raise ValueError(f"Field '{field}' is not valid for classes.")

                if field == "trainer_id":
                    # Validate trainer
                    trainer = MemberManagement.get_member_by_id(value)
                    if not trainer or trainer["user_type"] != "Training Staff":
                        logger.error("Invalid trainer selected.")
                        raise ValueError("Invalid trainer selected.")
                    class_to_update["trainer_id"] = value
                    class_to_update["trainer_name"] = trainer["name"]
                    logger.debug(f"Updated trainer for class '{class_id}' to '{trainer['name']}'.")

                elif field == "schedule":
                    # Validate schedule
                    validated_schedule = ClassActivityManager.validate_schedule(value)
                    class_to_update["schedule"] = validated_schedule
                    logger.debug(f"Updated schedule for class '{class_id}'.")

                elif field == "capacity":
                    # Validate capacity
                    if not isinstance(value, int) or value <= 0:
                        logger.error("Capacity must be a positive integer.")
                        raise ValueError("Capacity must be a positive integer.")
                    if value < len(class_to_update["registered_users"]):
                        logger.error("New capacity is less than the number of registered users.")
                        raise ValueError("New capacity cannot be less than the number of registered users.")
                    class_to_update["capacity"] = value
                    logger.debug(f"Updated capacity for class '{class_id}' to {value}.")

                else:
                    class_to_update[field] = value

            DataLoader.save_data("classes", classes)
            logger.info(f"Class ID {class_id} updated successfully.")
            return True
        except Exception as e:
            logger.error(f"Failed to update class '{class_id}': {e}")
            raise

    @staticmethod
    def delete_class(class_id):
        """
        Delete a class from the system.

        :param class_id: ID of the class to delete.
        """
        try:
            classes = DataLoader.get_data("classes")
            updated_classes = [c for c in classes if c["class_id"] != class_id]

            if len(updated_classes) == len(classes):
                logger.error(f"Class ID '{class_id}' not found.")
                raise ValueError(f"Class ID '{class_id}' not found.")

            DataLoader.save_data("classes", updated_classes)
            logger.info(f"Class ID '{class_id}' deleted successfully.")
            return True
        except Exception as e:
            logger.error(f"Failed to delete class '{class_id}': {e}")
            raise

    @staticmethod
    def get_trainer_schedule(trainer_id):
        """
        Retrieve all schedules for a given trainer.

        :param trainer_id: ID of the trainer.
        :return: List of schedules.
        """
        try:
            classes = DataLoader.get_data("classes")
            trainer_classes = [c["schedule"] for c in classes if c["trainer_id"] == trainer_id]
            logger.info(f"Retrieved schedule for trainer '{trainer_id}'.")
            return trainer_classes
        except Exception as e:
            logger.error(f"Failed to retrieve schedule for trainer '{trainer_id}': {e}")
            return []

    @staticmethod
    def get_registered_user_count(class_id):
        """
        Get the number of gym users registered to a class.

        :param class_id: ID of the class.
        :return: Integer count of registered users.
        """
        try:
            classes = DataLoader.get_data("classes")
            cls = next((c for c in classes if c["class_id"] == class_id), None)
            if cls:
                count = len(cls.get("registered_users", []))
                logger.info(f"Class '{class_id}' has {count} registered users.")
                return count
            logger.warning(f"Class ID '{class_id}' not found.")
            return 0
        except Exception as e:
            logger.error(f"Failed to get registered user count for class '{class_id}': {e}")
            return 0

    @staticmethod
    def register_user_to_class(class_id, member_id):
        """
        Register a gym user to a class.

        :param class_id: ID of the class.
        :param member_id: ID of the gym user.
        """
        try:
            classes = DataLoader.get_data("classes")
            cls = next((c for c in classes if c["class_id"] == class_id), None)
            if not cls:
                logger.error(f"Class ID '{class_id}' not found.")
                raise ValueError(f"Class ID '{class_id}' not found.")

            if len(cls["registered_users"]) >= cls["capacity"]:
                logger.warning(f"Class '{class_id}' capacity reached.")
                raise ValueError("Class capacity reached.")

            if member_id in cls["registered_users"]:
                logger.warning(f"User '{member_id}' already registered for class '{class_id}'.")
                raise ValueError("User already registered for this class.")

            # Optionally, verify member existence and eligibility
            member = MemberManagement.get_member_by_id(member_id)
            if not member:
                logger.error(f"Member ID '{member_id}' does not exist.")
                raise ValueError("Member does not exist.")

            cls["registered_users"].append(member_id)
            DataLoader.save_data("classes", classes)
            logger.info(f"Member ID '{member_id}' registered to Class ID '{class_id}' successfully.")
            return True
        except Exception as e:
            logger.error(f"Failed to register user '{member_id}' to class '{class_id}': {e}")
            raise

    @staticmethod
    def validate_schedule(schedule):
        """
        Validate the schedule format:
        schedule = {
            "Monday": ["10:00-11:00", "14:00-15:00"],
            "Tuesday": [],
            ...
        }

        :param schedule: Schedule dictionary to validate.
        :return: Validated schedule dictionary.
        """
        import re

        if not isinstance(schedule, dict):
            logger.error("Schedule must be a dictionary.")
            raise ValueError("Schedule must be a dictionary.")

        for day, times in schedule.items():
            if day not in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
                logger.error(f"Invalid day in schedule: {day}.")
                raise ValueError(f"Invalid day in schedule: {day}.")

            if not isinstance(times, list):
                logger.error(f"Expected a list of intervals for {day}.")
                raise ValueError(f"Expected a list of intervals for {day}.")

            for interval in times:
                if not isinstance(interval, str):
                    logger.error(f"Interval must be a string in the format 'HH:MM-HH:MM' for {day}.")
                    raise ValueError(f"Interval must be a string in the format 'HH:MM-HH:MM' for {day}.")

                if not re.match(r"^\d{2}:\d{2}-\d{2}:\d{2}$", interval):
                    logger.error(f"Invalid interval format for {day}: {interval}. Expected 'HH:MM-HH:MM'.")
                    raise ValueError(f"Invalid interval format for {day}: {interval}. Expected 'HH:MM-HH:MM'.")

                start_time, end_time = interval.split("-")
                if not ClassActivityManager.is_valid_time_format(start_time) or not ClassActivityManager.is_valid_time_format(end_time):
                    logger.error(f"Invalid time format in interval for {day}: {interval}.")
                    raise ValueError(f"Invalid time format in interval for {day}: {interval}.")

                if end_time <= start_time:
                    logger.error(f"End time must be later than start time for {day}: {interval}.")
                    raise ValueError(f"End time must be later than start time for {day}: {interval}.")

        logger.debug("Schedule validated successfully.")
        return schedule

    @staticmethod
    def is_valid_time_format(t):
        """
        Simple check for HH:MM format.

        :param t: Time string to validate.
        :return: True if valid, else False.
        """
        return bool(re.match(r"^\d{2}:\d{2}$", t))

    @classmethod
    def search_activities(cls, gym_id=None, trainer_id=None):
        """
        Search activities based on gym ID and/or trainer ID.

        Args:
            gym_id (str): The ID of the gym to filter activities by (optional).
            trainer_id (str): The ID of the trainer to filter activities by (optional).

        Returns:
            list: A list of activities matching the search criteria. Each activity is a dictionary with full details.
        """
        # Fetch all activities
        activities = cls.view_all_classes()

        # Filter activities based on gym_id and trainer_id
        filtered_activities = []
        for activity in activities:
            matches_gym = gym_id is None or str(activity['gym_id']) == str(gym_id)
            matches_trainer = trainer_id is None or str(activity['trainer_id']) == str(trainer_id)

            if matches_gym and matches_trainer:
                filtered_activities.append(activity)

        return filtered_activities
