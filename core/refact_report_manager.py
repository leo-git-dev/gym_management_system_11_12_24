# core/report_management.py

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from reports.report_manager import ReportManager
from database.data_loader import DataLoader  # Ensure this path is correct based on your project structure
import logging
import os

# Configure logging
logging.basicConfig(
    filename='logs/report_management.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ReportManagementFrame(ttk.Frame):
    def __init__(self, parent, data_loader: DataLoader):
        super().__init__(parent)
        self.parent = parent  # The Notebook or main application frame
        self.data_loader = data_loader
        self.report_manager = ReportManager(self.data_loader)
        self.create_widgets()

    def create_widgets(self):
        # Create Tabs within this frame
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")

        # Create Frames for Tabs
        self.attendance_report_tab = ttk.Frame(self.notebook)
        self.membership_growth_report_tab = ttk.Frame(self.notebook)
        self.payment_report_tab = ttk.Frame(self.notebook)
        self.membership_fees_report_tab = ttk.Frame(self.notebook)
        self.appointments_vs_staff_cost_report_tab = ttk.Frame(self.notebook)
        self.all_reports_tab = ttk.Frame(self.notebook)

        # Add Tabs to Notebook
        self.notebook.add(self.attendance_report_tab, text="Attendance Report")
        self.notebook.add(self.membership_growth_report_tab, text="Membership Growth Report")
        self.notebook.add(self.payment_report_tab, text="Payment Report")
        self.notebook.add(self.membership_fees_report_tab, text="Membership Fees Report")
        self.notebook.add(self.appointments_vs_staff_cost_report_tab, text="Appointments vs Staff Cost Report")
        self.notebook.add(self.all_reports_tab, text="All Reports")

        # Initialize Tabs
        self.create_attendance_report_tab()
        self.create_membership_growth_report_tab()
        self.create_payment_report_tab()
        self.create_membership_fees_report_tab()
        self.create_appointments_vs_staff_cost_report_tab()
        self.create_all_reports_tab()

    # Attendance Report Tab
    def create_attendance_report_tab(self):
        ttk.Label(self.attendance_report_tab, text="Attendance Report", font=("Helvetica", 16)).pack(pady=10)

        # Generate Report Button
        generate_button = ttk.Button(
            self.attendance_report_tab,
            text="Generate Attendance Report",
            command=self.generate_attendance_report
        )
        generate_button.pack(pady=10)

        # Report Status Label
        self.attendance_report_status = ttk.Label(
            self.attendance_report_tab,
            text="",
            foreground="green"
        )
        self.attendance_report_status.pack(pady=5)

    def generate_attendance_report(self):
        try:
            self.report_manager.generate_attendance_report()
            report_path = os.path.join(self.report_manager.reports_dir, 'attendance_report.jpeg')
            schedule_report_path = os.path.join(self.report_manager.reports_dir, 'attendance_schedule_report.jpeg')
            self.attendance_report_status.config(
                text=f"Attendance Report generated at:\n{report_path}\n{schedule_report_path}"
            )
            logger.info("Attendance Report generated successfully via GUI.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate Attendance Report: {e}")
            self.attendance_report_status.config(text="", foreground="red")
            logger.error(f"Failed to generate Attendance Report via GUI: {e}")

    # Membership Growth Report Tab
    def create_membership_growth_report_tab(self):
        ttk.Label(
            self.membership_growth_report_tab,
            text="Membership Growth Report",
            font=("Helvetica", 16)
        ).pack(pady=10)

        # Generate Report Button
        generate_button = ttk.Button(
            self.membership_growth_report_tab,
            text="Generate Membership Growth Report",
            command=self.generate_membership_growth_report
        )
        generate_button.pack(pady=10)

        # Report Status Label
        self.membership_growth_report_status = ttk.Label(
            self.membership_growth_report_tab,
            text="",
            foreground="green"
        )
        self.membership_growth_report_status.pack(pady=5)

    def generate_membership_growth_report(self):
        try:
            self.report_manager.generate_membership_growth_report()
            report_path = os.path.join(self.report_manager.reports_dir, 'membership_growth_report.jpeg')
            self.membership_growth_report_status.config(
                text=f"Membership Growth Report generated at {report_path}"
            )
            logger.info("Membership Growth Report generated successfully via GUI.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate Membership Growth Report: {e}")
            self.membership_growth_report_status.config(text="", foreground="red")
            logger.error(f"Failed to generate Membership Growth Report via GUI: {e}")

    # Payment Report Tab
    def create_payment_report_tab(self):
        ttk.Label(
            self.payment_report_tab,
            text="Payment Report",
            font=("Helvetica", 16)
        ).pack(pady=10)

        # Generate Report Button
        generate_button = ttk.Button(
            self.payment_report_tab,
            text="Generate Payment Report",
            command=self.generate_payment_report
        )
        generate_button.pack(pady=10)

        # Report Status Label
        self.payment_report_status = ttk.Label(
            self.payment_report_tab,
            text="",
            foreground="green"
        )
        self.payment_report_status.pack(pady=5)

    def generate_payment_report(self):
        try:
            self.report_manager.generate_payment_report()
            report_path = os.path.join(self.report_manager.reports_dir, 'payment_report.jpeg')
            payment_pie_report_path = os.path.join(
                self.report_manager.reports_dir,
                'payment_distribution_pie_report.jpeg'
            )
            self.payment_report_status.config(
                text=f"Payment Report generated at:\n{report_path}\n{payment_pie_report_path}"
            )
            logger.info("Payment Report generated successfully via GUI.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate Payment Report: {e}")
            self.payment_report_status.config(text="", foreground="red")
            logger.error(f"Failed to generate Payment Report via GUI: {e}")

    # Membership Fees Report Tab
    def create_membership_fees_report_tab(self):
        ttk.Label(
            self.membership_fees_report_tab,
            text="Membership Fees Report",
            font=("Helvetica", 16)
        ).pack(pady=10)

        # Generate Report Button
        generate_button = ttk.Button(
            self.membership_fees_report_tab,
            text="Generate Membership Fees Report",
            command=self.generate_membership_fees_report
        )
        generate_button.pack(pady=10)

        # Report Status Label
        self.membership_fees_report_status = ttk.Label(
            self.membership_fees_report_tab,
            text="",
            foreground="green"
        )
        self.membership_fees_report_status.pack(pady=5)

    def generate_membership_fees_report(self):
        try:
            self.report_manager.generate_membership_fees_report()
            report_path = os.path.join(self.report_manager.reports_dir, 'membership_fees_report.jpeg')
            self.membership_fees_report_status.config(
                text=f"Membership Fees Report generated at {report_path}"
            )
            logger.info("Membership Fees Report generated successfully via GUI.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate Membership Fees Report: {e}")
            self.membership_fees_report_status.config(text="", foreground="red")
            logger.error(f"Failed to generate Membership Fees Report via GUI: {e}")

    # Appointments vs Staff Cost Report Tab
    def create_appointments_vs_staff_cost_report_tab(self):
        ttk.Label(
            self.appointments_vs_staff_cost_report_tab,
            text="Appointments vs Staff Cost Report",
            font=("Helvetica", 16)
        ).pack(pady=10)

        # Appointment Fee Input
        fee_frame = ttk.Frame(self.appointments_vs_staff_cost_report_tab)
        fee_frame.pack(pady=5)

        ttk.Label(fee_frame, text="Appointment Fee ($):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.appointment_fee_entry = ttk.Entry(fee_frame)
        self.appointment_fee_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.appointment_fee_entry.insert(0, "50")  # Default value

        # Generate Report Button
        generate_button = ttk.Button(
            self.appointments_vs_staff_cost_report_tab,
            text="Generate Report",
            command=self.generate_appointments_vs_staff_cost_report
        )
        generate_button.pack(pady=10)

        # Report Status Label
        self.appointments_vs_staff_cost_report_status = ttk.Label(
            self.appointments_vs_staff_cost_report_tab,
            text="",
            foreground="green"
        )
        self.appointments_vs_staff_cost_report_status.pack(pady=5)

    def generate_appointments_vs_staff_cost_report(self):
        try:
            fee_str = self.appointment_fee_entry.get().strip()
            if not self.validate_numeric_input(fee_str):
                messagebox.showerror("Invalid Input", "Please enter a valid numeric appointment fee.")
                self.appointments_vs_staff_cost_report_status.config(text="", foreground="red")
                logger.error("Invalid appointment fee entered.")
                return
            appointment_fee = float(fee_str)
            self.report_manager.generate_appointments_vs_staff_cost_report(appointment_fee=appointment_fee)
            report_path = os.path.join(
                self.report_manager.reports_dir,
                'appointments_vs_staff_cost_report.jpeg'
            )
            self.appointments_vs_staff_cost_report_status.config(
                text=f"Report generated at {report_path}"
            )
            logger.info("Appointments vs Staff Cost Report generated successfully via GUI.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate Appointments vs Staff Cost Report: {e}")
            self.appointments_vs_staff_cost_report_status.config(text="", foreground="red")
            logger.error(f"Failed to generate Appointments vs Staff Cost Report via GUI: {e}")

    # All Reports Tab
    def create_all_reports_tab(self):
        ttk.Label(
            self.all_reports_tab,
            text="Generate All Reports",
            font=("Helvetica", 16)
        ).pack(pady=10)

        # Generate All Reports Button
        generate_button = ttk.Button(
            self.all_reports_tab,
            text="Generate All Reports",
            command=self.generate_all_reports
        )
        generate_button.pack(pady=10)

        # Report Status Label
        self.all_reports_status = ttk.Label(
            self.all_reports_tab,
            text="",
            foreground="green"
        )
        self.all_reports_status.pack(pady=5)

    def generate_all_reports(self):
        try:
            self.report_manager.generate_all_reports()
            reports = [
                'attendance_report.jpeg',
                'attendance_schedule_report.jpeg',
                'membership_growth_report.jpeg',
                'payment_report.jpeg',
                'payment_distribution_pie_report.jpeg',
                'appointments_vs_staff_cost_report.jpeg',
                'membership_fees_report.jpeg'
            ]
            report_paths = [os.path.join(self.report_manager.reports_dir, report) for report in reports]
            report_paths_str = "\n".join(report_paths)
            self.all_reports_status.config(
                text=f"All reports generated at:\n{report_paths_str}"
            )
            logger.info("All reports generated successfully via GUI.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate all reports: {e}")
            self.all_reports_status.config(text="", foreground="red")
            logger.error(f"Failed to generate all reports via GUI: {e}")

    # Utility Method for Numeric Input Validation
    def validate_numeric_input(self, input_str):
        """
        Validates if the input string is a positive number.

        :param input_str: The input string to validate.
        :return: True if valid, False otherwise.
        """
        try:
            value = float(input_str)
            if value < 0:
                return False
            return True
        except ValueError:
            return False

