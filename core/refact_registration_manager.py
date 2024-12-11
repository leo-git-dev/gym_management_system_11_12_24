# core/registration_management.py

import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from core.registration_manager import RegistrationManager
from core.class_activity_manager import ClassActivityManager
from core.member_management import MemberManagement
from core.gym_management import GymManager
from database.data_loader import DataLoader
import logging
import re

# Configure logging with debug level for detailed output
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RegistrationManagementFrame(ttk.Frame):
    def __init__(self, parent, data_loader:DataLoader):
        super().__init__(parent)
        self.parent = parent  # The Notebook or main application frame
        self.selected_payment_id = None  # Not directly used here but kept for consistency
        self.create_widgets()

    def create_widgets(self):
        # Create Tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")

        # Create Frames for Tabs
        self.register_tab = ttk.Frame(self.notebook)
        self.unregister_tab = ttk.Frame(self.notebook)

        # Add Tabs to Notebook
        self.notebook.add(self.register_tab, text="Register User")
        self.notebook.add(self.unregister_tab, text="Unregister User")

        # Initialize Tabs
        self.create_register_tab()
        self.create_unregister_tab()

        # Bind tab change to update title if needed
        # Uncomment and modify if you want to handle title updates
        # self.notebook.bind("<<NotebookTabChanged>>", lambda e: self.update_title(self.notebook.tab(self.notebook.select(), "text")))

    def update_title(self, title):
        """Update window title with the current tab name."""
        # Assuming the main application handles the window title,
        # you might want to emit an event or call a callback instead.
        # For now, we'll leave this method empty.
        pass

    # Register Tab
    def create_register_tab(self):
        main_frame = ttk.Frame(self.register_tab, padding="10")
        main_frame.pack(fill="both", expand=True)

        # Section 1: Register User to Class
        register_frame = ttk.LabelFrame(main_frame, text="Register User to Class")
        register_frame.pack(fill="x", pady=5)

        # Select Gym
        ttk.Label(register_frame, text="Select Gym:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.register_gym_dropdown = ttk.Combobox(register_frame, values=self.get_gym_display_names(), state="readonly", width=50)
        self.register_gym_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.register_gym_dropdown.set("Select Gym")
        self.register_gym_dropdown.bind("<<ComboboxSelected>>", self.update_class_dropdown)

        # Select Class
        ttk.Label(register_frame, text="Select Class:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.register_class_dropdown = ttk.Combobox(register_frame, values=[], state="readonly", width=50)
        self.register_class_dropdown.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.register_class_dropdown.set("Select Class")
        self.register_class_dropdown.bind("<<ComboboxSelected>>", self.update_schedule_dropdown)

        # Select Day
        ttk.Label(register_frame, text="Select Day:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.register_day_dropdown = ttk.Combobox(register_frame, values=[], state="readonly", width=50)
        self.register_day_dropdown.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.register_day_dropdown.set("Select Day")
        self.register_day_dropdown.bind("<<ComboboxSelected>>", self.update_time_dropdown)

        # Select Time
        ttk.Label(register_frame, text="Select Time:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.register_time_dropdown = ttk.Combobox(register_frame, values=[], state="readonly", width=50)
        self.register_time_dropdown.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        self.register_time_dropdown.set("Select Time")
        self.register_time_dropdown.bind("<<ComboboxSelected>>", self.update_register_user_dropdown)

        # Select User
        ttk.Label(register_frame, text="Select User:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.register_user_dropdown = ttk.Combobox(register_frame, values=[], state="readonly", width=50)
        self.register_user_dropdown.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        self.register_user_dropdown.set("Select User")

        # Register Button
        register_button = ttk.Button(register_frame, text="Register User", command=self.register_user)
        register_button.grid(row=5, column=0, columnspan=2, pady=10)

    # Unregister Tab
    def create_unregister_tab(self):
        main_frame = ttk.Frame(self.unregister_tab, padding="10")
        main_frame.pack(fill="both", expand=True)

        # Section 2: Unregister User from Class
        unregister_frame = ttk.LabelFrame(main_frame, text="Unregister User from Class")
        unregister_frame.pack(fill="x", pady=5)

        # Select Gym for Unregistration
        ttk.Label(unregister_frame, text="Select Gym:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.unregister_gym_dropdown = ttk.Combobox(unregister_frame, values=self.get_gym_display_names(), state="readonly", width=50)
        self.unregister_gym_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.unregister_gym_dropdown.set("Select Gym")
        self.unregister_gym_dropdown.bind("<<ComboboxSelected>>", self.update_unregister_class_dropdown)

        # Select Class for Unregistration
        ttk.Label(unregister_frame, text="Select Class:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.unregister_class_dropdown = ttk.Combobox(unregister_frame, values=[], state="readonly", width=50)
        self.unregister_class_dropdown.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.unregister_class_dropdown.set("Select Class")
        self.unregister_class_dropdown.bind("<<ComboboxSelected>>", self.update_unregister_schedule_dropdown)

        # Select Day for Unregistration
        ttk.Label(unregister_frame, text="Select Day:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.unregister_day_dropdown = ttk.Combobox(unregister_frame, values=[], state="readonly", width=50)
        self.unregister_day_dropdown.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.unregister_day_dropdown.set("Select Day")
        self.unregister_day_dropdown.bind("<<ComboboxSelected>>", self.update_unregister_time_dropdown)

        # Select Time for Unregistration
        ttk.Label(unregister_frame, text="Select Time:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.unregister_time_dropdown = ttk.Combobox(unregister_frame, values=[], state="readonly", width=50)
        self.unregister_time_dropdown.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        self.unregister_time_dropdown.set("Select Time")
        self.unregister_time_dropdown.bind("<<ComboboxSelected>>", self.update_unregister_user_dropdown)

        # Select User for Unregistration
        ttk.Label(unregister_frame, text="Select User:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.unregister_user_dropdown = ttk.Combobox(unregister_frame, values=[], state="readonly", width=50)
        self.unregister_user_dropdown.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        self.unregister_user_dropdown.set("Select User")

        # Unregister Button
        unregister_button = ttk.Button(unregister_frame, text="Unregister User", command=self.unregister_user)
        unregister_button.grid(row=5, column=0, columnspan=2, pady=10)

    def extract_id_from_display(self, display_string, entity_type="ID"):
        """
        Extracts the ID from a display string formatted as 'Name (ID: XXX)'.

        :param display_string: The display string.
        :param entity_type: The type of ID to extract ('ID' by default).
        :return: Extracted ID or None if not found.
        """
        pattern = rf"\({entity_type}: (\w+)\)"
        match = re.search(pattern, display_string)
        if match:
            return match.group(1)
        else:
            logger.error(f"Failed to extract {entity_type} from '{display_string}'.")
            return None

    def get_gym_display_names(self):
        """
        Retrieve all gym names formatted with their IDs.
        :return: List of formatted gym names.
        """
        try:
            gyms = GymManager.view_all_gyms()
            logger.info(f"Loaded gyms: {gyms}")
            return [f"{gym['gym_name']} (ID: {gym['gym_id']})" for gym in gyms]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load gyms: {e}")
            logger.error(f"Failed to load gyms: {e}")
            return []

    def update_class_dropdown(self, event=None):
        """
        Update the class dropdown based on the selected gym.
        """
        selected_gym = self.register_gym_dropdown.get()
        logger.info(f"Selected gym: {selected_gym}")
        if not selected_gym or selected_gym == "Select Gym":
            self.register_class_dropdown['values'] = []
            self.register_class_dropdown.set("Select Class")
            self.register_day_dropdown['values'] = []
            self.register_day_dropdown.set("Select Day")
            self.register_time_dropdown['values'] = []
            self.register_time_dropdown.set("Select Time")
            self.register_user_dropdown['values'] = []
            self.register_user_dropdown.set("Select User")
            return

        gym_id = self.extract_id_from_display(selected_gym, "ID")
        if not gym_id:
            messagebox.showerror("Error", "Invalid gym selection format.")
            return

        try:
            classes = ClassActivityManager.view_all_classes()
            gym_classes = [f"{cls['class_name']} (ID: {cls['class_id']})" for cls in classes if cls['gym_id'] == gym_id]
            logger.info(f"Classes for gym_id {gym_id}: {gym_classes}")

            self.register_class_dropdown['values'] = gym_classes
            self.register_class_dropdown.set("Select Class")
            self.register_day_dropdown['values'] = []
            self.register_day_dropdown.set("Select Day")
            self.register_time_dropdown['values'] = []
            self.register_time_dropdown.set("Select Time")
            self.register_user_dropdown['values'] = []
            self.register_user_dropdown.set("Select User")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load classes: {e}")
            logger.error(f"Failed to load classes: {e}")

    def update_schedule_dropdown(self, event=None):
        """
        Update the day dropdown based on the selected class.
        """
        selected_class = self.register_class_dropdown.get()
        logger.info(f"Selected class for registration: {selected_class}")
        if not selected_class or selected_class == "Select Class":
            self.register_day_dropdown['values'] = []
            self.register_day_dropdown.set("Select Day")
            self.register_time_dropdown['values'] = []
            self.register_time_dropdown.set("Select Time")
            self.register_user_dropdown['values'] = []
            self.register_user_dropdown.set("Select User")
            return

        class_id = self.extract_id_from_display(selected_class, "ID")
        if not class_id:
            messagebox.showerror("Error", "Invalid class selection format.")
            return

        try:
            classes = ClassActivityManager.view_all_classes()
            cls = next((c for c in classes if c["class_id"] == class_id), None)
            if not cls:
                messagebox.showerror("Error", "Selected class does not exist.")
                return

            days = list(cls["schedule"].keys())
            logger.info(f"Available days for class_id {class_id}: {days}")

            self.register_day_dropdown['values'] = days
            self.register_day_dropdown.set("Select Day")
            self.register_time_dropdown['values'] = []
            self.register_time_dropdown.set("Select Time")
            self.register_user_dropdown['values'] = []
            self.register_user_dropdown.set("Select User")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load schedule: {e}")
            logger.error(f"Failed to load schedule: {e}")

    def update_time_dropdown(self, event=None):
        """
        Update the time dropdown based on the selected day.
        """
        selected_class = self.register_class_dropdown.get()
        selected_day = self.register_day_dropdown.get()
        logger.info(f"Selected day for registration: {selected_day}")

        if not selected_day or selected_day == "Select Day":
            self.register_time_dropdown['values'] = []
            self.register_time_dropdown.set("Select Time")
            self.register_user_dropdown['values'] = []
            self.register_user_dropdown.set("Select User")
            return

        class_id = self.extract_id_from_display(selected_class, "ID")
        try:
            classes = ClassActivityManager.view_all_classes()
            cls = next((c for c in classes if c["class_id"] == class_id), None)
            if not cls:
                messagebox.showerror("Error", "Selected class does not exist.")
                return

            times = cls["schedule"].get(selected_day, [])
            logger.info(f"Available times on {selected_day} for class_id {class_id}: {times}")

            self.register_time_dropdown['values'] = times
            self.register_time_dropdown.set("Select Time")
            self.register_user_dropdown['values'] = []
            self.register_user_dropdown.set("Select User")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load times: {e}")
            logger.error(f"Failed to load times: {e}")

    def update_register_user_dropdown(self, event=None):
        """
        Update the user dropdown based on the selected class, day, and time.
        """
        selected_class = self.register_class_dropdown.get()
        selected_day = self.register_day_dropdown.get()
        selected_time = self.register_time_dropdown.get()
        logger.info(f"Selected class: {selected_class}, day: {selected_day}, time: {selected_time}")

        if not all([selected_class != "Select Class", selected_day != "Select Day", selected_time != "Select Time"]):
            self.register_user_dropdown['values'] = []
            self.register_user_dropdown.set("Select User")
            logger.debug("Insufficient selections for user dropdown.")
            return

        class_id = self.extract_id_from_display(selected_class, "ID")
        day = selected_day
        time = selected_time

        try:
            # Check current registrations for this schedule
            classes = ClassActivityManager.view_all_classes()
            cls = next((c for c in classes if c["class_id"] == class_id), None)
            if not cls:
                messagebox.showerror("Error", "Selected class does not exist.")
                logger.error(f"Class with ID {class_id} not found.")
                return

            current_registrations = [
                user for user in cls.get("registered_users", [])
                if user["day"] == day and user["time"] == time
            ]
            current_member_ids = {user["member_id"] for user in current_registrations}
            logger.debug(f"Current Registrations: {current_registrations}")
            logger.debug(f"Current Member IDs: {current_member_ids}")

            # Retrieve all Gym Users eligible for registration (not already registered for this schedule)
            all_members = MemberManagement.view_all_members()
            logger.debug(f"All Members: {all_members}")
            gym_id = cls["gym_id"]

            eligible_users = [
                m for m in all_members
                if m["gym_id"] == gym_id
                and m["user_type"] == "Gym User"
                and m["member_id"] not in current_member_ids
            ]
            logger.debug(f"Eligible Users: {eligible_users}")

            if not eligible_users:
                messagebox.showinfo("Info", "No eligible users available for registration for this schedule.")
                self.register_user_dropdown['values'] = []
                self.register_user_dropdown.set("Select User")
                return

            # Format user display names
            user_display = [f"{user['name']} (ID: {user['member_id']})" for user in eligible_users]
            self.register_user_dropdown['values'] = user_display
            self.register_user_dropdown.set("Select User")
            logger.info(f"User dropdown updated with: {user_display}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to retrieve eligible users: {e}")
            logger.error(f"Failed to retrieve eligible users: {e}")

    # Unregister Tab Methods
    def update_unregister_class_dropdown(self, event=None):
        """
        Update the class dropdown for unregistration based on the selected gym.
        """
        selected_gym = self.unregister_gym_dropdown.get()
        logger.info(f"Selected gym for unregistration: {selected_gym}")
        if not selected_gym or selected_gym == "Select Gym":
            self.unregister_class_dropdown['values'] = []
            self.unregister_class_dropdown.set("Select Class")
            self.unregister_day_dropdown['values'] = []
            self.unregister_day_dropdown.set("Select Day")
            self.unregister_time_dropdown['values'] = []
            self.unregister_time_dropdown.set("Select Time")
            self.unregister_user_dropdown['values'] = []
            self.unregister_user_dropdown.set("Select User")
            return

        gym_id = self.extract_id_from_display(selected_gym, "ID")
        if not gym_id:
            messagebox.showerror("Error", "Invalid gym selection format.")
            return

        try:
            classes = ClassActivityManager.view_all_classes()
            gym_classes = [f"{cls['class_name']} (ID: {cls['class_id']})" for cls in classes if cls['gym_id'] == gym_id]
            logger.info(f"Classes for gym_id {gym_id}: {gym_classes}")

            self.unregister_class_dropdown['values'] = gym_classes
            self.unregister_class_dropdown.set("Select Class")
            self.unregister_day_dropdown['values'] = []
            self.unregister_day_dropdown.set("Select Day")
            self.unregister_time_dropdown['values'] = []
            self.unregister_time_dropdown.set("Select Time")
            self.unregister_user_dropdown['values'] = []
            self.unregister_user_dropdown.set("Select User")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load classes: {e}")
            logger.error(f"Failed to load classes: {e}")

    def update_unregister_schedule_dropdown(self, event=None):
        """
        Update the day dropdown for unregistration based on the selected class.
        """
        selected_class = self.unregister_class_dropdown.get()
        logger.info(f"Selected class for unregistration: {selected_class}")
        if not selected_class or selected_class == "Select Class":
            self.unregister_day_dropdown['values'] = []
            self.unregister_day_dropdown.set("Select Day")
            self.unregister_time_dropdown['values'] = []
            self.unregister_time_dropdown.set("Select Time")
            self.unregister_user_dropdown['values'] = []
            self.unregister_user_dropdown.set("Select User")
            return

        class_id = self.extract_id_from_display(selected_class, "ID")
        if not class_id:
            messagebox.showerror("Error", "Invalid class selection format.")
            return

        try:
            classes = ClassActivityManager.view_all_classes()
            cls = next((c for c in classes if c["class_id"] == class_id), None)
            if not cls:
                messagebox.showerror("Error", "Selected class does not exist.")
                return

            days = list(cls["schedule"].keys())
            logger.info(f"Available days for class_id {class_id}: {days}")

            self.unregister_day_dropdown['values'] = days
            self.unregister_day_dropdown.set("Select Day")
            self.unregister_time_dropdown['values'] = []
            self.unregister_time_dropdown.set("Select Time")
            self.unregister_user_dropdown['values'] = []
            self.unregister_user_dropdown.set("Select User")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load schedule: {e}")
            logger.error(f"Failed to load schedule: {e}")

    def update_unregister_time_dropdown(self, event=None):
        """
        Update the time dropdown based on the selected day for unregistration.
        """
        selected_class = self.unregister_class_dropdown.get()
        selected_day = self.unregister_day_dropdown.get()
        logger.info(f"Selected day for unregistration: {selected_day}")

        if not selected_day or selected_day == "Select Day":
            self.unregister_time_dropdown['values'] = []
            self.unregister_time_dropdown.set("Select Time")
            self.unregister_user_dropdown['values'] = []
            self.unregister_user_dropdown.set("Select User")
            return

        class_id = self.extract_id_from_display(selected_class, "ID")
        try:
            classes = ClassActivityManager.view_all_classes()
            cls = next((c for c in classes if c["class_id"] == class_id), None)
            if not cls:
                messagebox.showerror("Error", "Selected class does not exist.")
                return

            times = cls["schedule"].get(selected_day, [])
            logger.info(f"Available times on {selected_day} for class_id {class_id}: {times}")

            self.unregister_time_dropdown['values'] = times
            self.unregister_time_dropdown.set("Select Time")
            self.unregister_user_dropdown['values'] = []
            self.unregister_user_dropdown.set("Select User")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load times: {e}")
            logger.error(f"Failed to load times: {e}")

    def update_unregister_user_dropdown(self, event=None):
        """
        Update the user dropdown for unregistration based on the selected class, day, and time.
        """
        selected_class = self.unregister_class_dropdown.get()
        selected_day = self.unregister_day_dropdown.get()
        selected_time = self.unregister_time_dropdown.get()
        logger.info(f"Selected class: {selected_class}, day: {selected_day}, time: {selected_time}")

        if not all([selected_class != "Select Class", selected_day != "Select Day", selected_time != "Select Time"]):
            self.unregister_user_dropdown['values'] = []
            self.unregister_user_dropdown.set("Select User")
            logger.debug("Insufficient selections for unregister user dropdown.")
            return

        class_id = self.extract_id_from_display(selected_class, "ID")
        day = selected_day
        time = selected_time

        try:
            # Retrieve registered users for this specific schedule
            classes = ClassActivityManager.view_all_classes()
            cls = next((c for c in classes if c["class_id"] == class_id), None)
            if not cls:
                messagebox.showerror("Error", "Selected class does not exist.")
                logger.error(f"Class with ID {class_id} not found.")
                return

            registered_users = [
                user for user in cls.get("registered_users", [])
                if user["day"] == day and user["time"] == time
            ]
            logger.debug(f"Registered Users: {registered_users}")

            if not registered_users:
                messagebox.showinfo("Info", "No users registered for this schedule.")
                self.unregister_user_dropdown['values'] = []
                self.unregister_user_dropdown.set("Select User")
                return

            # Retrieve member details
            members = MemberManagement.view_all_members()
            logger.debug(f"All Members: {members}")
            registered_member_ids = [user["member_id"] for user in registered_users]
            users_to_unregister = [m for m in members if m["member_id"] in registered_member_ids]
            logger.debug(f"Users to Unregister: {users_to_unregister}")

            if not users_to_unregister:
                messagebox.showinfo("Info", "No users found for unregistration.")
                self.unregister_user_dropdown['values'] = []
                self.unregister_user_dropdown.set("Select User")
                return

            # Format user display names
            user_display = [f"{user['name']} (ID: {user['member_id']})" for user in users_to_unregister]
            self.unregister_user_dropdown['values'] = user_display
            self.unregister_user_dropdown.set("Select User")
            logger.info(f"Unregister User dropdown updated with: {user_display}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to retrieve users for unregistration: {e}")
            logger.error(f"Failed to retrieve users for unregistration: {e}")

    def register_user(self):
        """
        Register a selected user to a selected class schedule.
        """
        selected_class = self.register_class_dropdown.get()
        selected_day = self.register_day_dropdown.get()
        selected_time = self.register_time_dropdown.get()
        selected_user = self.register_user_dropdown.get()

        if not all([selected_class != "Select Class", selected_day != "Select Day", selected_time != "Select Time", selected_user != "Select User"]):
            messagebox.showwarning("Validation Error", "Please select a class, day, time, and user.")
            return

        class_id = self.extract_id_from_display(selected_class, "ID")
        member_id = self.extract_id_from_display(selected_user, "ID")
        day = selected_day
        time = selected_time

        if not all([class_id, member_id, day, time]):
            messagebox.showerror("Error", "Invalid selection format.")
            return

        try:
            RegistrationManager.register_user_to_class(class_id, member_id, day, time)
            messagebox.showinfo("Success", f"User {selected_user} registered to {selected_class} on {day} at {time} successfully.")
            # Refresh dropdowns to reflect updated registrations
            self.update_class_dropdown()
            self.update_register_user_dropdown()
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
            logger.error(str(ve))
        except TypeError as te:
            messagebox.showerror("Error", str(te))
            logger.error(str(te))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to register user: {e}")
            logger.error(f"Failed to register user: {e}")

    def unregister_user(self):
        """
        Unregister a selected user from a selected class schedule.
        """
        selected_class = self.unregister_class_dropdown.get()
        selected_day = self.unregister_day_dropdown.get()
        selected_time = self.unregister_time_dropdown.get()
        selected_user = self.unregister_user_dropdown.get()

        if not all([selected_class != "Select Class", selected_day != "Select Day", selected_time != "Select Time", selected_user != "Select User"]):
            messagebox.showwarning("Validation Error", "Please select a class, day, time, and user.")
            return

        class_id = self.extract_id_from_display(selected_class, "ID")
        member_id = self.extract_id_from_display(selected_user, "ID")
        day = selected_day
        time = selected_time

        if not all([class_id, member_id, day, time]):
            messagebox.showerror("Error", "Invalid selection format.")
            return

        try:
            RegistrationManager.unregister_user_from_class(class_id, member_id, day, time)
            messagebox.showinfo("Success", f"User {selected_user} unregistered from {selected_class} on {day} at {time} successfully.")
            # Refresh dropdowns to reflect updated registrations
            self.update_unregister_class_dropdown()
            self.update_unregister_user_dropdown()
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
            logger.error(str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to unregister user: {e}")
            logger.error(f"Failed to unregister user: {e}")

    # Utility Methods
    def get_gym_display_names(self):
        """
        Retrieve all gym names formatted with their IDs.
        :return: List of formatted gym names.
        """
        try:
            gyms = GymManager.view_all_gyms()
            logger.info(f"Loaded gyms: {gyms}")
            return [f"{gym['gym_name']} (ID: {gym['gym_id']})" for gym in gyms]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load gyms: {e}")
            logger.error(f"Failed to load gyms: {e}")
            return []
