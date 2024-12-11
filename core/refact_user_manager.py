# core/user_management.py

import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from core.member_management import MemberManagement
from core.gym_management import GymManager
import re
from database.data_loader import DataLoader

def is_valid_zone_name(zone_name):
    """Validate the zone name."""
    if len(zone_name) < 3 or len(zone_name) > 30:
        return False
    if not re.match("^[A-Za-z0-9 ]+$", zone_name):
        return False
    return True

class UserManagementFrame(ttk.Frame):
    def __init__(self, parent, data_loader:DataLoader):
        super().__init__(parent)
        self.parent = parent  # The Notebook
        self.create_widgets()

    def create_widgets(self):
        # Create Main Menu Tab
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")

        # Create Tabs
        self.main_menu_tab = ttk.Frame(self.notebook)
        self.add_user_tab = ttk.Frame(self.notebook)
        self.view_users_tab = ttk.Frame(self.notebook)
        self.search_user_tab = ttk.Frame(self.notebook)
        self.update_user_tab = ttk.Frame(self.notebook)
        self.delete_user_tab = ttk.Frame(self.notebook)

        # Add Tabs to Notebook
        self.notebook.add(self.main_menu_tab, text="Main Menu")
        self.notebook.add(self.add_user_tab, text="Add User")
        self.notebook.add(self.view_users_tab, text="View All Users")
        self.notebook.add(self.search_user_tab, text="Search User")
        self.notebook.add(self.update_user_tab, text="Update User")
        self.notebook.add(self.delete_user_tab, text="Delete User")

        # Bind tab change to update title if needed
        # self.notebook.bind("<<NotebookTabChanged>>", lambda e: self.update_title())

        # Initialize Tabs
        self.create_main_menu_tab()
        self.create_add_user_tab()
        self.create_view_all_users_tab()
        self.create_search_user_tab()
        self.create_update_user_tab()
        self.create_delete_user_tab()

    def create_main_menu_tab(self):
        frame = ttk.Frame(self.main_menu_tab)
        frame.pack(expand=True, fill="both")
        frame.grid_columnconfigure(0, weight=1)

        ttk.Label(frame, text="User Management System", font=("Helvetica", 16)).grid(row=0, column=0, pady=20)
        ttk.Button(frame, text="Add User", command=lambda: self.notebook.select(self.add_user_tab)).grid(row=1, column=0, pady=10)
        ttk.Button(frame, text="View All Users", command=lambda: self.notebook.select(self.view_users_tab)).grid(row=2, column=0, pady=10)
        ttk.Button(frame, text="Search User", command=lambda: self.notebook.select(self.search_user_tab)).grid(row=3, column=0, pady=10)
        ttk.Button(frame, text="Update User", command=lambda: self.notebook.select(self.update_user_tab)).grid(row=4, column=0, pady=10)
        ttk.Button(frame, text="Delete User", command=lambda: self.notebook.select(self.delete_user_tab)).grid(row=5, column=0, pady=10)

    # Add User Tab
    def create_add_user_tab(self):
        frame = ttk.Frame(self.add_user_tab)
        frame.grid(sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)

        ttk.Label(frame, text="Add User", font=("Helvetica", 14)).grid(row=0, column=0, pady=10)

        user_type_dropdown = ttk.Combobox(frame, values=["Gym User", "Training Staff", "Wellbeing Staff", "Management Staff"])
        user_type_dropdown.grid(row=1, column=0, pady=10)
        user_type_dropdown.set("Select User Type")

        ttk.Button(frame, text="Next", command=lambda: self.load_user_type_menu(user_type_dropdown.get())).grid(row=2, column=0, pady=10)
        self.add_back_button(frame, row=3, col_span=1)

    def load_user_type_menu(self, user_type):
        if user_type == "Gym User":
            self.notebook.select(self.add_user_tab)
            self.show_gym_user_menu()
        elif user_type == "Training Staff":
            self.notebook.select(self.add_user_tab)
            self.show_training_staff_menu()
        elif user_type == "Wellbeing Staff":
            self.notebook.select(self.add_user_tab)
            self.show_wellbeing_staff_menu()
        elif user_type == "Management Staff":
            self.notebook.select(self.add_user_tab)
            self.show_management_staff_menu()
        else:
            messagebox.showerror("Error", "Please select a valid user type.")

    def show_gym_user_menu(self):
        # Clear previous widgets in add_user_tab
        for widget in self.add_user_tab.winfo_children():
            widget.destroy()

        frame = ttk.Frame(self.add_user_tab)
        frame.grid(sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        ttk.Label(frame, text="Add Gym User", font=("Helvetica", 14)).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(frame, text="Name:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        name_entry = ttk.Entry(frame)
        name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(frame, text="Gym:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        gym_dropdown = ttk.Combobox(frame, values=self.get_gym_names())
        gym_dropdown.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(frame, text="Membership Type:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        membership_dropdown = ttk.Combobox(frame, values=["Trial", "Standard", "Weekender", "Premium"])
        membership_dropdown.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(frame, text="Join Date:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        join_date_calendar = Calendar(frame, selectmode="day", date_pattern="yyyy-mm-dd")
        join_date_calendar.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        ttk.Button(frame, text="Add Gym User", command=lambda: self.add_gym_user(
            name=name_entry.get(),
            gym=gym_dropdown.get(),
            membership_type=membership_dropdown.get(),
            join_date=join_date_calendar.get_date(),
        )).grid(row=5, column=0, columnspan=2, pady=10)

        self.add_back_button(frame, row=6, col_span=2)

    def add_gym_user(self, name, gym, membership_type, join_date):
        try:
            gym_data = self.get_gym_by_name(gym)
            if not gym_data:
                raise ValueError("Invalid gym selected.")

            # Ensure we include city from gym_data
            city = gym_data.get("city", "Unknown")

            cost = MemberManagement.calculate_membership_cost(membership_type)
            MemberManagement.add_member(
                name=name,
                user_type="Gym User",
                gym_id=gym_data["gym_id"],
                membership_type=membership_type,
                cost=cost,
                join_date=join_date,
                city=city
            )
            messagebox.showinfo("Success", "Gym user added successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add gym user: {e}")

            # Reset the form by returning to main menu
            self.notebook.select(self.main_menu_tab)
            self.create_main_menu_tab()
        except ValueError as ve:
            messagebox.showwarning("Validation Error", str(ve))
            logger.warning(f"Validation error while adding gym user: {ve}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add gym user: {e}")
            logger.error(f"Error while adding gym user: {e}")


    # Training Staff Tab
    def show_training_staff_menu(self):
        # Clear previous widgets in add_user_tab
        for widget in self.add_user_tab.winfo_children():
            widget.destroy()

        frame = ttk.Frame(self.add_user_tab)
        frame.grid(sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_columnconfigure(2, weight=1)

        ttk.Label(frame, text="Add Training Staff", font=("Helvetica", 14)).grid(row=0, column=0, columnspan=3, pady=10)

        # Name
        ttk.Label(frame, text="Name:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        name_entry = ttk.Entry(frame)
        name_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="w")

        # Gym
        ttk.Label(frame, text="Gym:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        gym_dropdown = ttk.Combobox(frame, values=self.get_gym_names(), state="readonly")
        gym_dropdown.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky="w")

        # Expertise
        ttk.Label(frame, text="Expertise:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        expertise_entry = ttk.Entry(frame)
        expertise_entry.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky="w")

        # Schedule Table
        self.create_schedule_table(frame, 4, name_entry, gym_dropdown, expertise_entry, "Training Staff")

    # Wellbeing Staff Tab
    def show_wellbeing_staff_menu(self):
        # Clear previous widgets in add_user_tab
        for widget in self.add_user_tab.winfo_children():
            widget.destroy()

        frame = ttk.Frame(self.add_user_tab)
        frame.grid(sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        ttk.Label(frame, text="Add Wellbeing Staff", font=("Helvetica", 14)).grid(row=0, column=0, columnspan=2, pady=10)

        # Name
        ttk.Label(frame, text="Name:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        name_entry = ttk.Entry(frame)
        name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Gym
        ttk.Label(frame, text="Gym:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        gym_dropdown = ttk.Combobox(frame, values=self.get_gym_names(), state="readonly")
        gym_dropdown.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Activity
        ttk.Label(frame, text="Activity:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        activity_dropdown = ttk.Combobox(frame, values=["Physiotherapy", "Nutrition"], state="readonly")
        activity_dropdown.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Schedule Table
        self.create_schedule_table(frame, 4, name_entry, gym_dropdown, activity_dropdown, "Wellbeing Staff")

    # Management Staff Tab
    def show_management_staff_menu(self):
        # Clear previous widgets in add_user_tab
        for widget in self.add_user_tab.winfo_children():
            widget.destroy()

        frame = ttk.Frame(self.add_user_tab)
        frame.grid(sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        ttk.Label(frame, text="Add Management Staff", font=("Helvetica", 14)).grid(row=0, column=0, columnspan=2, pady=10)

        # Name
        ttk.Label(frame, text="Name:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        name_entry = ttk.Entry(frame)
        name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Gym
        ttk.Label(frame, text="Gym:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        gym_dropdown = ttk.Combobox(frame, values=self.get_gym_names(), state="readonly")
        gym_dropdown.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Role
        ttk.Label(frame, text="Role:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        role_dropdown = ttk.Combobox(frame, values=["Reception", "Cleaning", "Cafeteria", "Security"], state="readonly")
        role_dropdown.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        ttk.Button(
            frame,
            text="Add Management Staff",
            command=lambda: self.add_management_staff(
                name=name_entry.get(),
                gym=gym_dropdown.get(),
                role=role_dropdown.get(),
            )
        ).grid(row=4, column=0, columnspan=2, pady=10)

        self.add_back_button(frame, row=5, col_span=2)

    def add_management_staff(self, name, gym, role):
        try:
            if not name or not gym or not role:
                raise ValueError("All fields are required.")

            gym_data = self.get_gym_by_name(gym)
            if not gym_data:
                raise ValueError("Invalid gym selected.")

            city = gym_data.get("city", "Unknown")

            MemberManagement.add_member(
                name=name,
                user_type="Management Staff",
                gym_id=gym_data["gym_id"],
                role=role,
                cost=2500,
                city=city
            )
            messagebox.showinfo("Success", "Management staff added successfully.")

            # Reset the form by returning to main menu
            self.notebook.select(self.main_menu_tab)
            self.create_main_menu_tab()

        except ValueError as ve:
            messagebox.showwarning("Validation Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add management staff: {e}")

    # Schedule Table Creation
    def create_schedule_table(self, frame, start_row, name_entry, gym_dropdown, extra_field, user_type):
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        time_intervals = self.generate_time_intervals()
        day_entries = {}

        # Table headers
        ttk.Label(frame, text="Day").grid(row=start_row, column=0, padx=5, pady=5, sticky="e")
        ttk.Label(frame, text="Start Time").grid(row=start_row, column=1, padx=5, pady=5, sticky="w")
        ttk.Label(frame, text="End Time").grid(row=start_row, column=2, padx=5, pady=5, sticky="w")

        for i, day in enumerate(days, start=start_row+1):
            ttk.Label(frame, text=day).grid(row=i, column=0, padx=5, pady=5, sticky="e")
            start_cb = ttk.Combobox(frame, values=time_intervals, state="readonly")
            start_cb.grid(row=i, column=1, padx=5, pady=5, sticky="w")

            end_cb = ttk.Combobox(frame, values=time_intervals, state="readonly")
            end_cb.grid(row=i, column=2, padx=5, pady=5, sticky="w")

            day_entries[day] = (start_cb, end_cb)

        #Save schedule button
        ttk.Button(
            frame, text="Save Schedule",
            command=lambda: self.save_schedule(name_entry, gym_dropdown, extra_field, day_entries, user_type)
        ).grid(row=i+1, column=0, columnspan=3, pady=10)

        self.add_back_button(frame, row=i+2, col_span=3)


    def save_schedule(self, name_entry, gym_dropdown, extra_field, day_entries, user_type):
        schedule = {}
        for day, (start_cb, end_cb) in day_entries.items():
            start_time = start_cb.get()
            end_time = end_cb.get()
            if start_time and end_time:
                if end_time <= start_time:
                    messagebox.showerror("Validation Error", f"End time must be later than start time for {day}.")
                    return
                schedule[day] = [{"start_time": start_time, "end_time": end_time}]
            else:
                schedule[day] = []

        self.add_user_with_schedule(name_entry, gym_dropdown, extra_field, schedule, user_type)

    # Search User Tab
    def create_search_user_tab(self):
        frame = ttk.Frame(self.search_user_tab)
        frame.grid(sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(3, weight=1)

        ttk.Label(frame, text="Search User by Name", font=("Helvetica", 14)).grid(
            row=0, column=0, columnspan=2, pady=10
        )

        ttk.Label(frame, text="User Type:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.user_type_dropdown = ttk.Combobox(
            frame, values=["Gym User", "Training Staff", "Wellbeing Staff", "Management Staff"], state="readonly"
        )
        self.user_type_dropdown.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.user_type_dropdown.set("Select User Type")

        ttk.Label(frame, text="Name:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.name_dropdown = ttk.Combobox(frame, state="readonly")
        self.name_dropdown.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.name_dropdown.set("Select Name")

        self.user_type_dropdown.bind("<<ComboboxSelected>>", self.on_user_type_selected)

        result_frame = ttk.Frame(frame)
        result_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        result_frame.grid_rowconfigure(0, weight=1)
        result_frame.grid_columnconfigure(0, weight=1)

        canvas = tk.Canvas(result_frame)
        canvas.grid(row=0, column=0, sticky="nsew")

        scroll_y = ttk.Scrollbar(result_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scroll_y.set)
        scroll_y.grid(row=0, column=1, sticky="ns")

        self.result_inner_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=self.result_inner_frame, anchor="nw")
        self.result_inner_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.configure(yscrollcommand=scroll_y.set)

        ttk.Button(
            frame,
            text="Search",
            command=lambda: self.search_user_by_name(
                self.user_type_dropdown.get(),
                self.name_dropdown.get(),
                self.result_inner_frame,
            ),
        ).grid(row=4, column=0, columnspan=2, pady=10)

        self.add_back_button(frame, row=5, col_span=2)

    def on_user_type_selected(self, event):
        user_type = self.user_type_dropdown.get()
        names = self.get_names_by_user_type(user_type)
        self.name_dropdown["values"] = names
        self.name_dropdown.set("Select Name")

    def get_names_by_user_type(self, user_type):
        try:
            users = MemberManagement.view_all_members()
            return [u["name"] for u in users if u["user_type"] == user_type]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch names: {e}")
            return []

    def search_user_by_name(self, user_type, name, result_frame):
        try:
            for widget in result_frame.winfo_children():
                widget.destroy()

            if not user_type or user_type == "Select User Type":
                raise ValueError("Please select a valid user type.")
            if not name or name == "Select Name":
                raise ValueError("Please select a name to search.")

            users = MemberManagement.view_all_members()
            user = next((u for u in users if u["name"] == name and u["user_type"] == user_type), None)

            if not user:
                ttk.Label(result_frame, text="No matching user found.", font=("Helvetica", 12)).pack(pady=10)
                return

            schedule = self.format_schedule(user.get("schedule"))

            details = [
                ("ID", user["member_id"]),
                ("Name", user["name"]),
                ("User Type", user["user_type"]),
                ("Gym Name", user.get("gym_name", "Unknown")),
                ("City", user.get("city", "Unknown")),
                ("Cost", f"${float(user.get('cost', 0)):.2f}"),
                ("Schedule", schedule),
            ]

            for field, value in details:
                ttk.Label(result_frame, text=field, font=("Helvetica", 10, "bold")).pack(anchor="w", pady=2)
                ttk.Label(result_frame, text=value, font=("Helvetica", 10)).pack(anchor="w", padx=10)

        except ValueError as ve:
            messagebox.showwarning("Validation Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to search user: {e}")

    def format_schedule(self, schedule):
        if not schedule or not isinstance(schedule, dict):
            return "No schedule available."
        formatted = []
        for day, intervals in schedule.items():
            if isinstance(intervals, list):
                for interval in intervals:
                    formatted.append(f"{day}: {interval['start_time']} - {interval['end_time']}")
            else:
                # Old single-interval format
                if "start_time" in intervals and "end_time" in intervals:
                    formatted.append(f"{day}: {intervals['start_time']} - {intervals['end_time']}")
                else:
                    formatted.append(f"{day}: No valid intervals")
        return "\n".join(formatted)

    # Update User Tab
    def create_update_user_tab(self):
        frame = ttk.Frame(self.update_user_tab)
        frame.grid(sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(5, weight=1)

        ttk.Label(frame, text="Update User", font=("Helvetica", 14)).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(frame, text="Select User:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.user_name_dropdown = ttk.Combobox(frame, values=self.get_all_member_names(), state="readonly")
        self.user_name_dropdown.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.user_name_dropdown.bind("<<ComboboxSelected>>", self.display_user_info)

        self.info_table = ttk.Treeview(frame, columns=("Field", "Value"), show="headings", height=5)
        self.info_table.heading("Field", text="Field")
        self.info_table.heading("Value", text="Value")
        self.info_table.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        ttk.Label(frame, text="Field to Update:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.field_dropdown = ttk.Combobox(frame, values=[], state="readonly")
        self.field_dropdown.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(frame, text="New Value:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.new_value_entry = ttk.Entry(frame)
        self.new_value_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        ttk.Button(
            frame,
            text="Update",
            command=lambda: self.update_user(
                name=self.user_name_dropdown.get(),
                field=self.field_dropdown.get(),
                new_value=self.new_value_entry.get()
            )
        ).grid(row=6, column=0, columnspan=2, pady=10)

        self.add_back_button(frame, row=7, col_span=2)

    def display_user_info(self, event):
        selected_name = self.user_name_dropdown.get()
        member = MemberManagement.search_member(name=selected_name)

        if not member:
            messagebox.showerror("Error", "No member data found.")
            return

        self.info_table.delete(*self.info_table.get_children())

        for field, value in member.items():
            self.info_table.insert("", "end", values=(field, value))

        self.field_dropdown["values"] = list(member.keys())

    # Delete User Tab
    def create_delete_user_tab(self):
        frame = ttk.Frame(self.delete_user_tab)
        frame.grid(sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(2, weight=1)

        ttk.Label(frame, text="Delete User", font=("Helvetica", 14)).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(frame, text="Select User Name:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.member_name_dropdown = ttk.Combobox(frame, values=self.get_all_member_names(), state="readonly")
        self.member_name_dropdown.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Button(
            frame,
            text="Delete User",
            command=lambda: self.delete_user_and_return(name=self.member_name_dropdown.get())
        ).grid(row=3, column=0, columnspan=2, pady=10)

        self.add_back_button(frame, row=4, col_span=2)

    def delete_user_and_return(self, name=None):
        try:
            if not name:
                messagebox.showerror("Error", "Please select a user to delete.")
                return

            success = MemberManagement.delete_member_by_name(name)

            if success:
                messagebox.showinfo("Success", f"User '{name}' deleted successfully.")
                self.notebook.select(self.main_menu_tab)
            else:
                messagebox.showerror("Error", "User not found or could not be deleted.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete user: {e}")

    # View All Users Tab
    def create_view_all_users_tab(self):
        frame = ttk.Frame(self.view_users_tab)
        frame.grid(sticky="nsew", padx=10, pady=10)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(1, weight=1)

        ttk.Label(frame, text="All Users", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=3, pady=10)

        users_tree = ttk.Treeview(
            frame, columns=("ID", "Name", "User Type", "Gym", "Cost"), show="headings", height=15
        )
        users_tree.heading("ID", text="ID")
        users_tree.heading("Name", text="Name")
        users_tree.heading("User Type", text="User Type")
        users_tree.heading("Gym", text="Gym")
        users_tree.heading("Cost", text="Cost")
        users_tree.grid(row=1, column=0, columnspan=2, sticky="nsew")

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=users_tree.yview)
        users_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=1, column=2, sticky="ns")

        ttk.Button(
            frame, text="Refresh", command=lambda: self.refresh_users_tree(users_tree)
        ).grid(row=2, column=0, columnspan=2, pady=10)

        self.refresh_users_tree(users_tree)
        self.add_back_button(frame, row=3, col_span=3)

    def refresh_users_tree(self, tree):
        tree.delete(*tree.get_children())
        try:
            members = MemberManagement.view_all_members()
            for member in members:
                tree.insert(
                    "",
                    "end",
                    values=(
                        member.get("member_id", "N/A"),
                        member.get("name", "N/A"),
                        member.get("user_type", "N/A"),
                        member.get("gym_name", "N/A"),
                        f"${float(member.get('cost', 0)):.2f}",
                    ),
                )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load users: {e}")

    # Update User Method
    def update_user(self, name, field, new_value):
        try:
            if not name or not field or not new_value:
                raise ValueError("Please select a user, field, and provide a new value.")

            # Search the member by name
            member = MemberManagement.search_member(name=name)
            if not member:
                raise ValueError(f"No member found with name: {name}")

            member_id = member["member_id"]
            updates = {field: new_value}

            success = MemberManagement.update_member(member_id, updates)

            if success:
                messagebox.showinfo("Success", "User updated successfully.")
            else:
                messagebox.showerror("Error", "Failed to update user.")
        except ValueError as ve:
            messagebox.showwarning("Validation Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    # Utility Methods
    def get_gym_names(self):
        try:
            gyms = GymManager.view_all_gyms()
            return [gym["gym_name"] for gym in gyms]
        except Exception:
            return []

    def get_gym_by_name(self, gym_name):
        try:
            gyms = GymManager.view_all_gyms()
            return next((gym for gym in gyms if gym["gym_name"] == gym_name), None)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch gym details: {e}")
            return None

    def get_all_member_names(self):
        try:
            members = MemberManagement.view_all_members()
            return [member["name"] for member in members if "name" in member]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch member names: {e}")
            return []

    def add_back_button(self, frame, row=10, col_span=1):
        ttk.Button(
            frame, text="Back", command=lambda: self.notebook.select(self.main_menu_tab)
        ).grid(row=row, column=0, columnspan=col_span, pady=10, sticky="ew")
