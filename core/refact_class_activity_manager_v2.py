import tkinter as tk
from tkinter import ttk, messagebox
from core.class_activity_manager import ClassActivityManager
from core.gym_management import GymManager
from core.member_management import MemberManagement
import logging
import re


# Define constants for days and time slots
DAYS_OF_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
TIME_SLOTS = [
    "06:00-07:00", "07:00-08:00", "08:00-09:00",
    "09:00-10:00", "10:00-11:00", "11:00-12:00",
    "12:00-13:00", "13:00-14:00", "14:00-15:00",
    "15:00-16:00", "16:00-17:00", "17:00-18:00",
    "18:00-19:00", "19:00-20:00", "20:00-21:00",
    "21:00-22:00", "22:00-23:00", "23:00-00:00"
]

# Configure logging
logging.basicConfig(
    filename='logs/class_activity_tk_manager.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ClassManagementApp(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # Removed self.root.title(...) since we now use a Frame as parent
        self.create_widgets()

    def create_widgets(self):
        # Tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")

        self.add_tab = ttk.Frame(self.notebook)
        self.view_tab = ttk.Frame(self.notebook)
        self.search_tab = ttk.Frame(self.notebook)  # New Search Tab

        self.notebook.add(self.add_tab, text="Add Class")
        self.notebook.add(self.view_tab, text="View/Manage Classes")
        self.notebook.add(self.search_tab, text="Search Activities")  # Add the new tab

        self.create_add_tab()
        self.create_view_tab()
        self.create_search_tab()

    def create_search_tab(self):
        """
        Create the Search Activity tab with functionality to search by gym name or training staff.
        """
        for widget in self.search_tab.winfo_children():
            widget.destroy()

        ttk.Label(self.search_tab, text="Search Activities", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=4,
                                                                                          pady=10)

        # Dropdowns for search criteria
        ttk.Label(self.search_tab, text="Search by Gym Name:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.search_gym_dropdown = ttk.Combobox(self.search_tab, values=self.get_gym_display_names(), state="readonly")
        self.search_gym_dropdown.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.search_gym_dropdown.set("Select Gym")

        ttk.Label(self.search_tab, text="Search by Trainer Name:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.search_trainer_dropdown = ttk.Combobox(self.search_tab, values=self.get_training_staff_names(),
                                                    state="readonly")
        self.search_trainer_dropdown.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.search_trainer_dropdown.set("Select Trainer")

        # Search Button
        search_button = ttk.Button(self.search_tab, text="Search", command=self.search_activities)
        search_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Refresh Button
        refresh_button = ttk.Button(self.search_tab, text="Refresh", command=self.refresh_search_tab)
        refresh_button.grid(row=4, column=0, columnspan=2, pady=5)

        # Treeview for displaying search results
        columns = ("ID", "Class Name", "Trainer", "Gym", "Schedule", "Capacity", "Registered Users")
        self.search_tree = ttk.Treeview(self.search_tab, columns=columns, show="headings")
        for col in columns:
            self.search_tree.heading(col, text=col)
            self.search_tree.column(col, width=150, anchor="center")
        self.search_tree.grid(row=5, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        # Configure row and column weights
        self.search_tab.grid_columnconfigure(0, weight=1)
        self.search_tab.grid_columnconfigure(1, weight=1)
        self.search_tab.grid_rowconfigure(5, weight=1)

    def search_activities(self):
        """
        Search activities based on the selected gym or trainer.
        """
        selected_gym = self.search_gym_dropdown.get()
        selected_trainer = self.search_trainer_dropdown.get()

        if selected_gym == "Select Gym" and selected_trainer == "Select Trainer":
            messagebox.showwarning("Validation Error", "Please select a Gym or Trainer to search.")
            return

        gym_id = None
        trainer_id = None

        # Extract gym ID
        if selected_gym != "Select Gym":
            try:
                gym_id = selected_gym.split("(ID: ")[1].rstrip(")")
            except IndexError:
                messagebox.showerror("Error", "Invalid gym selection format.")
                return

        # Extract trainer ID
        if selected_trainer != "Select Trainer":
            try:
                trainer_id = selected_trainer.split("(ID: ")[1].rstrip(")")
            except IndexError:
                messagebox.showerror("Error", "Invalid trainer selection format.")
                return

        # Search activities
        try:
            activities = ClassActivityManager.search_activities(gym_id=gym_id, trainer_id=trainer_id)
            for row in self.search_tree.get_children():
                self.search_tree.delete(row)

            for activity in activities:
                registered_count = len(activity.get("registered_users", []))
                schedule_formatted = self.format_schedule(activity["schedule"])
                self.search_tree.insert(
                    "",
                    "end",
                    values=(
                        activity["class_id"],
                        activity["class_name"],
                        activity["trainer_name"],
                        activity["gym_name"],
                        schedule_formatted,
                        activity["capacity"],
                        registered_count
                    ),
                )
            if not activities:
                messagebox.showinfo("No Results", "No activities found for the selected criteria.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to search activities: {e}")

    def refresh_search_tab(self):
        """
        Refresh the Search Activity tab: reload gym and trainer dropdowns and clear search results.
        """
        self.search_gym_dropdown['values'] = self.get_gym_display_names()
        self.search_gym_dropdown.set("Select Gym")
        self.search_trainer_dropdown['values'] = self.get_training_staff_names()
        self.search_trainer_dropdown.set("Select Trainer")

        for row in self.search_tree.get_children():
            self.search_tree.delete(row)

        messagebox.showinfo("Refreshed", "Search tab refreshed.")

    def create_add_tab(self):
        """
        Create the Add Class tab with all required fields.
        """
        for widget in self.add_tab.winfo_children():
            widget.destroy()

        ttk.Label(self.add_tab, text="Add New Class", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=4, pady=10)

        # 1.1 Class Name
        ttk.Label(self.add_tab, text="Class Name:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.class_name_entry = ttk.Entry(self.add_tab)
        self.class_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # 1.2 Select Gym by Gym Name using Drop-down Menu
        ttk.Label(self.add_tab, text="Select Gym:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.gym_dropdown = ttk.Combobox(self.add_tab, values=self.get_gym_display_names(), state="readonly")
        self.gym_dropdown.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.gym_dropdown.set("Select Gym")

        # Bind gym selection to update trainer dropdown
        self.gym_dropdown.bind("<<ComboboxSelected>>", self.update_trainer_dropdown)

        # 1.3 Select Training Staff by Name using Drop-down Menu
        ttk.Label(self.add_tab, text="Select Trainer:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.trainer_dropdown = ttk.Combobox(self.add_tab, values=[], state="readonly")
        self.trainer_dropdown.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        self.trainer_dropdown.set("Select Trainer")

        # Bind trainer selection to update schedule
        self.trainer_dropdown.bind("<<ComboboxSelected>>", self.update_trainer_schedule)

        # 1.4 Retrieve Date/Time from Training Staff: Display in a Table
        ttk.Label(self.add_tab, text="Trainer Schedule:").grid(row=4, column=0, padx=5, pady=5, sticky="ne")
        self.trainer_schedule_tree = ttk.Treeview(self.add_tab, columns=("Schedule"), show="headings", height=5)
        self.trainer_schedule_tree.heading("Schedule", text="Schedule")
        self.trainer_schedule_tree.column("Schedule", width=200, anchor="center")
        self.trainer_schedule_tree.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        # 1.5 Add Schedule Table: Ability to Add Further Classes
        ttk.Label(self.add_tab, text="Add Additional Schedules:").grid(row=5, column=0, padx=5, pady=5, sticky="ne")
        self.additional_schedule_frame = ttk.Frame(self.add_tab)
        self.additional_schedule_frame.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        self.schedule_entries = []
        self.add_schedule_row()  # Add initial schedule row

        add_schedule_button = ttk.Button(self.additional_schedule_frame, text="Add Another Schedule", command=self.add_schedule_row)
        add_schedule_button.grid(row=100, column=0, columnspan=4, pady=5)

        # 1.6 Enter Class Capacity: Limit Gym Users to Attend the Class
        ttk.Label(self.add_tab, text="Class Capacity:").grid(row=6, column=0, padx=5, pady=5, sticky="e")
        self.capacity_entry = ttk.Entry(self.add_tab)
        self.capacity_entry.grid(row=6, column=1, padx=5, pady=5, sticky="w")

        # 1.7 Add Class Button: Parse Information to Update the Schedule Database
        add_class_button = ttk.Button(self.add_tab, text="Add Class", command=self.add_class)
        add_class_button.grid(row=7, column=0, columnspan=4, pady=10)

        # 1.8 Add a Refresh Button to reload gyms and clear trainer schedule
        refresh_button = ttk.Button(self.add_tab, text="Refresh", command=self.refresh_add_tab)
        refresh_button.grid(row=8, column=0, columnspan=4, pady=5)

    def create_view_tab(self):
        """
        Create the View/Manage Classes tab with all required functionalities.
        """
        for widget in self.view_tab.winfo_children():
            widget.destroy()

        ttk.Label(self.view_tab, text="View and Manage Classes", font=("Helvetica", 16)).pack(pady=10)

        # 2.1 Display Table with Class Details
        self.classes_tree = ttk.Treeview(
            self.view_tab,
            columns=("ID", "Name", "Trainer", "Gym", "Schedule", "Capacity", "Registered Users"),
            show="headings",
            selectmode="browse"
        )
        self.classes_tree.heading("ID", text="Class ID")
        self.classes_tree.heading("Name", text="Class Name")
        self.classes_tree.heading("Trainer", text="Trainer Name")
        self.classes_tree.heading("Gym", text="Gym Name")
        self.classes_tree.heading("Schedule", text="Schedule")
        self.classes_tree.heading("Capacity", text="Capacity")
        self.classes_tree.heading("Registered Users", text="Registered Users")
        self.classes_tree.pack(expand=True, fill="both", padx=10, pady=10)

        # 2.2 Refresh Button to Load Classes
        refresh_button = ttk.Button(self.view_tab, text="Refresh", command=self.view_all_classes)
        refresh_button.pack(pady=5)

        # 2.3 Update/Delete Frame
        manage_frame = ttk.Frame(self.view_tab)
        manage_frame.pack(pady=5)

        # 2.4 Update Class Functionality
        ttk.Label(manage_frame, text="Select Class:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.manage_class_dropdown = ttk.Combobox(manage_frame, values=self.get_class_display_names(), state="readonly")
        self.manage_class_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.manage_class_dropdown.set("Select Class")
        self.manage_class_dropdown.bind("<<ComboboxSelected>>", self.populate_update_fields)

        ttk.Label(manage_frame, text="Field to Update:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.update_field_dropdown = ttk.Combobox(
            manage_frame,
            values=["Trainer", "Schedule", "Capacity"],
            state="readonly"
        )
        self.update_field_dropdown.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.update_field_dropdown.set("Select Field")

        ttk.Label(manage_frame, text="New Value:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.update_value_entry = ttk.Entry(manage_frame)
        self.update_value_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        update_button = ttk.Button(manage_frame, text="Update Class", command=self.update_class)
        update_button.grid(row=3, column=0, padx=5, pady=5)

        # 2.5 Delete Class Functionality
        delete_button = ttk.Button(manage_frame, text="Delete Class", command=self.delete_class)
        delete_button.grid(row=3, column=1, padx=5, pady=5)

        # Load all classes initially
        self.view_all_classes()

    def refresh_add_tab(self):
        """
        Refresh the Add Class tab: re-fetch gyms and clear trainer schedule.
        """
        self.gym_dropdown['values'] = self.get_gym_display_names()
        self.gym_dropdown.set("Select Gym")
        self.trainer_dropdown['values'] = []
        self.trainer_dropdown.set("Select Trainer")
        for row in self.trainer_schedule_tree.get_children():
            self.trainer_schedule_tree.delete(row)
        # Also clear schedules if needed
        for day_cb, time_cb in self.schedule_entries:
            day_cb.set("Select Day")
            time_cb.set("Select Time")
        self.class_name_entry.delete(0, tk.END)
        self.capacity_entry.delete(0, tk.END)
        messagebox.showinfo("Refreshed", "Add Class tab refreshed.")

    def create_main_menu(self):
        """
        Navigate back to the main menu. Placeholder for actual main menu implementation.
        """
        messagebox.showinfo("Info", "Return to main menu functionality to be implemented.")

    def get_gym_display_names(self):
        """
        Retrieve all gym names formatted with their IDs.
        """
        gyms = GymManager.view_all_gyms()
        gym_display = [f"{gym['gym_name']} (ID: {gym['gym_id']})" for gym in gyms]
        logger.debug(f"Retrieved gym display names: {gym_display}")
        return gym_display

    def get_training_staff_names(self, gym_id=None):
        """
        Retrieve all training staff names, optionally filtered by gym_id.
        """
        members = MemberManagement.view_all_members()
        training_staff = [m for m in members if m["user_type"] == "Training Staff"]
        if gym_id:
            training_staff = [m for m in training_staff if m["gym_id"] == gym_id]
        trainers_display = [f"{staff['name']} (ID: {staff['member_id']})" for staff in training_staff]
        logger.debug(f"Retrieved training staff names for gym '{gym_id}': {trainers_display}")
        return trainers_display

    def get_class_display_names(self):
        """
        Retrieve all classes formatted with their IDs.
        """
        classes = ClassActivityManager.view_all_classes()
        class_display = [f"{cls['class_name']} (ID: {cls['class_id']})" for cls in classes]
        logger.debug(f"Retrieved class display names: {class_display}")
        return class_display

    def update_trainer_dropdown(self, event=None):
        """
        Update the trainer dropdown based on the selected gym.
        """
        selected_gym = self.gym_dropdown.get()
        if not selected_gym or selected_gym == "Select Gym":
            self.trainer_dropdown['values'] = []
            self.trainer_dropdown.set("Select Trainer")
            # Clear trainer schedule
            for row in self.trainer_schedule_tree.get_children():
                self.trainer_schedule_tree.delete(row)
            logger.debug("No gym selected. Trainer dropdown cleared.")
            return

        # Extract gym_id from selection
        try:
            gym_id = selected_gym.split("(ID: ")[1].rstrip(")")
        except IndexError:
            messagebox.showerror("Error", "Invalid gym selection format.")
            logger.error("Invalid gym selection format.")
            return

        trainers = self.get_training_staff_names(gym_id)
        self.trainer_dropdown['values'] = trainers
        self.trainer_dropdown.set("Select Trainer")
        logger.debug(f"Trainer dropdown updated for gym '{gym_id}': {trainers}")

        # Clear trainer schedule
        for row in self.trainer_schedule_tree.get_children():
            self.trainer_schedule_tree.delete(row)

    def update_trainer_schedule(self, event=None):
        """
        Update the trainer schedule table based on selected trainer.
        """
        selected_trainer = self.trainer_dropdown.get()
        if not selected_trainer or selected_trainer == "Select Trainer":
            for row in self.trainer_schedule_tree.get_children():
                self.trainer_schedule_tree.delete(row)
            logger.debug("No trainer selected. Trainer schedule cleared.")
            return

        try:
            trainer_id = selected_trainer.split("(ID: ")[1].rstrip(")")
        except IndexError:
            messagebox.showerror("Error", "Invalid trainer selection format.")
            logger.error("Invalid trainer selection format.")
            return

        schedules = ClassActivityManager.get_trainer_schedule(trainer_id)
        logger.debug(f"Schedules retrieved for trainer '{trainer_id}': {schedules}")

        # Clear existing schedule entries
        for row in self.trainer_schedule_tree.get_children():
            self.trainer_schedule_tree.delete(row)

        # Populate the trainer schedule table
        for sched in schedules:
            try:
                # Determine if sched is a dict or an object
                if isinstance(sched, dict):
                    schedule_dict = sched
                else:
                    # Assuming sched has a 'schedule' attribute
                    schedule_dict = sched.schedule

                formatted_sched = self.format_schedule_for_display(schedule_dict)
                self.trainer_schedule_tree.insert("", "end", values=(formatted_sched,))
            except AttributeError as ae:
                logger.error(f"AttributeError: {ae} - Skipping this schedule entry.")
                continue
            except Exception as e:
                logger.error(f"Failed to format schedule for display: {e}")
                continue

        logger.debug(f"Trainer schedule updated for trainer '{trainer_id}'.")

    def format_schedule_for_display(self, schedule_dict):
        """
        Format the schedule dictionary into a readable string.
        """
        schedule_str = ""
        if not isinstance(schedule_dict, dict):
            logger.error(f"Expected schedule to be a dict, got {type(schedule_dict)} instead.")
            return schedule_str  # Return empty string if not a dict

        for day, times in schedule_dict.items():
            times_formatted = ", ".join(times)
            schedule_str += f"{day}: {times_formatted}\n"

        return schedule_str.strip()

    def add_schedule_row(self):
        """
        Add a new schedule entry row in the Add Class tab.
        """
        row = len(self.schedule_entries)
        ttk.Label(self.additional_schedule_frame, text=f"Schedule {row + 1} Day:").grid(row=row, column=0, padx=5, pady=2, sticky="e")
        day_combobox = ttk.Combobox(self.additional_schedule_frame, values=DAYS_OF_WEEK, state="readonly")
        day_combobox.grid(row=row, column=1, padx=5, pady=2, sticky="w")
        day_combobox.set("Select Day")

        ttk.Label(self.additional_schedule_frame, text=f"Schedule {row + 1} Time:").grid(row=row, column=2, padx=5, pady=2, sticky="e")
        time_combobox = ttk.Combobox(self.additional_schedule_frame, values=TIME_SLOTS, state="readonly")
        time_combobox.grid(row=row, column=3, padx=5, pady=2, sticky="w")
        time_combobox.set("Select Time")

        self.schedule_entries.append((day_combobox, time_combobox))
        logger.debug(f"Added new schedule row: Day Combobox - {day_combobox}, Time Combobox - {time_combobox}")

    def add_class(self):
        """
        Gather information from the Add Class form and add a new class.
        """
        class_name = self.class_name_entry.get().strip()
        selected_gym = self.gym_dropdown.get()
        selected_trainer = self.trainer_dropdown.get()
        capacity = self.capacity_entry.get().strip()

        if not class_name:
            messagebox.showwarning("Validation Error", "Please enter the class name.")
            logger.warning("Add Class failed: Class name is empty.")
            return
        if not selected_gym or selected_gym == "Select Gym":
            messagebox.showwarning("Validation Error", "Please select a gym.")
            logger.warning("Add Class failed: Gym not selected.")
            return
        if not selected_trainer or selected_trainer == "Select Trainer":
            messagebox.showwarning("Validation Error", "Please select a trainer.")
            logger.warning("Add Class failed: Trainer not selected.")
            return
        if not capacity.isdigit() or int(capacity) <= 0:
            messagebox.showwarning("Validation Error", "Please enter a valid class capacity.")
            logger.warning("Add Class failed: Invalid capacity entered.")
            return

        try:
            gym_id = selected_gym.split("(ID: ")[1].rstrip(")")
            trainer_id = selected_trainer.split("(ID: ")[1].rstrip(")")
        except IndexError:
            messagebox.showerror("Error", "Invalid selection format for gym or trainer.")
            logger.error("Add Class failed: Invalid selection format for gym or trainer.")
            return

        additional_schedules = {}
        for day_cb, time_cb in self.schedule_entries:
            day = day_cb.get().strip()
            time = time_cb.get().strip()
            if day != "Select Day" and time != "Select Time":
                if day not in additional_schedules:
                    additional_schedules[day] = []
                additional_schedules[day].append(time)

        existing_schedules = ClassActivityManager.get_trainer_schedule(trainer_id)
        existing_schedule_times = []
        for sched in existing_schedules:
            if not isinstance(sched, dict):
                logger.error(f"Expected schedule to be a dict, got {type(sched)} instead.")
                continue
            for day, times in sched.items():
                for t in times:
                    existing_schedule_times.append(f"{day} {t}")

        logger.debug(f"Existing schedules for trainer '{trainer_id}': {existing_schedule_times}")

        for day, times in additional_schedules.items():
            for t in times:
                schedule_entry = f"{day} {t}"
                if schedule_entry in existing_schedule_times:
                    messagebox.showwarning("Validation Error", f"Schedule conflict detected: {schedule_entry}")
                    logger.warning(f"Add Class failed: Schedule conflict for {schedule_entry}")
                    return

        final_schedule = additional_schedules
        try:
            validated_schedule = ClassActivityManager.validate_schedule(final_schedule)
        except ValueError as ve:
            messagebox.showerror("Validation Error", str(ve))
            logger.error(f"Add Class failed during schedule validation: {ve}")
            return

        capacity_int = int(capacity)

        try:
            class_id = ClassActivityManager.add_class(
                class_name=class_name,
                trainer_id=trainer_id,
                schedule=validated_schedule,
                capacity=capacity_int,
                gym_id=gym_id
            )
            messagebox.showinfo("Success", f"Class '{class_name}' added successfully with ID: {class_id}.")
            logger.info(f"Class '{class_name}' added successfully with ID: {class_id}.")
            self.clear_add_class_form()
            self.view_all_classes()
            self.refresh_manage_class_dropdown()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add class: {e}")
            logger.error(f"Failed to add class '{class_name}': {e}")

    def clear_add_class_form(self):
        """
        Clear all input fields in the Add Class form.
        """
        self.class_name_entry.delete(0, tk.END)
        self.gym_dropdown.set("Select Gym")
        self.trainer_dropdown.set("Select Trainer")
        for day_cb, time_cb in self.schedule_entries:
            day_cb.set("Select Day")
            time_cb.set("Select Time")
        self.capacity_entry.delete(0, tk.END)

        for row in self.trainer_schedule_tree.get_children():
            self.trainer_schedule_tree.delete(row)
        logger.debug("Add Class form cleared.")

    def view_all_classes(self):
        """
        Populate the classes_tree with all classes from the database.
        """
        try:
            classes = ClassActivityManager.view_all_classes()
            for row in self.classes_tree.get_children():
                self.classes_tree.delete(row)
            for cls in classes:
                registered_count = len(cls.get("registered_users", []))
                schedule_formatted = self.format_schedule(cls["schedule"])
                self.classes_tree.insert(
                    "",
                    "end",
                    values=(
                        cls["class_id"],
                        cls["class_name"],
                        cls["trainer_name"],
                        cls["gym_name"],
                        schedule_formatted,
                        cls["capacity"],
                        registered_count
                    ),
                )
            logger.info("Classes loaded into the view successfully.")
            self.manage_class_dropdown['values'] = self.get_class_display_names()
            self.manage_class_dropdown.set("Select Class")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load classes: {e}")
            logger.error(f"Failed to load classes: {e}")

    def format_schedule(self, schedule_dict):
        """
        Format the schedule dictionary into a readable string.
        """
        if not isinstance(schedule_dict, dict):
            logger.error(f"Expected schedule to be a dict, got {type(schedule_dict)} instead.")
            raise TypeError(f"Schedule must be a dictionary, got {type(schedule_dict)}.")

        schedule_str = ""
        for day, times in schedule_dict.items():
            times_formatted = ", ".join(times)
            schedule_str += f"{day}: {times_formatted}\n"
        return schedule_str.strip()

    def populate_update_fields(self, event=None):
        """
        Populate the update fields based on the selected class.
        """
        selected_class = self.manage_class_dropdown.get()
        if not selected_class or selected_class == "Select Class":
            return

        try:
            class_id = selected_class.split("(ID: ")[1].rstrip(")")
        except IndexError:
            messagebox.showerror("Error", "Invalid class selection.")
            logger.error("Populate Update Fields failed: Invalid class selection format.")
            return

        classes = ClassActivityManager.view_all_classes()
        cls = next((c for c in classes if c["class_id"] == class_id), None)
        if not cls:
            messagebox.showerror("Error", "Selected class not found.")
            logger.error(f"Populate Update Fields failed: Class ID {class_id} not found.")
            return

        selected_field = self.update_field_dropdown.get()
        if selected_field == "Trainer":
            trainers = self.get_training_staff_names(cls["gym_id"])
            trainer_display = f"{cls['trainer_name']} (ID: {cls['trainer_id']})"
            self.update_value_entry.configure(state="disabled")
            trainer_combobox = ttk.Combobox(self.view_tab, values=trainers, state="readonly")
            trainer_combobox.set(trainer_display)
            trainer_combobox.grid(row=2, column=1, padx=5, pady=5, sticky="w")
            self.update_value_entry = trainer_combobox
        elif selected_field == "Schedule":
            self.update_value_entry.delete(0, tk.END)
            schedule_str = self.format_schedule(cls["schedule"])
            self.update_value_entry.insert(0, schedule_str)
        elif selected_field == "Capacity":
            self.update_value_entry.delete(0, tk.END)
            self.update_value_entry.insert(0, str(cls["capacity"]))
        else:
            self.update_value_entry.delete(0, tk.END)
        logger.debug(f"Update fields populated for class '{class_id}'.")

    def update_class(self):
        """
        Update the selected class with new values.
        """
        selected_class = self.manage_class_dropdown.get()
        field = self.update_field_dropdown.get()
        new_value = self.update_value_entry.get().strip()

        if not selected_class or selected_class == "Select Class":
            messagebox.showwarning("Validation Error", "Please select a class to update.")
            logger.warning("Update Class failed: No class selected.")
            return
        if not field or field == "Select Field":
            messagebox.showwarning("Validation Error", "Please select a field to update.")
            logger.warning("Update Class failed: No field selected.")
            return
        if not new_value:
            messagebox.showwarning("Validation Error", "Please enter a new value for the selected field.")
            logger.warning("Update Class failed: New value is empty.")
            return

        try:
            class_id = selected_class.split("(ID: ")[1].rstrip(")")
        except IndexError:
            messagebox.showerror("Error", "Invalid class selection.")
            logger.error("Update Class failed: Invalid class selection format.")
            return

        updates = {}
        if field == "Trainer":
            try:
                trainer_id = new_value.split("(ID: ")[1].rstrip(")")
                updates["trainer_id"] = trainer_id
            except IndexError:
                messagebox.showerror("Error", "Invalid trainer format. Use 'Name (ID: xxx)'.")
                logger.error("Update Class failed: Invalid trainer format.")
                return
        elif field == "Schedule":
            try:
                schedule_dict = {}
                lines = new_value.split("\n")
                for line in lines:
                    if ':' not in line:
                        raise ValueError(f"Invalid schedule line format: '{line}'. Expected 'Day: time1, time2'.")
                    day_part, times_part = line.split(":")
                    day = day_part.strip()
                    times = [t.strip() for t in times_part.split(",")]
                    schedule_dict[day] = times
                validated_schedule = ClassActivityManager.validate_schedule(schedule_dict)
                updates["schedule"] = validated_schedule
            except Exception as e:
                messagebox.showerror("Error", f"Invalid schedule format: {e}")
                logger.error(f"Update Class failed: {e}")
                return
        elif field == "Capacity":
            if not new_value.isdigit() or int(new_value) <= 0:
                messagebox.showwarning("Validation Error", "Please enter a valid capacity.")
                logger.warning("Update Class failed: Invalid capacity entered.")
                return
            updates["capacity"] = int(new_value)
        else:
            messagebox.showerror("Error", f"Field '{field}' cannot be updated.")
            logger.error(f"Update Class failed: Field '{field}' cannot be updated.")
            return

        confirm = messagebox.askyesno("Confirm Update", f"Are you sure you want to update the {field} of the selected class?")
        if not confirm:
            logger.info(f"Update Class operation canceled by user for class '{class_id}'.")
            return

        try:
            ClassActivityManager.update_class(class_id, updates)
            messagebox.showinfo("Success", "Class updated successfully.")
            logger.info(f"Class '{class_id}' updated successfully with changes: {updates}")
            self.view_all_classes()
            self.refresh_manage_class_dropdown()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update class: {e}")
            logger.error(f"Failed to update class '{class_id}': {e}")

    def delete_class(self):
        """
        Delete the selected class.
        """
        selected_class = self.manage_class_dropdown.get()
        if not selected_class or selected_class == "Select Class":
            messagebox.showwarning("Validation Error", "Please select a class to delete.")
            logger.warning("Delete Class failed: No class selected.")
            return

        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete the selected class?")
        if not confirm:
            logger.info("Delete Class operation canceled by user.")
            return

        try:
            class_id = selected_class.split("(ID: ")[1].rstrip(")")
        except IndexError:
            messagebox.showerror("Error", "Invalid class selection.")
            logger.error("Delete Class failed: Invalid class selection format.")
            return

        try:
            ClassActivityManager.delete_class(class_id)
            messagebox.showinfo("Success", "Class deleted successfully.")
            logger.info(f"Class '{class_id}' deleted successfully.")
            self.view_all_classes()
            self.refresh_manage_class_dropdown()
            self.manage_class_dropdown.set("Select Class")
            self.update_field_dropdown.set("Select Field")
            self.update_value_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete class: {e}")
            logger.error(f"Failed to delete class '{class_id}': {e}")

    def refresh_manage_class_dropdown(self):
        """
        Refresh the manage_class_dropdown with the latest class names.
        """
        try:
            classes = ClassActivityManager.view_all_classes()
            class_display = [f"{cls['class_name']} (ID: {cls['class_id']})" for cls in classes]
            self.manage_class_dropdown['values'] = class_display
            logger.debug(f"manage_class_dropdown refreshed with: {class_display}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh class dropdown: {e}")
            logger.error(f"Failed to refresh class dropdown: {e}")
'''
if __name__ == "__main__":
    root = tk.Tk()
    app = ClassManagementApp(root)
    app.pack(expand=True, fill='both')
    root.mainloop()
'''



"""import tkinter as tk
from tkinter import ttk, messagebox
from core.class_activity_manager import ClassActivityManager
from core.gym_management import GymManager
from core.member_management import MemberManagement
import logging
import re

# Define constants for days and time slots
DAYS_OF_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
TIME_SLOTS = [
    "06:00-07:00", "07:00-08:00", "08:00-09:00",
    "09:00-10:00", "10:00-11:00", "11:00-12:00",
    "12:00-13:00", "13:00-14:00", "14:00-15:00",
    "15:00-16:00", "16:00-17:00", "17:00-18:00",
    "18:00-19:00", "19:00-20:00", "20:00-21:00",
    "21:00-22:00", "22:00-23:00", "23:00-00:00"
]

# Configure logging
logging.basicConfig(
    filename='logs/class_activity_tk_manager.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ClassManagementApp(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # Removed self.root.title(...) since we now use a Frame as parent
        self.create_widgets()

    def create_widgets(self):
        # Tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")

        self.add_tab = ttk.Frame(self.notebook)
        self.view_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.add_tab, text="Add Class")
        self.notebook.add(self.view_tab, text="View/Manage Classes")

        self.create_add_tab()
        self.create_view_tab()

    def create_add_tab(self):
        """
       # Create the Add Class tab with all required fields.
"""
        for widget in self.add_tab.winfo_children():
            widget.destroy()

        ttk.Label(self.add_tab, text="Add New Class", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=4, pady=10)

        # 1.1 Class Name
        ttk.Label(self.add_tab, text="Class Name:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.class_name_entry = ttk.Entry(self.add_tab)
        self.class_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # 1.2 Select Gym by Gym Name using Drop-down Menu
        ttk.Label(self.add_tab, text="Select Gym:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.gym_dropdown = ttk.Combobox(self.add_tab, values=self.get_gym_display_names(), state="readonly")
        self.gym_dropdown.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.gym_dropdown.set("Select Gym")

        # Bind gym selection to update trainer dropdown
        self.gym_dropdown.bind("<<ComboboxSelected>>", self.update_trainer_dropdown)

        # 1.3 Select Training Staff by Name using Drop-down Menu
        ttk.Label(self.add_tab, text="Select Trainer:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.trainer_dropdown = ttk.Combobox(self.add_tab, values=[], state="readonly")
        self.trainer_dropdown.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        self.trainer_dropdown.set("Select Trainer")

        # Bind trainer selection to update schedule
        self.trainer_dropdown.bind("<<ComboboxSelected>>", self.update_trainer_schedule)

        # 1.4 Retrieve Date/Time from Training Staff: Display in a Table
        ttk.Label(self.add_tab, text="Trainer Schedule:").grid(row=4, column=0, padx=5, pady=5, sticky="ne")
        self.trainer_schedule_tree = ttk.Treeview(self.add_tab, columns=("Schedule"), show="headings", height=5)
        self.trainer_schedule_tree.heading("Schedule", text="Schedule")
        self.trainer_schedule_tree.column("Schedule", width=200, anchor="center")
        self.trainer_schedule_tree.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        # 1.5 Add Schedule Table: Ability to Add Further Classes
        ttk.Label(self.add_tab, text="Add Additional Schedules:").grid(row=5, column=0, padx=5, pady=5, sticky="ne")
        self.additional_schedule_frame = ttk.Frame(self.add_tab)
        self.additional_schedule_frame.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        self.schedule_entries = []
        self.add_schedule_row()  # Add initial schedule row

        add_schedule_button = ttk.Button(self.additional_schedule_frame, text="Add Another Schedule", command=self.add_schedule_row)
        add_schedule_button.grid(row=100, column=0, columnspan=4, pady=5)

        # 1.6 Enter Class Capacity: Limit Gym Users to Attend the Class
        ttk.Label(self.add_tab, text="Class Capacity:").grid(row=6, column=0, padx=5, pady=5, sticky="e")
        self.capacity_entry = ttk.Entry(self.add_tab)
        self.capacity_entry.grid(row=6, column=1, padx=5, pady=5, sticky="w")

        # 1.7 Add Class Button: Parse Information to Update the Schedule Database
        add_class_button = ttk.Button(self.add_tab, text="Add Class", command=self.add_class)
        add_class_button.grid(row=7, column=0, columnspan=4, pady=10)

        # 1.8 Add a Refresh Button to reload gyms and clear trainer schedule
        refresh_button = ttk.Button(self.add_tab, text="Refresh", command=self.refresh_add_tab)
        refresh_button.grid(row=8, column=0, columnspan=4, pady=5)

    def create_view_tab(self):
        """
#        Create the View/Manage Classes tab with all required functionalities.
"""
        for widget in self.view_tab.winfo_children():
            widget.destroy()

        ttk.Label(self.view_tab, text="View and Manage Classes", font=("Helvetica", 16)).pack(pady=10)

        # 2.1 Display Table with Class Details
        self.classes_tree = ttk.Treeview(
            self.view_tab,
            columns=("ID", "Name", "Trainer", "Gym", "Schedule", "Capacity", "Registered Users"),
            show="headings",
            selectmode="browse"
        )
        self.classes_tree.heading("ID", text="Class ID")
        self.classes_tree.heading("Name", text="Class Name")
        self.classes_tree.heading("Trainer", text="Trainer Name")
        self.classes_tree.heading("Gym", text="Gym Name")
        self.classes_tree.heading("Schedule", text="Schedule")
        self.classes_tree.heading("Capacity", text="Capacity")
        self.classes_tree.heading("Registered Users", text="Registered Users")
        self.classes_tree.pack(expand=True, fill="both", padx=10, pady=10)

        # 2.2 Refresh Button to Load Classes
        refresh_button = ttk.Button(self.view_tab, text="Refresh", command=self.view_all_classes)
        refresh_button.pack(pady=5)

        # 2.3 Update/Delete Frame
        manage_frame = ttk.Frame(self.view_tab)
        manage_frame.pack(pady=5)

        # 2.4 Update Class Functionality
        ttk.Label(manage_frame, text="Select Class:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.manage_class_dropdown = ttk.Combobox(manage_frame, values=self.get_class_display_names(), state="readonly")
        self.manage_class_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.manage_class_dropdown.set("Select Class")
        self.manage_class_dropdown.bind("<<ComboboxSelected>>", self.populate_update_fields)

        ttk.Label(manage_frame, text="Field to Update:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.update_field_dropdown = ttk.Combobox(
            manage_frame,
            values=["Trainer", "Schedule", "Capacity"],
            state="readonly"
        )
        self.update_field_dropdown.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.update_field_dropdown.set("Select Field")

        ttk.Label(manage_frame, text="New Value:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.update_value_entry = ttk.Entry(manage_frame)
        self.update_value_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        update_button = ttk.Button(manage_frame, text="Update Class", command=self.update_class)
        update_button.grid(row=3, column=0, padx=5, pady=5)

        # 2.5 Delete Class Functionality
        delete_button = ttk.Button(manage_frame, text="Delete Class", command=self.delete_class)
        delete_button.grid(row=3, column=1, padx=5, pady=5)

        # Load all classes initially
        self.view_all_classes()

    def refresh_add_tab(self):
        """
#        Refresh the Add Class tab: re-fetch gyms and clear trainer schedule.
"""
        self.gym_dropdown['values'] = self.get_gym_display_names()
        self.gym_dropdown.set("Select Gym")
        self.trainer_dropdown['values'] = []
        self.trainer_dropdown.set("Select Trainer")
        for row in self.trainer_schedule_tree.get_children():
            self.trainer_schedule_tree.delete(row)
        # Also clear schedules if needed
        for day_cb, time_cb in self.schedule_entries:
            day_cb.set("Select Day")
            time_cb.set("Select Time")
        self.class_name_entry.delete(0, tk.END)
        self.capacity_entry.delete(0, tk.END)
        messagebox.showinfo("Refreshed", "Add Class tab refreshed.")

    def create_main_menu(self):
        """
#        Navigate back to the main menu. Placeholder for actual main menu implementation.
"""
        messagebox.showinfo("Info", "Return to main menu functionality to be implemented.")

    def get_gym_display_names(self):
        """
#        Retrieve all gym names formatted with their IDs.
"""
        gyms = GymManager.view_all_gyms()
        gym_display = [f"{gym['gym_name']} (ID: {gym['gym_id']})" for gym in gyms]
        logger.debug(f"Retrieved gym display names: {gym_display}")
        return gym_display

    def get_training_staff_names(self, gym_id=None):
        """
#Retrieve all training staff names, optionally filtered by gym_id.
"""
        members = MemberManagement.view_all_members()
        training_staff = [m for m in members if m["user_type"] == "Training Staff"]
        if gym_id:
            training_staff = [m for m in training_staff if m["gym_id"] == gym_id]
        trainers_display = [f"{staff['name']} (ID: {staff['member_id']})" for staff in training_staff]
        logger.debug(f"Retrieved training staff names for gym '{gym_id}': {trainers_display}")
        return trainers_display

    def get_class_display_names(self):
        """
 #Retrieve all classes formatted with their IDs.
"""
        classes = ClassActivityManager.view_all_classes()
        class_display = [f"{cls['class_name']} (ID: {cls['class_id']})" for cls in classes]
        logger.debug(f"Retrieved class display names: {class_display}")
        return class_display

    def update_trainer_dropdown(self, event=None):
        """
#        Update the trainer dropdown based on the selected gym.
"""
        selected_gym = self.gym_dropdown.get()
        if not selected_gym or selected_gym == "Select Gym":
            self.trainer_dropdown['values'] = []
            self.trainer_dropdown.set("Select Trainer")
            # Clear trainer schedule
            for row in self.trainer_schedule_tree.get_children():
                self.trainer_schedule_tree.delete(row)
            logger.debug("No gym selected. Trainer dropdown cleared.")
            return

        # Extract gym_id from selection
        try:
            gym_id = selected_gym.split("(ID: ")[1].rstrip(")")
        except IndexError:
            messagebox.showerror("Error", "Invalid gym selection format.")
            logger.error("Invalid gym selection format.")
            return

        trainers = self.get_training_staff_names(gym_id)
        self.trainer_dropdown['values'] = trainers
        self.trainer_dropdown.set("Select Trainer")
        logger.debug(f"Trainer dropdown updated for gym '{gym_id}': {trainers}")

        # Clear trainer schedule
        for row in self.trainer_schedule_tree.get_children():
            self.trainer_schedule_tree.delete(row)

    def update_trainer_schedule(self, event=None):
        """
#        Update the trainer schedule table based on selected trainer.
"""
        selected_trainer = self.trainer_dropdown.get()
        if not selected_trainer or selected_trainer == "Select Trainer":
            for row in self.trainer_schedule_tree.get_children():
                self.trainer_schedule_tree.delete(row)
            logger.debug("No trainer selected. Trainer schedule cleared.")
            return

        try:
            trainer_id = selected_trainer.split("(ID: ")[1].rstrip(")")
        except IndexError:
            messagebox.showerror("Error", "Invalid trainer selection format.")
            logger.error("Invalid trainer selection format.")
            return

        schedules = ClassActivityManager.get_trainer_schedule(trainer_id)

        for row in self.trainer_schedule_tree.get_children():
            self.trainer_schedule_tree.delete(row)

        for sched in schedules:
            try:
                formatted_sched = self.format_schedule_for_display(sched)
                self.trainer_schedule_tree.insert("", "end", values=(formatted_sched,))
            except Exception as e:
                logger.error(f"Failed to format schedule for display: {e}")
                continue
        logger.debug(f"Trainer schedule updated for trainer '{trainer_id}': {schedules}")

    def format_schedule_for_display(self, schedule_list):
"""
#Format the schedule list into a readable string.
"""
        schedule_str = ""
        for sched in schedule_list:
            if not isinstance(sched, dict):
                logger.error(f"Expected schedule to be a dict, got {type(sched)} instead.")
                continue
            for day, times in sched.items():
                times_formatted = ", ".join(times)
                schedule_str += f"{day}: {times_formatted}\n"
        return schedule_str.strip()

    def add_schedule_row(self):
"""
#Add a new schedule entry row in the Add Class tab.
"""
        row = len(self.schedule_entries)
        ttk.Label(self.additional_schedule_frame, text=f"Schedule {row + 1} Day:").grid(row=row, column=0, padx=5, pady=2, sticky="e")
        day_combobox = ttk.Combobox(self.additional_schedule_frame, values=DAYS_OF_WEEK, state="readonly")
        day_combobox.grid(row=row, column=1, padx=5, pady=2, sticky="w")
        day_combobox.set("Select Day")

        ttk.Label(self.additional_schedule_frame, text=f"Schedule {row + 1} Time:").grid(row=row, column=2, padx=5, pady=2, sticky="e")
        time_combobox = ttk.Combobox(self.additional_schedule_frame, values=TIME_SLOTS, state="readonly")
        time_combobox.grid(row=row, column=3, padx=5, pady=2, sticky="w")
        time_combobox.set("Select Time")

        self.schedule_entries.append((day_combobox, time_combobox))
        logger.debug(f"Added new schedule row: Day Combobox - {day_combobox}, Time Combobox - {time_combobox}")

    def add_class(self):
"""
#Gather information from the Add Class form and add a new class.
"""
        class_name = self.class_name_entry.get().strip()
        selected_gym = self.gym_dropdown.get()
        selected_trainer = self.trainer_dropdown.get()
        capacity = self.capacity_entry.get().strip()

        if not class_name:
            messagebox.showwarning("Validation Error", "Please enter the class name.")
            logger.warning("Add Class failed: Class name is empty.")
            return
        if not selected_gym or selected_gym == "Select Gym":
            messagebox.showwarning("Validation Error", "Please select a gym.")
            logger.warning("Add Class failed: Gym not selected.")
            return
        if not selected_trainer or selected_trainer == "Select Trainer":
            messagebox.showwarning("Validation Error", "Please select a trainer.")
            logger.warning("Add Class failed: Trainer not selected.")
            return
        if not capacity.isdigit() or int(capacity) <= 0:
            messagebox.showwarning("Validation Error", "Please enter a valid class capacity.")
            logger.warning("Add Class failed: Invalid capacity entered.")
            return

        try:
            gym_id = selected_gym.split("(ID: ")[1].rstrip(")")
            trainer_id = selected_trainer.split("(ID: ")[1].rstrip(")")
        except IndexError:
            messagebox.showerror("Error", "Invalid selection format for gym or trainer.")
            logger.error("Add Class failed: Invalid selection format for gym or trainer.")
            return

        additional_schedules = {}
        for day_cb, time_cb in self.schedule_entries:
            day = day_cb.get().strip()
            time = time_cb.get().strip()
            if day != "Select Day" and time != "Select Time":
                if day not in additional_schedules:
                    additional_schedules[day] = []
                additional_schedules[day].append(time)

        existing_schedules = ClassActivityManager.get_trainer_schedule(trainer_id)
        existing_schedule_times = []
        for sched in existing_schedules:
            if not isinstance(sched, dict):
                logger.error(f"Expected schedule to be a dict, got {type(sched)} instead.")
                continue
            for day, times in sched.items():
                for t in times:
                    existing_schedule_times.append(f"{day} {t}")

        logger.debug(f"Existing schedules for trainer '{trainer_id}': {existing_schedule_times}")

        for day, times in additional_schedules.items():
            for t in times:
                schedule_entry = f"{day} {t}"
                if schedule_entry in existing_schedule_times:
                    messagebox.showwarning("Validation Error", f"Schedule conflict detected: {schedule_entry}")
                    logger.warning(f"Add Class failed: Schedule conflict for {schedule_entry}")
                    return

        final_schedule = additional_schedules
        try:
            validated_schedule = ClassActivityManager.validate_schedule(final_schedule)
        except ValueError as ve:
            messagebox.showerror("Validation Error", str(ve))
            logger.error(f"Add Class failed during schedule validation: {ve}")
            return

        capacity_int = int(capacity)

        try:
            class_id = ClassActivityManager.add_class(
                class_name=class_name,
                trainer_id=trainer_id,
                schedule=validated_schedule,
                capacity=capacity_int,
                gym_id=gym_id
            )
            messagebox.showinfo("Success", f"Class '{class_name}' added successfully with ID: {class_id}.")
            logger.info(f"Class '{class_name}' added successfully with ID: {class_id}.")
            self.clear_add_class_form()
            self.view_all_classes()
            self.refresh_manage_class_dropdown()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add class: {e}")
            logger.error(f"Failed to add class '{class_name}': {e}")

    def clear_add_class_form(self):
"""
#Clear all input fields in the Add Class form.
"""
        self.class_name_entry.delete(0, tk.END)
        self.gym_dropdown.set("Select Gym")
        self.trainer_dropdown.set("Select Trainer")
        for day_cb, time_cb in self.schedule_entries:
            day_cb.set("Select Day")
            time_cb.set("Select Time")
        self.capacity_entry.delete(0, tk.END)

        for row in self.trainer_schedule_tree.get_children():
            self.trainer_schedule_tree.delete(row)
        logger.debug("Add Class form cleared.")

    def view_all_classes(self):
"""
#Populate the classes_tree with all classes from the database.
"""
        try:
            classes = ClassActivityManager.view_all_classes()
            for row in self.classes_tree.get_children():
                self.classes_tree.delete(row)
            for cls in classes:
                registered_count = len(cls.get("registered_users", []))
                schedule_formatted = self.format_schedule(cls["schedule"])
                self.classes_tree.insert(
                    "",
                    "end",
                    values=(
                        cls["class_id"],
                        cls["class_name"],
                        cls["trainer_name"],
                        cls["gym_name"],
                        schedule_formatted,
                        cls["capacity"],
                        registered_count
                    ),
                )
            logger.info("Classes loaded into the view successfully.")
            self.manage_class_dropdown['values'] = self.get_class_display_names()
            self.manage_class_dropdown.set("Select Class")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load classes: {e}")
            logger.error(f"Failed to load classes: {e}")

    def format_schedule(self, schedule_dict):
"""
#Format the schedule dictionary into a readable string.
"""
        if not isinstance(schedule_dict, dict):
            logger.error(f"Expected schedule to be a dict, got {type(schedule_dict)} instead.")
            raise TypeError(f"Schedule must be a dictionary, got {type(schedule_dict)}.")

        schedule_str = ""
        for day, times in schedule_dict.items():
            times_formatted = ", ".join(times)
            schedule_str += f"{day}: {times_formatted}\n"
        return schedule_str.strip()

    def populate_update_fields(self, event=None):
"""
#Populate the update fields based on the selected class.
"""
        selected_class = self.manage_class_dropdown.get()
        if not selected_class or selected_class == "Select Class":
            return

        try:
            class_id = selected_class.split("(ID: ")[1].rstrip(")")
        except IndexError:
            messagebox.showerror("Error", "Invalid class selection.")
            logger.error("Populate Update Fields failed: Invalid class selection format.")
            return

        classes = ClassActivityManager.view_all_classes()
        cls = next((c for c in classes if c["class_id"] == class_id), None)
        if not cls:
            messagebox.showerror("Error", "Selected class not found.")
            logger.error(f"Populate Update Fields failed: Class ID {class_id} not found.")
            return

        selected_field = self.update_field_dropdown.get()
        if selected_field == "Trainer":
            trainers = self.get_training_staff_names(cls["gym_id"])
            trainer_display = f"{cls['trainer_name']} (ID: {cls['trainer_id']})"
            self.update_value_entry.configure(state="disabled")
            trainer_combobox = ttk.Combobox(self.view_tab, values=trainers, state="readonly")
            trainer_combobox.set(trainer_display)
            trainer_combobox.grid(row=2, column=1, padx=5, pady=5, sticky="w")
            self.update_value_entry = trainer_combobox
        elif selected_field == "Schedule":
            self.update_value_entry.delete(0, tk.END)
            schedule_str = self.format_schedule(cls["schedule"])
            self.update_value_entry.insert(0, schedule_str)
        elif selected_field == "Capacity":
            self.update_value_entry.delete(0, tk.END)
            self.update_value_entry.insert(0, str(cls["capacity"]))
        else:
            self.update_value_entry.delete(0, tk.END)
        logger.debug(f"Update fields populated for class '{class_id}'.")

    def update_class(self):
"""
#Update the selected class with new values.
"""
        selected_class = self.manage_class_dropdown.get()
        field = self.update_field_dropdown.get()
        new_value = self.update_value_entry.get().strip()

        if not selected_class or selected_class == "Select Class":
            messagebox.showwarning("Validation Error", "Please select a class to update.")
            logger.warning("Update Class failed: No class selected.")
            return
        if not field or field == "Select Field":
            messagebox.showwarning("Validation Error", "Please select a field to update.")
            logger.warning("Update Class failed: No field selected.")
            return
        if not new_value:
            messagebox.showwarning("Validation Error", "Please enter a new value for the selected field.")
            logger.warning("Update Class failed: New value is empty.")
            return

        try:
            class_id = selected_class.split("(ID: ")[1].rstrip(")")
        except IndexError:
            messagebox.showerror("Error", "Invalid class selection.")
            logger.error("Update Class failed: Invalid class selection format.")
            return

        updates = {}
        if field == "Trainer":
            try:
                trainer_id = new_value.split("(ID: ")[1].rstrip(")")
                updates["trainer_id"] = trainer_id
            except IndexError:
                messagebox.showerror("Error", "Invalid trainer format. Use 'Name (ID: xxx)'.")
                logger.error("Update Class failed: Invalid trainer format.")
                return
        elif field == "Schedule":
            try:
                schedule_dict = {}
                lines = new_value.split("\n")
                for line in lines:
                    if ':' not in line:
                        raise ValueError(f"Invalid schedule line format: '{line}'. Expected 'Day: time1, time2'.")
                    day_part, times_part = line.split(":")
                    day = day_part.strip()
                    times = [t.strip() for t in times_part.split(",")]
                    schedule_dict[day] = times
                validated_schedule = ClassActivityManager.validate_schedule(schedule_dict)
                updates["schedule"] = validated_schedule
            except Exception as e:
                messagebox.showerror("Error", f"Invalid schedule format: {e}")
                logger.error(f"Update Class failed: {e}")
                return
        elif field == "Capacity":
            if not new_value.isdigit() or int(new_value) <= 0:
                messagebox.showwarning("Validation Error", "Please enter a valid capacity.")
                logger.warning("Update Class failed: Invalid capacity entered.")
                return
            updates["capacity"] = int(new_value)
        else:
            messagebox.showerror("Error", f"Field '{field}' cannot be updated.")
            logger.error(f"Update Class failed: Field '{field}' cannot be updated.")
            return

        confirm = messagebox.askyesno("Confirm Update", f"Are you sure you want to update the {field} of the selected class?")
        if not confirm:
            logger.info(f"Update Class operation canceled by user for class '{class_id}'.")
            return

        try:
            ClassActivityManager.update_class(class_id, updates)
            messagebox.showinfo("Success", "Class updated successfully.")
            logger.info(f"Class '{class_id}' updated successfully with changes: {updates}")
            self.view_all_classes()
            self.refresh_manage_class_dropdown()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update class: {e}")
            logger.error(f"Failed to update class '{class_id}': {e}")

    def delete_class(self):
"""
#Delete the selected class.
"""
        selected_class = self.manage_class_dropdown.get()
        if not selected_class or selected_class == "Select Class":
            messagebox.showwarning("Validation Error", "Please select a class to delete.")
            logger.warning("Delete Class failed: No class selected.")
            return

        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete the selected class?")
        if not confirm:
            logger.info("Delete Class operation canceled by user.")
            return

        try:
            class_id = selected_class.split("(ID: ")[1].rstrip(")")
        except IndexError:
            messagebox.showerror("Error", "Invalid class selection.")
            logger.error("Delete Class failed: Invalid class selection format.")
            return

        try:
            ClassActivityManager.delete_class(class_id)
            messagebox.showinfo("Success", "Class deleted successfully.")
            logger.info(f"Class '{class_id}' deleted successfully.")
            self.view_all_classes()
            self.refresh_manage_class_dropdown()
            self.manage_class_dropdown.set("Select Class")
            self.update_field_dropdown.set("Select Field")
            self.update_value_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete class: {e}")
            logger.error(f"Failed to delete class '{class_id}': {e}")

    def refresh_manage_class_dropdown(self):
"""
#Refresh the manage_class_dropdown with the latest class names.
"""
        try:
            classes = ClassActivityManager.view_all_classes()
            class_display = [f"{cls['class_name']} (ID: {cls['class_id']})" for cls in classes]
            self.manage_class_dropdown['values'] = class_display
            logger.debug(f"manage_class_dropdown refreshed with: {class_display}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh class dropdown: {e}")
            logger.error(f"Failed to refresh class dropdown: {e}")
'''
if __name__ == "__main__":
    root = tk.Tk()
    app = ClassManagementApp(root)
    app.pack(expand=True, fill='both')
    root.mainloop()
'''"""