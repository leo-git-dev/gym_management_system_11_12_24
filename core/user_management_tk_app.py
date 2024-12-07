import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from core.member_management import MemberManagement
from core.gym_management import GymManager


class UserManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("User Management System")
        self.root.geometry("800x600")
        self.create_main_menu()

######### HERE WE CREATE THE MAIN MENU FUNCTION ###############

    def create_main_menu(self):
        """
        Create the main menu with user management options.
        """
        self.clear_root_widgets()

        frame = ttk.Frame(self.root)
        frame.grid(sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)

        ttk.Label(frame, text="User Management System", font=("Helvetica", 16)).grid(row=0, column=0, pady=20)
        ttk.Button(frame, text="Add User", command=self.create_add_user_menu).grid(row=1, column=0, pady=10)
        ttk.Button(frame, text="View All Users", command=self.create_view_all_users_menu).grid(row=2, column=0, pady=10)
        ttk.Button(frame, text="Search User", command=self.create_search_user_menu).grid(row=3, column=0, pady=10)
        ttk.Button(frame, text="Update User", command=self.create_update_user_menu).grid(row=4, column=0, pady=10)
        ttk.Button(frame, text="Delete User", command=self.create_delete_user_menu).grid(row=5, column=0, pady=10)

######### HERE WE CREATE THE ADD MENU FUNCTION ###############


    def create_add_user_menu(self):
        """
        Redirect to the Add User functionality.
        """
        self.clear_root_widgets()

        frame = ttk.Frame(self.root)
        frame.grid(sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)

        ttk.Label(frame, text="Add User", font=("Helvetica", 14)).grid(row=0, column=0, pady=10)

        user_type_dropdown = ttk.Combobox(frame, values=["Gym User", "Training Staff", "Wellbeing Staff", "Management Staff"])
        user_type_dropdown.grid(row=1, column=0, pady=10)
        user_type_dropdown.set("Select User Type")

        ttk.Button(frame, text="Next", command=lambda: self.load_user_type_menu(user_type_dropdown.get())).grid(row=2, column=0, pady=10)
        self.add_back_button(frame)

    def load_user_type_menu(self, user_type):
        """
        Load the appropriate menu for user type.
        """
        if user_type == "Gym User":
            self.create_gym_user_menu()
        elif user_type == "Training Staff":
            self.create_training_staff_menu()
        elif user_type == "Wellbeing Staff":
            self.create_wellbeing_staff_menu()
        elif user_type == "Management Staff":
            self.create_management_staff_menu()
        else:
            messagebox.showerror("Error", "Please select a valid user type.")

######### HERE WE CREATE THE GYM USER MENU FUNCTION ###############

    def create_gym_user_menu(self):
        """
        Create the form for adding a gym user.
        """
        self.clear_root_widgets()

        frame = ttk.Frame(self.root)
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

        self.add_back_button(frame)

