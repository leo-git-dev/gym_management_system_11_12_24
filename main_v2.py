# main_app.py

import tkinter as tk
from tkinter import ttk
from core.refact_registration_manager_v2 import RegistrationFrame
from core.refact_user_manager_v2 import UserManagementApp
from core.refact_gym_manager_v2 import GymManagementApp
from core.refact_class_activity_manager_v2 import ClassManagementApp
from core.refact_payment_manager_v2 import PaymentManagementFrame
from core.refact_appointment_manager_v2 import AppointmentManagerFrame
from reports.refact_report_manager_v2 import ReportManagementFrame
from database.data_loader import DataLoader

class GymManagementSystem(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gym Management System")
        self.geometry("1200x800")

        # Initialize DataLoader first
        self.data_loader = DataLoader()

        # Initialize Notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")

        # Add User Management Tab
        self.user_management_frame = UserManagementApp(self.notebook)
        self.notebook.add(self.user_management_frame, text="User Management")

        # Add Gym Management Tab
        self.gym_management_frame = GymManagementApp(self.notebook)
        self.notebook.add(self.gym_management_frame, text="Gym Management")

        # Add Class Activity Management Tab
        self.class_management_frame = ClassManagementApp(self.notebook)
        self.notebook.add(self.class_management_frame, text="Class Management")

        # Add Class Registration Management Tab
        self.registration_frame = RegistrationFrame(self.notebook)
        self.notebook.add(self.registration_frame, text="Registration Management")

        # Add Appointment Management Tab
        self.appointment_management_frame = AppointmentManagerFrame(self.notebook)
        self.notebook.add(self.appointment_management_frame, text="Appointment Management")

        # Add Payment Management Tab
        self.payment_management_frame = PaymentManagementFrame(self.notebook)
        self.notebook.add(self.payment_management_frame, text="Payment Management")

        # Add Report Management Tab
        # Note: Now we pass self.data_loader to ReportManagementFrame
        self.report_management_frame = ReportManagementFrame(self.notebook, self.data_loader)
        self.notebook.add(self.report_management_frame, text="Report Management")

if __name__ == "__main__":
    app = GymManagementSystem()
    app.mainloop()
import os
print("Current working directory:", os.getcwd())