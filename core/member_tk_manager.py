import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from core.member_management import MemberManagement
from core.gym_management import GymManager


class UserManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("User Management")
        self.create_main_menu()

    def create_main_menu(self):
        """
        Create the main menu with user management options.
        """
        self.clear_root_widgets()

        ttk.Label(self.root, text="User Management System", font=("Helvetica", 16)).pack(pady=10)

        ttk.Button(self.root, text="Add User", command=self.create_add_user_menu).pack(pady=5)
        ttk.Button(self.root, text="View All Users", command=self.create_view_all_users_menu).pack(pady=5)
        ttk.Button(self.root, text="Search User", command=self.create_search_user_menu).pack(pady=5)
        ttk.Button(self.root, text="Update/Delete User", command=self.create_update_delete_user_menu).pack(pady=5)

    def create_add_user_menu(self):
        """
        Create the menu for adding a user.
        """
        self.clear_root_widgets()

        ttk.Label(self.root, text="Add User").pack(pady=10)
        user_type_dropdown = ttk.Combobox(
            self.root, values=["Gym User", "Training Staff", "Wellbeing Staff", "Management Staff"]
        )
        user_type_dropdown.pack(pady=10)
        user_type_dropdown.set("Select User Type")

        ttk.Button(
            self.root,
            text="Next",
            command=lambda: self.load_user_type_menu(user_type_dropdown.get())
        ).pack(pady=10)

        self.add_back_button()

    def load_user_type_menu(self, user_type):
        """
        Load the appropriate menu for the selected user type.
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

    def create_gym_user_menu(self):
        """
        Create the menu for adding a Gym User.
        """
        self.clear_root_widgets()

        ttk.Label(self.root, text="Add Gym User", font=("Helvetica", 14)).pack(pady=10)

        ttk.Label(self.root, text="Name:").pack(pady=5)
        name_entry = ttk.Entry(self.root)
        name_entry.pack(pady=5)

        ttk.Label(self.root, text="Gym:").pack(pady=5)
        gym_dropdown = ttk.Combobox(self.root, values=self.get_gym_names())
        gym_dropdown.pack(pady=5)

        ttk.Label(self.root, text="Membership Type:").pack(pady=5)
        membership_dropdown = ttk.Combobox(
            self.root, values=["Trial", "Standard", "Weekender", "Premium"]
        )
        membership_dropdown.pack(pady=5)

        ttk.Label(self.root, text="Join Date:").pack(pady=5)
        join_date_calendar = Calendar(self.root, selectmode="day", date_pattern="yyyy-mm-dd")
        join_date_calendar.pack(pady=5)

        ttk.Button(
            self.root,
            text="Add Gym User",
            command=lambda: self.add_gym_user(
                name=name_entry.get(),
                gym_name=gym_dropdown.get(),
                membership_type=membership_dropdown.get(),
                join_date=join_date_calendar.get_date()
            )
        ).pack(pady=10)

        self.add_back_button()

    def create_training_staff_menu(self):
        """
        Create the menu for adding Training Staff.
        """
        self.clear_root_widgets()

        ttk.Label(self.root, text="Add Training Staff", font=("Helvetica", 14)).pack(pady=10)

        ttk.Label(self.root, text="Name:").pack(pady=5)
        name_entry = ttk.Entry(self.root)
        name_entry.pack(pady=5)

        ttk.Label(self.root, text="Gym:").pack(pady=5)
        gym_dropdown = ttk.Combobox(self.root, values=self.get_gym_names())
        gym_dropdown.pack(pady=5)

        ttk.Label(self.root, text="Expertise:").pack(pady=5)
        expertise_entry = ttk.Entry(self.root)
        expertise_entry.pack(pady=5)

        self.add_schedule_fields()

        ttk.Button(
            self.root,
            text="Add Training Staff",
            command=lambda: self.add_training_staff(
                name=name_entry.get(),
                gym_name=gym_dropdown.get(),
                expertise=expertise_entry.get()
            )
        ).pack(pady=10)

        self.add_back_button()

    def create_wellbeing_staff_menu(self):
        """
        Create the menu for adding Wellbeing Staff.
        """
        self.clear_root_widgets()

        ttk.Label(self.root, text="Add Wellbeing Staff", font=("Helvetica", 14)).pack(pady=10)

        ttk.Label(self.root, text="Name:").pack(pady=5)
        name_entry = ttk.Entry(self.root)
        name_entry.pack(pady=5)

        ttk.Label(self.root, text="Gym:").pack(pady=5)
        gym_dropdown = ttk.Combobox(self.root, values=self.get_gym_names())
        gym_dropdown.pack(pady=5)

        ttk.Label(self.root, text="Activity:").pack(pady=5)
        activity_dropdown = ttk.Combobox(self.root, values=["Physiotherapy", "Nutrition"])
        activity_dropdown.pack(pady=5)

        self.add_schedule_fields()

        ttk.Button(
            self.root,
            text="Add Wellbeing Staff",
            command=lambda: self.add_wellbeing_staff(
                name=name_entry.get(),
                gym_name=gym_dropdown.get(),
                activity=activity_dropdown.get()
            )
        ).pack(pady=10)

        self.add_back_button()

    def create_management_staff_menu(self):
        """
        Create the menu for adding Management Staff.
        """
        self.clear_root_widgets()

        ttk.Label(self.root, text="Add Management Staff", font=("Helvetica", 14)).pack(pady=10)

        ttk.Label(self.root, text="Name:").pack(pady=5)
        name_entry = ttk.Entry(self.root)
        name_entry.pack(pady=5)

        ttk.Label(self.root, text="Gym:").pack(pady=5)
        gym_dropdown = ttk.Combobox(self.root, values=self.get_gym_names())
        gym_dropdown.pack(pady=5)

        ttk.Label(self.root, text="Role:").pack(pady=5)
        role_dropdown = ttk.Combobox(self.root, values=["Reception", "Cleaning", "Cafeteria", "Security"])
        role_dropdown.pack(pady=5)

        ttk.Button(
            self.root,
            text="Add Management Staff",
            command=lambda: self.add_management_staff(
                name=name_entry.get(),
                gym_name=gym_dropdown.get(),
                role=role_dropdown.get()
            )
        ).pack(pady=10)

        self.add_back_button()

    def add_gym_user(self, name, gym_name, membership_type, join_date):
        """
        Add a gym user to the system.
        """
        try:
            gym = self.get_gym_by_name(gym_name)
            if not gym:
                raise ValueError("Invalid gym selected.")

            cost = MemberManagement.calculate_membership_cost(membership_type)
            MemberManagement.add_member(
                name=name,
                user_type="Gym User",
                gym_id=gym["gym_id"],
                membership_type=membership_type,
                cost=cost,
                join_date=join_date
            )
            messagebox.showinfo("Success", "Gym user added successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add gym user: {e}")

    def add_training_staff(self, name, gym_name, expertise):
        """
        Add training staff to the system.
        """
        try:
            gym = self.get_gym_by_name(gym_name)
            if not gym:
                raise ValueError("Invalid gym selected.")

            MemberManagement.add_member(
                name=name,
                user_type="Training Staff",
                gym_id=gym["gym_id"],
                expertise=expertise,
                cost=4000
            )
            messagebox.showinfo("Success", "Training staff added successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add training staff: {e}")

    def add_wellbeing_staff(self, name, gym_name, activity):
        """
        Add wellbeing staff to the system.
        """
        try:
            gym = self.get_gym_by_name(gym_name)
            if not gym:
                raise ValueError("Invalid gym selected.")

            MemberManagement.add_member(
                name=name,
                user_type="Wellbeing Staff",
                gym_id=gym["gym_id"],
                activity=activity,
                cost=4500
            )
            messagebox.showinfo("Success", "Wellbeing staff added successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add wellbeing staff: {e}")

    def get_gym_names(self):
        """
        Retrieve all gym names from the database.
        """
        gyms = GymManager.view_all_gyms()
        return [gym["gym_name"] for gym in gyms]

    def get_gym_by_name(self, gym_name):
        """
        Retrieve gym details by name.
        """
        gyms = GymManager.view_all_gyms()
        return next((gym for gym in gyms if gym["gym_name"] == gym_name), None)

    def add_schedule_fields(self):
        """
        Add schedule-related fields for staff roles.
        """
        ttk.Label(self.root, text="Day of Week:").pack(pady=5)
        day_of_week_dropdown = ttk.Combobox(
            self.root, values=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        )
        day_of_week_dropdown.pack(pady=5)

        ttk.Label(self.root, text="Start Time:").pack(pady=5)
        start_time_entry = ttk.Entry(self.root)
        start_time_entry.pack(pady=5)

        ttk.Label(self.root, text="End Time:").pack(pady=5)
        end_time_entry = ttk.Entry(self.root)
        end_time_entry.pack(pady=5)

    def create_view_all_users_menu(self):
        """
        Create the menu to view all users in the system.
        """
        self.clear_root_widgets()

        ttk.Label(self.root, text="All Users", font=("Helvetica", 16)).pack(pady=10)

        # Frame for the Treeview and scrollbars
        tree_frame = ttk.Frame(self.root)
        tree_frame.pack(expand=True, fill="both", padx=5, pady=5)

        # Scrollbars
        vert_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
        vert_scrollbar.pack(side="right", fill="y")
        horiz_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal")
        horiz_scrollbar.pack(side="bottom", fill="x")

        # Treeview
        self.users_tree = ttk.Treeview(
            tree_frame,
            columns=(
                "ID", "Name", "User Type", "Gym Name", "Membership Type", "Cost", "Join Date"
            ),
            show="headings",
            yscrollcommand=vert_scrollbar.set,
            xscrollcommand=horiz_scrollbar.set,
        )
        self.users_tree.pack(expand=True, fill="both")

        # Configure scrollbars
        vert_scrollbar.config(command=self.users_tree.yview)
        horiz_scrollbar.config(command=self.users_tree.xview)

        # Define headings
        self.users_tree.heading("ID", text="ID")
        self.users_tree.heading("Name", text="Name")
        self.users_tree.heading("User Type", text="User Type")
        self.users_tree.heading("Gym Name", text="Gym Name")
        self.users_tree.heading("Membership Type", text="Membership Type")
        self.users_tree.heading("Cost", text="Cost")
        self.users_tree.heading("Join Date", text="Join Date")

        # Set column widths
        for col in self.users_tree["columns"]:
            self.users_tree.column(col, width=100, anchor="center")

        # Populate the Treeview
        try:
            users = MemberManagement.view_all_members()
            for user in users:
                # Ensure 'cost' is a number and format it, otherwise, leave it as-is
                cost = user.get("cost", "N/A")
                if isinstance(cost, (int, float)):
                    cost = f"${float(cost):.2f}"
                else:
                    cost = str(cost)

                self.users_tree.insert(
                    "",
                    "end",
                    values=(
                        user.get("member_id", "N/A"),
                        user.get("name", "N/A"),
                        user.get("user_type", "N/A"),
                        user.get("gym_name", "N/A"),
                        user.get("membership_type", "N/A"),
                        cost,
                        user.get("join_date", "N/A"),
                    ),
                )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load users: {e}")

        # Back button
        self.add_back_button()

    def load_all_users(self):
        """
        Load all users into the Treeview table.
        """
        try:
            # Clear existing rows
            for row in self.users_tree.get_children():
                self.users_tree.delete(row)

            # Fetch all members from the database
            members = MemberManagement.view_all_members()

            # Add each member to the Treeview
            for member in members:
                self.users_tree.insert(
                    "",
                    "end",
                    values=(
                        member["member_id"],
                        member["name"],
                        member["user_type"],
                        member["gym_name"],
                        member["join_date"],
                        f"${member['cost']:.2f}" if "cost" in member else "N/A",
                    ),
                )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load users: {e}")

    def create_search_user_menu(self):
        """
        Create the menu to search for a user.
        """
        self.clear_root_widgets()

        ttk.Label(self.root, text="Search User", font=("Helvetica", 16)).pack(pady=10)

        # Dropdown to select user
        ttk.Label(self.root, text="Select User:").pack(pady=5)
        self.user_dropdown = ttk.Combobox(self.root, values=self.get_all_user_names(), state="readonly")
        self.user_dropdown.pack(pady=5)

        # Search button
        ttk.Button(self.root, text="Search", command=self.search_user).pack(pady=10)

        # Frame for results
        self.search_results_frame = ttk.Frame(self.root)
        self.search_results_frame.pack(expand=True, fill="both", padx=5, pady=5)

        # Back button
        self.add_back_button()

    def search_user(self):
        """
        Search for a user by name and display the result in a table.
        """
        try:
            selected_user_name = self.user_dropdown.get().strip()
            if not selected_user_name:
                raise ValueError("Please select a user to search.")

            # Search user details
            user = MemberManagement.search_member(name=selected_user_name)
            if not user:
                messagebox.showinfo("Search Result", "No user found.")
                return

            # Clear previous search results
            for widget in self.search_results_frame.winfo_children():
                widget.destroy()

            # Treeview for displaying results
            result_tree = ttk.Treeview(
                self.search_results_frame,
                columns=(
                    "Name", "Gym ID", "Gym Name", "City", "Membership Type",
                    "Membership Cost", "Join Date", "Attendance" if user["user_type"] == "Gym User" else "Details"
                ),
                show="headings",
            )
            result_tree.pack(expand=True, fill="both")

            # Define column headers
            result_tree.heading("Name", text="Name")
            result_tree.heading("Gym ID", text="Gym ID")
            result_tree.heading("Gym Name", text="Gym Name")
            result_tree.heading("City", text="City")
            result_tree.heading("Membership Type", text="Membership Type")
            result_tree.heading("Membership Cost", text="Membership Cost")
            result_tree.heading("Join Date", text="Join Date")

            if user["user_type"] == "Gym User":
                result_tree.heading("Attendance", text="Attendance")
            else:
                result_tree.heading("Details", text="Details")

            # Insert data into Treeview
            if user["user_type"] == "Gym User":
                # Retrieve attendance details from `attendance_tracking.py`
                attendance = self.get_attendance_by_user(user["member_id"])
                result_tree.insert(
                    "",
                    "end",
                    values=(
                        user["name"],
                        user["gym_id"],
                        user["gym_name"],
                        self.get_city_by_gym_id(user["gym_id"]),
                        user["membership_type"],
                        f"${float(user['cost']):.2f}",
                        user["join_date"],
                        attendance or "No attendance records",
                    ),
                )
            else:
                # Insert all user details
                result_tree.insert(
                    "",
                    "end",
                    values=(
                        user["name"],
                        user["gym_id"],
                        user["gym_name"],
                        self.get_city_by_gym_id(user["gym_id"]),
                        user.get("membership_type", "N/A"),
                        f"${float(user['cost']):.2f}",
                        user.get("join_date", "N/A"),
                        "All user details displayed here"  # Or replace with more specific data
                    ),
                )

        except ValueError as ve:
            messagebox.showwarning("Validation Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to search user: {e}")

    def get_all_user_names(self):
        """
        Retrieve all user names from the database.
        """
        try:
            users = MemberManagement.view_all_members()
            return [user["name"] for user in users]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch user names: {e}")
            return []

    def get_attendance_by_user(self, member_id):
        """
        Retrieve attendance records for a user.
        """
        try:
            # Replace with actual method to retrieve attendance from `attendance_tracking.py`
            attendance = AttendanceTracking.get_attendance_by_member_id(member_id)
            return ", ".join([f"{record['date']} ({record['zone']})" for record in attendance])
        except Exception:
            return None

    def get_city_by_gym_id(self, gym_id):
        """
        Retrieve the city associated with a gym ID.
        """
        try:
            gym = GymManager.view_gym_by_id(gym_id)
            return gym["city"] if gym else "Unknown"
        except Exception:
            return "Unknown"

    def create_update_delete_user_menu(self):
        """
        Create the menu for updating or deleting a user.
        """
        self.clear_root_widgets()

        ttk.Label(self.root, text="Update/Delete User", font=("Helvetica", 16)).pack(pady=10)

        # Dropdown to select user
        ttk.Label(self.root, text="Select User:").pack(pady=5)
        self.user_dropdown = ttk.Combobox(self.root, values=self.get_all_user_names(), state="readonly")
        self.user_dropdown.pack(pady=5)
        self.user_dropdown.set("Select a User")
        self.user_dropdown.bind("<<ComboboxSelected>>", self.on_user_selected)

        # Update user fields
        ttk.Label(self.root, text="Field to Update:").pack(pady=5)
        self.update_field_dropdown = ttk.Combobox(
            self.root,
            values=["name", "user_type", "gym_id", "membership_type", "cost"],
            state="readonly"
        )
        self.update_field_dropdown.pack(pady=5)

        ttk.Label(self.root, text="New Value:").pack(pady=5)
        self.update_value_entry = ttk.Entry(self.root)
        self.update_value_entry.pack(pady=5)

        ttk.Button(self.root, text="Update User", command=self.update_user).pack(pady=10)

        # Delete user button
        ttk.Button(self.root, text="Delete User", command=self.delete_user).pack(pady=10)

        # Back button
        self.add_back_button()

    def on_user_selected(self, event=None):
        """
        Handler for user selection dropdown.
        Ensures the selected user is valid.
        """
        try:
            selected_user_name = self.user_dropdown.get()
            users = MemberManagement.view_all_members()
            user = next((u for u in users if u["name"] == selected_user_name), None)
            if user:
                self.selected_user_id = user["member_id"]
            else:
                self.selected_user_id = None
                messagebox.showwarning("Warning", "Selected user not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to select user: {e}")

    def get_all_user_names(self):
        """
        Retrieve all user names from the database.
        """
        try:
            users = MemberManagement.view_all_members()
            return [user["name"] for user in users]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch user names: {e}")
            return []

    def update_user(self):
        """
        Update the selected user's field with the new value.
        """
        try:
            # Ensure a user has been selected
            if not hasattr(self, 'selected_user_id') or not self.selected_user_id:
                raise ValueError("Please select a user to update.")

            # Get the selected field and new value
            field = self.update_field_dropdown.get()
            new_value = self.update_value_entry.get().strip()

            # Validate inputs
            if not field:
                raise ValueError("Please select a field to update.")
            if not new_value:
                raise ValueError("New value cannot be empty.")

            # Update the user using MemberManagement
            MemberManagement.update_member(self.selected_user_id, {field: new_value})
            messagebox.showinfo("Success", "User updated successfully.")

            # Refresh the dropdown menu
            self.user_dropdown["values"] = self.get_all_user_names()

        except ValueError as ve:
            messagebox.showwarning("Validation Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update user: {e}")

    def delete_user(self):
        """
        Delete the selected user.
        """
        try:
            # Ensure a user has been selected
            if not hasattr(self, 'selected_user_id') or not self.selected_user_id:
                raise ValueError("Please select a user to delete.")

            # Delete the user using MemberManagement
            MemberManagement.delete_member_by_id(self.selected_user_id)
            messagebox.showinfo("Success", "User deleted successfully.")

            # Refresh the dropdown menu
            self.user_dropdown["values"] = self.get_all_user_names()

        except ValueError as ve:
            messagebox.showwarning("Validation Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete user: {e}")

    def clear_root_widgets(self):
        """
        Clear all widgets in the root window.
        """
        for widget in self.root.winfo_children():
            widget.destroy()

    def add_back_button(self):
        """
        Add a 'Back' button to return to the main menu.
        """
        back_button = ttk.Button(self.root, text="Back", command=self.create_main_menu)
        back_button.pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = UserManagementApp(root)
    root.mainloop()


