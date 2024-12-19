# core/registration_manager.py

from database.data_loader import DataLoader
from core.class_activity_manager import ClassActivityManager
from core.member_management import MemberManagement
from core.gym_management import GymManager
import logging

logger = logging.getLogger(__name__)

class RegistrationManager:
    @staticmethod
    def register_user_to_class(class_id, member_id, day, time):
        """
        Register a gym user to a specific schedule of a class.

        :param class_id: ID of the class.
        :param member_id: ID of the gym user.
        :param day: Day of the class schedule (e.g., 'Monday').
        :param time: Time slot of the class schedule (e.g., '10:00-11:00').
        :return: None
        """
        logger.debug(f"Attempting to register member_id {member_id} to class_id {class_id} on {day} at {time}.")
        classes = DataLoader.get_data("classes")
        cls = next((c for c in classes if c["class_id"] == class_id), None)
        if not cls:
            logger.error(f"Class ID {class_id} does not exist.")
            raise ValueError(f"Class ID {class_id} does not exist.")

        if not isinstance(cls.get("schedule", {}), dict):
            logger.error(f"Schedule for Class ID {class_id} is not a dictionary.")
            raise TypeError(f"Schedule for Class ID {class_id} is not properly formatted.")

        # Validate that the selected schedule exists
        if day not in cls["schedule"]:
            logger.error(f"Day '{day}' is not available for Class ID {class_id}.")
            raise ValueError(f"Day '{day}' is not available for Class ID {class_id}.")

        if time not in cls["schedule"][day]:
            logger.error(f"Time '{time}' is not available on '{day}' for Class ID {class_id}.")
            raise ValueError(f"Time '{time}' is not available on '{day}' for Class ID {class_id}.")

        # Check capacity for the specific schedule
        current_count = sum(
            1 for user in cls.get("registered_users", [])
            if user["day"] == day and user["time"] == time
        )
        if current_count >= cls["capacity"]:
            logger.warning(f"Class ID {class_id} on {day} at {time} has reached its capacity.")
            raise ValueError(f"Class '{cls['class_name']}' on {day} at {time} has reached its capacity.")

        # Verify that the user exists and belongs to the same gym
        user = MemberManagement.get_member_by_id(member_id)
        if not user:
            logger.error(f"Member ID {member_id} does not exist.")
            raise ValueError(f"Member ID {member_id} does not exist.")

        if user["gym_id"] != cls["gym_id"]:
            logger.error(f"Member ID {member_id} does not belong to Gym ID {cls['gym_id']}.")
            raise ValueError(f"Member ID {member_id} does not belong to Gym ID {cls['gym_id']}.")

        # Check if the user is already registered for this specific schedule
        already_registered = any(
            user["member_id"] == member_id and user["day"] == day and user["time"] == time
            for user in cls.get("registered_users", [])
        )
        if already_registered:
            logger.warning(f"Member ID {member_id} is already registered for Class ID {class_id} on {day} at {time}.")
            raise ValueError(f"Member ID {member_id} is already registered for this schedule.")

        # Register the user
        cls["registered_users"].append({
            "member_id": member_id,
            "day": day,
            "time": time
        })
        DataLoader.save_data("classes", classes)
        logger.info(f"Member ID {member_id} successfully registered to Class ID {class_id} on {day} at {time}.")

    @staticmethod
    def unregister_user_from_class(class_id, member_id, day, time):
        """
        Unregister a gym user from a specific schedule of a class.

        :param class_id: ID of the class.
        :param member_id: ID of the gym user.
        :param day: Day of the class schedule.
        :param time: Time slot of the class schedule.
        :return: None
        """
        logger.debug(f"Attempting to unregister member_id {member_id} from class_id {class_id} on {day} at {time}.")
        classes = DataLoader.get_data("classes")
        cls = next((c for c in classes if c["class_id"] == class_id), None)
        if not cls:
            logger.error(f"Class ID {class_id} does not exist.")
            raise ValueError(f"Class ID {class_id} does not exist.")

        if "registered_users" not in cls:
            logger.warning(f"No users are registered for Class ID {class_id}.")
            raise ValueError(f"No users are registered for Class ID {class_id}.")

        # Find the registration entry
        registration_entry = next(
            (user for user in cls["registered_users"] if user["member_id"] == member_id and user["day"] == day and user["time"] == time),
            None
        )
        if not registration_entry:
            logger.warning(f"Member ID {member_id} is not registered for Class ID {class_id} on {day} at {time}.")
            raise ValueError(f"Member ID {member_id} is not registered for this schedule.")

        # Unregister the user
        cls["registered_users"].remove(registration_entry)
        DataLoader.save_data("classes", classes)
        logger.info(f"Member ID {member_id} successfully unregistered from Class ID {class_id} on {day} at {time}.")

    @staticmethod
    def get_registered_users(class_id):
        """
        Retrieve a list of registered users for a specific class.

        :param class_id: ID of the class.
        :return: List of user dictionaries.
        """
        logger.debug(f"Retrieving registered users for class_id {class_id}.")
        classes = DataLoader.get_data("classes")
        cls = next((c for c in classes if c["class_id"] == class_id), None)
        if not cls:
            logger.error(f"Class ID {class_id} does not exist.")
            raise ValueError(f"Class ID {class_id} does not exist.")

        member_ids = [user["member_id"] for user in cls.get("registered_users", [])]
        members = MemberManagement.view_all_members()
        # Corrected list comprehension
        registered_users = [m for m in members if m["member_id"] in member_ids]
        logger.info(f"Retrieved {len(registered_users)} registered users for Class ID {class_id}.")
        return registered_users

    @staticmethod
    def get_all_registrations():
        """
        Retrieve all registration records with details about the gym, class, schedule, and training staff.
        """
        logger.debug("Retrieving all registrations from all classes.")
        classes = DataLoader.get_data("classes")
        members = MemberManagement.view_all_members()
        gyms = GymManager.view_all_gyms()

        all_data = []
        for c in classes:
            gym_id = c["gym_id"]
            gym = next((g for g in gyms if g["gym_id"] == gym_id), None)
            training_staff = c.get("trainer_name", "N/A")
            class_name = c["class_name"]
            class_id = c["class_id"]
            registered_users = c.get("registered_users", [])
            for ru in registered_users:
                member_id = ru["member_id"]
                day = ru["day"]
                time = ru["time"]
                member = next((m for m in members if m["member_id"] == member_id), {})
                member_name = member.get("name", "Unknown")
                gym_name = gym.get("gym_name", "Unknown") if gym else "Unknown"
                all_data.append({
                    "member_id": member_id,
                    "member_name": member_name,
                    "class_id": class_id,
                    "class_name": class_name,
                    "gym_id": gym_id,
                    "gym_name": gym_name,
                    "day": day,
                    "time": time,
                    "training_staff": training_staff
                })

        logger.info(f"Retrieved {len(all_data)} total registrations across all classes.")
        return all_data