######### HERE WE CREATE THE ADD TRAINING STAFF MENU FUNCTION ###############


    def create_training_staff_menu(self):
        """
        Create the menu for adding training staff.
        """
        self.clear_root_widgets()

        frame = ttk.Frame(self.root)
        frame.grid(sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_columnconfigure(2, weight=1)
        frame.grid_columnconfigure(3, weight=1)

        ttk.Label(frame, text="Add Training Staff", font=("Helvetica", 14)).grid(row=0, column=0, columnspan=4, pady=10)

        ttk.Label(frame, text="Name:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        name_entry = ttk.Entry(frame)
        name_entry.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky="w")

        ttk.Label(frame, text="Gym:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        gym_dropdown = ttk.Combobox(frame, values=self.get_gym_names())
        gym_dropdown.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky="w")

        ttk.Label(frame, text="Expertise:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        expertise_entry = ttk.Entry(frame)
        expertise_entry.grid(row=3, column=1, columnspan=3, padx=5, pady=5, sticky="w")

        # Schedule Section
        ttk.Label(frame, text="Day of Week:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        day_of_week_dropdown = ttk.Combobox(
            frame,
            values=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        )
        day_of_week_dropdown.grid(row=4, column=1, columnspan=3, padx=5, pady=5, sticky="w")

        ttk.Label(frame, text="Start Time:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        start_time_entry = ttk.Entry(frame, width=10)
        start_time_entry.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(frame, text="End Time:").grid(row=5, column=2, padx=5, pady=5, sticky="e")
        end_time_entry = ttk.Entry(frame, width=10)
        end_time_entry.grid(row=5, column=3, padx=5, pady=5, sticky="w")

        ttk.Button(frame, text="Add Training Staff", command=lambda: self.add_training_staff(
            name=name_entry.get(),
            gym=gym_dropdown.get(),
            expertise=expertise_entry.get(),
            schedule={
                "day_of_week": day_of_week_dropdown.get(),
                "start_time": start_time_entry.get(),
                "end_time": end_time_entry.get()
            }
        )).grid(row=6, column=0, columnspan=4, pady=10)

        # Add Back button at the end
        self.add_back_button(frame)

######### HERE WE CREATE THE ADD WELLBEING STAFF MENU FUNCTION ###############

    def create_wellbeing_staff_menu(self):
        """
        Create the form for adding wellbeing staff.
        """
        self.clear_root_widgets()

        frame = ttk.Frame(self.root)
        frame.grid(sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        ttk.Label(frame, text="Add Wellbeing Staff", font=("Helvetica", 14)).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(frame, text="Name:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        name_entry = ttk.Entry(frame)
        name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(frame, text="Gym:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        gym_dropdown = ttk.Combobox(frame, values=self.get_gym_names())
        gym_dropdown.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(frame, text="Activity:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        activity_dropdown = ttk.Combobox(frame, values=["Physiotherapy", "Nutrition"])
        activity_dropdown.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        self.add_schedule_fields(frame)

######### HERE WE CREATE THE SCHEDULE MENU FUNCTION ###############

    def add_schedule_fields(self, frame):
        """
        Add fields for entering a schedule.
        """
        ttk.Label(frame, text="Day of Week:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.day_of_week_dropdown = ttk.Combobox(frame, values=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        self.day_of_week_dropdown.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(frame, text="Start Time:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.start_time_entry = ttk.Entry(frame)
        self.start_time_entry.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(frame, text="End Time:").grid(row=5, column=3, padx=5, pady=5, sticky="e")
        self.end_time_entry = ttk.Entry(frame)
        self.end_time_entry.grid(row=5, column=5, padx=5, pady=5, sticky="w")

        ttk.Button(frame, text="Add Wellbeing Staff", command=lambda: self.add_wellbeing_staff(
            name=name_entry.get(),
            gym=gym_dropdown.get(),
            activity=activity_dropdown.get(),
            schedule={
                "day_of_week": self.day_of_week_dropdown.get(),
                "start_time": self.start_time_entry.get(),
                "end_time": self.end_time_entry.get()
            }
        )).grid(row=6, column=0, columnspan=4, pady=10)

        # Add Back button at the end
        self.add_back_button(frame)

    def get_schedule_data(self):
        """
        Retrieve schedule data from the UI fields.
        """
        return {
            "day_of_week": self.day_of_week_dropdown.get(),
            "start_time": self.start_time_entry.get(),
            "end_time": self.end_time_entry.get(),
        }

######### HERE WE CREATE THE ADD GYM USER MENU FUNCTION ###############

    def add_gym_user(self, name, gym, membership_type, join_date):
        """
        Add a gym user to the database.
        """
        try:
            gym_data = self.get_gym_by_name(gym)
            if not gym_data:
                raise ValueError("Invalid gym selected.")

            cost = MemberManagement.calculate_membership_cost(membership_type)
            MemberManagement.add_member(
                name=name,
                user_type="Gym User",
                gym_id=gym_data["gym_id"],
                membership_type=membership_type,
                cost=cost,
                join_date=join_date,
            )
            messagebox.showinfo("Success", "Gym user added successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add gym user: {e}")


######### HERE WE CREATE THE ADD TRAINING STAFF MENU FUNCTION ###############

    def add_training_staff(self, name, gym, expertise, schedule):
        """
        Add training staff to the database.
        """
        try:
            # Validate inputs
            if not name or not gym or not expertise:
                raise ValueError("All fields are required.")
            if not schedule.get("day_of_week") or not schedule.get("start_time") or not schedule.get("end_time"):
                raise ValueError("Complete schedule information is required.")

            gym_data = self.get_gym_by_name(gym)
            if not gym_data:
                raise ValueError("Invalid gym selected.")

            MemberManagement.add_member(
                name=name,
                user_type="Training Staff",
                gym_id=gym_data["gym_id"],
                expertise=expertise,
                schedule=schedule,
                cost=4000,
            )
            messagebox.showinfo("Success", "Training staff added successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add training staff: {e}")


######### HERE WE CREATE THE ADD WELLBEING STAFF MENU FUNCTION ###############

    def add_wellbeing_staff(self, name, gym, activity, schedule):
        """
        Add wellbeing staff to the database.
        """
        try:
            gym_data = self.get_gym_by_name(gym)
            if not gym_data:
                raise ValueError("Invalid gym selected.")

            MemberManagement.add_member(
                name=name,
                user_type="Wellbeing Staff",
                gym_id=gym_data["gym_id"],
                activity=activity,
                schedule=schedule,
                cost=4500,
            )
            messagebox.showinfo("Success", "Wellbeing staff added successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add wellbeing staff: {e}")


######### HERE WE CREATE THE RETURN GYM BY NAME FUNCTION ###############


    def get_gym_by_name(self, gym_name):
        """
        Retrieve a gym by its name.
        """
        gyms = GymManager.view_all_gyms()
        return next((gym for gym in gyms if gym["gym_name"] == gym_name), None)

    def get_gym_names(self):
        """
        Retrieve all gym names from the database.
        """
        gyms = GymManager.view_all_gyms()
        return [gym["gym_name"] for gym in gyms]

    def clear_root_widgets(self):
        """
        Clear all widgets in the root window.
        """
        for widget in self.root.winfo_children():
            widget.destroy()


######### HERE WE CREATE THE VIEW ALL GYM USERS MENU FUNCTION ###############

    def create_view_all_users_menu(self):
        """
        View all users in the system.
        """
        self.clear_root_widgets()

        # Create a frame for the view menu
        frame = ttk.Frame(self.root)
        frame.grid(sticky="nsew", padx=10, pady=10)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(1, weight=1)

        # Label for the title
        ttk.Label(frame, text="All Users", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=3, pady=10)

        # Treeview for displaying users
        users_tree = ttk.Treeview(
            frame, columns=("ID", "Name", "User Type", "Gym", "Cost"), show="headings", height=15
        )
        users_tree.heading("ID", text="ID")
        users_tree.heading("Name", text="Name")
        users_tree.heading("User Type", text="User Type")
        users_tree.heading("Gym", text="Gym")
        users_tree.heading("Cost", text="Cost")
        users_tree.grid(row=1, column=0, columnspan=2, sticky="nsew")

        # Add a vertical scrollbar
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=users_tree.yview)
        users_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=1, column=2, sticky="ns")

        # Refresh Button
        ttk.Button(
            frame, text="Refresh", command=lambda: self.refresh_users_tree(users_tree)
        ).grid(row=2, column=0, columnspan=2, pady=10)

        # Populate the treeview
        self.refresh_users_tree(users_tree)

        # Add the Back button
        self.add_back_button(frame)

    def refresh_users_tree(self, tree):
        """
        Refresh the user tree with data from the database.
        """
        tree.delete(*tree.get_children())
        try:
            # Fetch all members from the database
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
                        member.get("cost", "N/A"),
                    ),
                )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load users: {e}")

######### HERE WE CREATE THE ADD MANAGEMENT STAFF MENU FUNCTION ###############

    def create_management_staff_menu(self):
        """
        Create the form for adding management staff.
        """
        self.clear_root_widgets()

        frame = ttk.Frame(self.root)
        frame.grid(sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        ttk.Label(frame, text="Add Management Staff", font=("Helvetica", 14)).grid(row=0, column=0, columnspan=2,
                                                                                   pady=10)

        ttk.Label(frame, text="Name:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        name_entry = ttk.Entry(frame)
        name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(frame, text="Gym:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        gym_dropdown = ttk.Combobox(frame, values=self.get_gym_names())
        gym_dropdown.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(frame, text="Role:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        role_dropdown = ttk.Combobox(frame, values=["Reception", "Cleaning", "Cafeteria", "Security"])
        role_dropdown.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        ttk.Button(frame, text="Add Management Staff", command=lambda: self.add_management_staff(
            name=name_entry.get(),
            gym=gym_dropdown.get(),
            role=role_dropdown.get(),
        )).grid(row=4, column=0, columnspan=2, pady=10)

        self.add_back_button(frame)

######### HERE WE CREATE THE ADD MANAGEMENT STAFF MENU FUNCTION ###############

    def add_management_staff(self, name, gym, role):
        """
        Add management staff to the database.
        """
        try:
            gym_data = self.get_gym_by_name(gym)
            if not gym_data:
                raise ValueError("Invalid gym selected.")

            MemberManagement.add_member(
                name=name,
                user_type="Management Staff",
                gym_id=gym_data["gym_id"],
                role=role,
                cost=2500
            )
            messagebox.showinfo("Success", "Management staff added successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add management staff: {e}")

    def add_back_button(self, frame):
        """
        Add a 'Back' button to return to the main menu.
        """
        ttk.Button(frame, text="Back", command=self.create_main_menu).grid(row=8, column=0, columnspan=2, pady=10,
                                                                           sticky="ew")

######### HERE WE CREATE THE SEARCH GYM USER MENU FUNCTION ###############


    def create_search_user_menu(self):
        """
        Search users by ID or Name.
        """
        self.clear_root_widgets()

        frame = ttk.Frame(self.root)
        frame.grid(sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(3, weight=1)

        ttk.Label(frame, text="Search User", font=("Helvetica", 14)).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(frame, text="Member ID:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        search_id_entry = ttk.Entry(frame)
        search_id_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(frame, text="Name:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        search_name_entry = ttk.Entry(frame)
        search_name_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        results_box = tk.Text(frame, wrap="word", height=15)
        results_box.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        ttk.Button(
            frame,
            text="Search",
            command=lambda: self.search_user(
                search_id_entry.get(),
                search_name_entry.get(),
                results_box
            )
        ).grid(row=4, column=0, columnspan=2, pady=10)

        self.add_back_button(frame)

    def search_user(self, member_id, name, results_box):
        """
        Search for a user by Member ID or Name and display the results.
        """
        try:
            results_box.delete("1.0", tk.END)  # Clear the results box
            if not member_id and not name:
                results_box.insert(tk.END, "Please provide at least Member ID or Name to search.")
                return

            user = MemberManagement.search_member(member_id=member_id, name=name)
            if user:
                results_box.insert(tk.END, f"Member Found:\n{user}\n")
            else:
                results_box.insert(tk.END, "No matching user found.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to search user: {e}")

######### HERE WE CREATE THE UPDATE GYM USER DATA MENU FUNCTION ###############

    def update_user(self, member_id=None, name=None, field=None, new_value=None):
        """
        Update a specific field of a user's details in the database.
        """
        try:
            if not (member_id or name) or not field or not new_value:
                messagebox.showerror("Error",
                                     "Please select Member ID or Name, Field to Update, and enter a New Value.")
                return

            # Fetch member by ID or Name
            member = None
            if member_id:
                member = MemberManagement.search_member(member_id=member_id)
            elif name:
                member = MemberManagement.search_member(name=name)

            if not member:
                messagebox.showerror("Error", "No matching member found.")
                return

            # Perform the update
            success = MemberManagement.update_member(member["member_id"], {field: new_value})
            if success:
                messagebox.showinfo("Success", f"Updated {field} for Member ID {member['member_id']}.")
            else:
                messagebox.showerror("Error", "Failed to update user. User may not exist.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update user: {e}")

    def get_all_member_ids(self):
        """
        Retrieve all member IDs from the database.
        """
        try:
            members = MemberManagement.view_all_members()
            return [member.get("member_id") for member in members if member.get("member_id")]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch member IDs: {e}")
            return []

    def get_all_member_names(self):
        """
        Retrieve all member names from the database.
        """
        try:
            members = MemberManagement.view_all_members()
            return [member.get("name") for member in members if member.get("name")]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch member names: {e}")
            return []

    def create_update_user_menu(self):
        """
        Create a menu for updating user information.
        """
        self.clear_root_widgets()

        frame = ttk.Frame(self.root)
        frame.grid(sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(5, weight=1)

        ttk.Label(frame, text="Update User", font=("Helvetica", 14)).grid(row=0, column=0, columnspan=2, pady=10)

        # Dropdown to select a user by name
        ttk.Label(frame, text="Select User:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.user_name_dropdown = ttk.Combobox(frame, values=self.get_all_member_names(), state="readonly")
        self.user_name_dropdown.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.user_name_dropdown.bind("<<ComboboxSelected>>", self.display_user_info)

        # Table to display user information
        self.info_table = ttk.Treeview(frame, columns=("Field", "Value"), show="headings", height=5)
        self.info_table.heading("Field", text="Field")
        self.info_table.heading("Value", text="Value")
        self.info_table.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Dropdown to select a field to update
        ttk.Label(frame, text="Field to Update:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.field_dropdown = ttk.Combobox(frame, values=[], state="readonly")
        self.field_dropdown.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Entry for new value
        ttk.Label(frame, text="New Value:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.new_value_entry = ttk.Entry(frame)
        self.new_value_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        # Update Button
        ttk.Button(
            frame,
            text="Update",
            command=lambda: self.update_user(
                name=self.user_name_dropdown.get(),
                field=self.field_dropdown.get(),
                new_value=self.new_value_entry.get()
            )
        ).grid(row=6, column=0, columnspan=2, pady=10)

        # Back Button
        self.add_back_button(frame)

    def display_user_info(self, event):
        """
        Populate the table with the selected user's information and load available fields.
        """
        selected_name = self.user_name_dropdown.get()
        member = MemberManagement.search_member(name=selected_name)

        if not member:
            messagebox.showerror("Error", "No member data found.")
            return

        # Clear existing data
        self.info_table.delete(*self.info_table.get_children())

        # Populate the table with user information
        for field, value in member.items():
            self.info_table.insert("", "end", values=(field, value))

        # Populate fields dropdown
        self.field_dropdown["values"] = list(member.keys())

    def get_all_member_names(self):
        """
        Retrieve all member names from the database.
        """
        try:
            members = MemberManagement.view_all_members()
            return [member.get("name") for member in members if member.get("name")]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch member names: {e}")
            return []

######### HERE WE CREATE THE DELETE GYM USER DATA MENU FUNCTION ###############

    def create_delete_user_menu(self):
        """
        Create the menu for deleting users.
        """
        self.clear_root_widgets()

        frame = ttk.Frame(self.root)
        frame.grid(sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(2, weight=1)

        ttk.Label(frame, text="Delete User", font=("Helvetica", 14)).grid(row=0, column=0, columnspan=2, pady=10)

        # Dropdown for Member Name
        ttk.Label(frame, text="Select User Name:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.member_name_dropdown = ttk.Combobox(frame, values=self.get_all_member_names(), state="readonly")
        self.member_name_dropdown.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.member_name_dropdown.bind("<<ComboboxSelected>>", self.populate_user_details)

        # Table view for user details
        self.details_frame = ttk.Frame(frame)
        self.details_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

        # Delete Button
        ttk.Button(
            frame,
            text="Delete User",
            command=lambda: self.delete_user_and_return(name=self.member_name_dropdown.get())
        ).grid(row=3, column=0, columnspan=2, pady=10)

    def delete_user_and_return(self, name=None):
        """
        Delete a user from the database and navigate back to the main menu.
        """
        try:
            if not name:
                messagebox.showerror("Error", "Please select a user to delete.")
                return

            # Attempt to delete the user by name
            success = MemberManagement.delete_member_by_name(name)

            if success:
                messagebox.showinfo("Success", f"User '{name}' deleted successfully.")
                self.create_main_menu()  # Automatically navigate back to the main menu
            else:
                messagebox.showerror("Error", "User not found or could not be deleted.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete user: {e}")

    def populate_user_details(self, event=None):
        """
        Populate the table view with user details based on the selected name.
        """
        # Clear previous details
        for widget in self.details_frame.winfo_children():
            widget.destroy()

        user_name = self.member_name_dropdown.get()
        user = MemberManagement.search_member(name=user_name)

        if not user:
            ttk.Label(self.details_frame, text="No details found for the selected user.").grid(row=0, column=0)
            return

        # Create a table-like display of user details
        headers = ["Field", "Value"]
        for col, header in enumerate(headers):
            ttk.Label(self.details_frame, text=header, font=("Helvetica", 10, "bold")).grid(row=0, column=col, padx=5,
                                                                                            pady=5)

        for row, (field, value) in enumerate(user.items(), start=1):
            ttk.Label(self.details_frame, text=field).grid(row=row, column=0, padx=5, pady=5, sticky="w")
            ttk.Label(self.details_frame, text=value).grid(row=row, column=1, padx=5, pady=5, sticky="w")


if __name__ == "__main__":
    root = tk.Tk()
    app = UserManagementApp(root)
    root.mainloop()

