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


