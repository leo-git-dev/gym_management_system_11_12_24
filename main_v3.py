# main_app.py

import tkinter as tk
from tkinter import ttk, messagebox
from database.data_loader import DataLoader
from core.refact_registration_manager_v2 import RegistrationFrame
from core.refact_user_manager_v2 import UserManagementApp
from core.refact_gym_manager_v2 import GymManagementApp
from core.refact_class_activity_manager_v2 import ClassManagementApp
from core.refact_payment_manager_v2 import PaymentManagementFrame
from core.refact_appointment_manager_v2 import AppointmentManagerFrame
from reports.refact_report_manager_v2 import ReportManagementFrame
import os

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"
STAFF_USERNAME = "staff"
STAFF_PASSWORD = "staff123"

def authenticate_admin(username, password):
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        return True
    return False

def authenticate_staff(username, password):
    if username == STAFF_USERNAME and password == STAFF_PASSWORD:
        return True
    return False

class StaffRoleWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Select Staff Role")
        self.geometry("300x150")
        self.parent = parent

        ttk.Label(self, text="Select Your Staff Role:").pack(pady=10)
        self.role_var = tk.StringVar(value="Training Staff")
        role_combo = ttk.Combobox(self, textvariable=self.role_var, values=["Training Staff", "Wellbeing Staff", "Management Staff"], state="readonly")
        role_combo.pack(pady=5)

        ttk.Button(self, text="OK", command=self.on_ok).pack(pady=10)

    def on_ok(self):
        self.parent.chosen_staff_role = self.role_var.get()
        self.destroy()

class StaffLoginWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Staff Login")
        self.geometry("300x200")
        self.parent = parent

        ttk.Label(self, text="Username:").pack(pady=5)
        self.username_entry = ttk.Entry(self)
        self.username_entry.pack(pady=5)
        ttk.Label(self, text="Password:").pack(pady=5)
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        ttk.Button(self, text="Login", command=self.handle_login).pack(pady=10)
        self.bind("<Return>", lambda e: self.handle_login())
        self.username_entry.focus()

    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if authenticate_staff(username, password):
            # Successful staff login, now choose role
            role_win = StaffRoleWindow(self.parent)
            self.wait_window(role_win)
            if self.parent.chosen_staff_role:
                self.parent.logged_in_user = {"user_type": self.parent.chosen_staff_role, "username": username}
                self.destroy()
            else:
                messagebox.showerror("Role Selection", "You must select a role.")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

class AdminLoginWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Admin Login")
        self.geometry("300x200")
        self.parent = parent

        ttk.Label(self, text="Username:").pack(pady=5)
        self.username_entry = ttk.Entry(self)
        self.username_entry.pack(pady=5)
        ttk.Label(self, text="Password:").pack(pady=5)
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        ttk.Button(self, text="Login", command=self.handle_login).pack(pady=10)
        self.bind("<Return>", lambda e: self.handle_login())
        self.username_entry.focus()

    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if authenticate_admin(username, password):
            self.parent.logged_in_user = {"user_type": "Admin", "username": username}
            self.destroy()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

class RoleSelectionWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Select Role")
        self.geometry("300x200")
        self.parent = parent

        ttk.Label(self, text="Welcome to St Mary's Fitness Gym Management System", font=("Helvetica", 12)).pack(pady=10)
        ttk.Label(self, text="Please select your role:").pack(pady=5)
        self.role_var = tk.StringVar(value="Admin")
        role_combo = ttk.Combobox(self, textvariable=self.role_var, values=["Admin", "Staff"], state="readonly")
        role_combo.pack(pady=5)

        ttk.Button(self, text="Proceed", command=self.handle_proceed).pack(pady=10)

    def handle_proceed(self):
        role = self.role_var.get()
        if role == "Admin":
            login_win = AdminLoginWindow(self.parent)
            self.wait_window(login_win)
            if not self.parent.logged_in_user:
                # Admin login failed or closed
                return
            self.destroy()
        elif role == "Staff":
            login_win = StaffLoginWindow(self.parent)
            self.wait_window(login_win)
            if not self.parent.logged_in_user:
                # Staff login failed or closed
                return
            self.destroy()


class GymManagementSystem(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gym Management System")
        self.geometry("1200x800")

        self.data_loader = DataLoader()
        self.logged_in_user = None
        self.chosen_staff_role = None  # Will store chosen staff role after staff login

        # Show role selection window first
        self.withdraw()
        role_win = RoleSelectionWindow(self)
        self.wait_window(role_win)

        if not self.logged_in_user:
            # User closed the windows or login failed
            self.destroy()
            return

        # Now that we have logged_in_user, continue loading main app
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")

        # Create frames
        self.user_management_frame = UserManagementApp(self.notebook)
        self.gym_management_frame = GymManagementApp(self.notebook)
        self.class_management_frame = ClassManagementApp(self.notebook)
        self.registration_frame = RegistrationFrame(self.notebook)
        self.appointment_management_frame = AppointmentManagerFrame(self.notebook)
        self.payment_management_frame = PaymentManagementFrame(self.notebook)
        self.report_management_frame = ReportManagementFrame(self.notebook, self.data_loader)

        # Decide which tabs to add
        user_type = self.logged_in_user["user_type"]

        if user_type == "Admin":
            self.notebook.add(self.user_management_frame, text="User Management")
            self.notebook.add(self.gym_management_frame, text="Gym Management")
            self.notebook.add(self.class_management_frame, text="Class Management")
            self.notebook.add(self.registration_frame, text="Registration Management")
            self.notebook.add(self.appointment_management_frame, text="Appointment Management")
            self.notebook.add(self.payment_management_frame, text="Payment Management")
            self.notebook.add(self.report_management_frame, text="Report Management")

        elif user_type in ["Training Staff", "Wellbeing Staff"]:
            self.notebook.add(self.class_management_frame, text="Class Management")
            self.notebook.add(self.registration_frame, text="Registration Management")
            self.notebook.add(self.appointment_management_frame, text="Appointment Management")

        elif user_type == "Management Staff":
            self.notebook.add(self.user_management_frame, text="User Management")
            # Exclude Gym Management
            self.notebook.add(self.class_management_frame, text="Class Management")
            self.notebook.add(self.registration_frame, text="Registration Management")
            self.notebook.add(self.appointment_management_frame, text="Appointment Management")
            self.notebook.add(self.payment_management_frame, text="Payment Management")
            self.notebook.add(self.report_management_frame, text="Report Management")

        self.deiconify()

if __name__ == "__main__":
    app = GymManagementSystem()
    app.mainloop()
print("Current working directory:", os.getcwd())
