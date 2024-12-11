import tkinter as tk
from tkinter import ttk, messagebox
import os
import logging
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ReportManagementFrame(ttk.Frame):
    def __init__(self, parent, data_loader, reports_dir="../gym_management_system/reports"):
        super().__init__(parent)
        self.data_loader = data_loader
        self.reports_dir = reports_dir
        self.ensure_reports_dir()
        print(os.path.abspath(self.reports_dir))
        self.create_widgets()

    def ensure_reports_dir(self):
        """
        Ensures that the reports directory exists. Creates it if it doesn't.
        """
        if not os.path.exists(self.reports_dir):
            try:
                os.makedirs(self.reports_dir)
                logger.info(f"Created reports directory at {self.reports_dir}")
            except Exception as e:
                logger.error(f"Failed to create reports directory: {e}")
                raise

    def create_widgets(self):
        """
        Create the UI elements for managing and generating reports.
        """
        # Main frame layout
        ttk.Label(self, text="Report Management", font=("Helvetica", 16)).pack(pady=10)

        # Buttons for individual reports
        buttons_frame = ttk.Frame(self)
        buttons_frame.pack(pady=10)

        attendance_btn = ttk.Button(buttons_frame, text="Generate Attendance Report", command=self.generate_attendance_report)
        attendance_btn.grid(row=0, column=0, padx=5, pady=5)

        membership_growth_btn = ttk.Button(buttons_frame, text="Generate Membership Growth Report", command=self.generate_membership_growth_report)
        membership_growth_btn.grid(row=0, column=1, padx=5, pady=5)

        payment_btn = ttk.Button(buttons_frame, text="Generate Payment Report", command=self.generate_payment_report)
        payment_btn.grid(row=1, column=0, padx=5, pady=5)

        membership_fees_btn = ttk.Button(buttons_frame, text="Generate Membership Fees Report", command=self.generate_membership_fees_report)
        membership_fees_btn.grid(row=1, column=1, padx=5, pady=5)

        appointments_vs_staff_btn = ttk.Button(buttons_frame, text="Generate Appointments vs Staff Cost Report", command=self.generate_appointments_vs_staff_cost_report)
        appointments_vs_staff_btn.grid(row=2, column=0, padx=5, pady=5, columnspan=2)

        # Button to generate all reports
        generate_all_btn = ttk.Button(self, text="Generate All Reports", command=self.generate_all_reports)
        generate_all_btn.pack(pady=10)

        # Status text area
        self.status_text = tk.Text(self, height=10, wrap="word")
        self.status_text.pack(fill="both", expand=True, padx=10, pady=10)
        self.status_text.insert("end", "Report generation logs will appear here.\n")

    def log_status(self, message):
        """
        Utility to log status messages to the text box and logger.
        """
        self.status_text.insert("end", message + "\n")
        self.status_text.see("end")  # Auto-scroll
        logger.info(message)

    def generate_attendance_report(self):
        """
        Generates the Attendance Report:
        - Total number of registrations per class.
        - Registrations per schedule (day and time).
        Saves the report as 'attendance_report.jpeg'.
        """
        try:
            classes = self.data_loader.get_data("classes")
            logger.debug(f"Loaded classes data: {classes}")

            # Prepare data for total registrations per class
            class_names = []
            total_registrations = []

            for cls in classes:
                class_names.append(cls['class_name'])
                total_registrations.append(len(cls.get('registered_users', [])))

            # Plot Total Registrations per Class
            plt.figure(figsize=(10, 6))
            plt.bar(class_names, total_registrations, color='skyblue')
            plt.xlabel('Class Name')
            plt.ylabel('Number of Registrations')
            plt.title('Total Registrations per Class')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            attendance_report_path = os.path.join(self.reports_dir, 'attendance_report.jpeg')
            plt.savefig(attendance_report_path, format='jpeg')
            plt.close()
            self.log_status(f"Attendance Report generated at {attendance_report_path}")

            # Prepare data for registrations per schedule
            schedule_data = []
            for cls in classes:
                for registration in cls.get('registered_users', []):
                    schedule_data.append({
                        'Class Name': cls['class_name'],
                        'Day': registration['day'],
                        'Time': registration['time']
                    })

            if schedule_data:
                df_schedule = pd.DataFrame(schedule_data)
                # Count registrations per class per day per time
                pivot_table = df_schedule.pivot_table(index=['Class Name', 'Day'], columns='Time', aggfunc='size',
                                                      fill_value=0)

                # Plot Registrations per Schedule
                pivot_table.plot(kind='bar', stacked=True, figsize=(12, 7))
                plt.xlabel('Class Name and Day')
                plt.ylabel('Number of Registrations')
                plt.title('Registrations per Schedule (Day and Time)')
                plt.xticks(rotation=45, ha='right')
                plt.legend(title='Time', bbox_to_anchor=(1.05, 1), loc='upper left')
                plt.tight_layout()
                schedule_report_path = os.path.join(self.reports_dir, 'attendance_schedule_report.jpeg')
                plt.savefig(schedule_report_path, format='jpeg')
                plt.close()
                self.log_status(f"Attendance Schedule Report generated at {schedule_report_path}")
            else:
                self.log_status("No registration data available to generate schedule report.")

        except Exception as e:
            self.log_status(f"Failed to generate Attendance Report: {e}")
            logger.error(f"Failed to generate Attendance Report: {e}")

    def generate_membership_growth_report(self):
        """
        Generates the Membership Growth Report:
        - Number of new memberships over time (by join_date).
        Saves the report as 'membership_growth_report.jpeg'.
        """
        try:
            members = self.data_loader.get_data("members")
            logger.debug(f"Loaded members data: {members}")

            # Extract join dates and filter valid dates
            join_dates = []
            for member in members:
                join_date_str = member.get('join_date', None)
                if join_date_str and join_date_str != "N/A":
                    try:
                        join_date = datetime.strptime(join_date_str, "%Y-%m-%d")
                        join_dates.append(join_date)
                    except ValueError:
                        logger.warning(f"Invalid join_date format for member_id {member['member_id']}: {join_date_str}")

            if not join_dates:
                self.log_status("No valid join dates available to generate Membership Growth Report.")
                return

            # Create a DataFrame
            df_join = pd.DataFrame({'Join Date': join_dates})
            df_join['Month'] = df_join['Join Date'].dt.to_period('M')
            monthly_growth = df_join.groupby('Month').size().reset_index(name='New Members')
            monthly_growth['Month'] = monthly_growth['Month'].dt.to_timestamp()

            # Plot Membership Growth
            plt.figure(figsize=(10, 6))
            plt.plot(monthly_growth['Month'], monthly_growth['New Members'], marker='o', linestyle='-')
            plt.xlabel('Month')
            plt.ylabel('Number of New Members')
            plt.title('Membership Growth Over Time')
            plt.grid(True)
            plt.tight_layout()
            growth_report_path = os.path.join(self.reports_dir, 'membership_growth_report.jpeg')
            plt.savefig(growth_report_path, format='jpeg')
            plt.close()
            self.log_status(f"Membership Growth Report generated at {growth_report_path}")

        except Exception as e:
            self.log_status(f"Failed to generate Membership Growth Report: {e}")
            logger.error(f"Failed to generate Membership Growth Report: {e}")

    def generate_payment_report(self):
        """
        Generates the Payment Report:
        - Total payments received.
        - Payments by membership type.
        Saves the report as 'payment_report.jpeg'.
        """
        try:
            members = self.data_loader.get_data("members")
            logger.debug(f"Loaded members data: {members}")

            # Extract payment data
            payment_data = []
            for member in members:
                cost = member.get('cost', 0)
                membership_type = member.get('membership_type', 'N/A')
                payment_data.append({
                    'Membership Type': membership_type,
                    'Cost': cost
                })

            df_payment = pd.DataFrame(payment_data)

            # Total Payments
            total_payments = df_payment['Cost'].sum()
            self.log_status(f"Total Payments Received: {total_payments}")

            # Payments by Membership Type
            payments_by_type = df_payment.groupby('Membership Type')['Cost'].sum().reset_index()

            # Plot Payment Report
            plt.figure(figsize=(10, 6))
            plt.bar(payments_by_type['Membership Type'], payments_by_type['Cost'], color='salmon')
            plt.xlabel('Membership Type')
            plt.ylabel('Total Payments Received')
            plt.title('Payments by Membership Type')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            payment_report_path = os.path.join(self.reports_dir, 'payment_report.jpeg')
            plt.savefig(payment_report_path, format='jpeg')
            plt.close()
            self.log_status(f"Payment Report generated at {payment_report_path}")

            # Pie chart for payment distribution
            plt.figure(figsize=(8, 8))
            plt.pie(payments_by_type['Cost'], labels=payments_by_type['Membership Type'], autopct='%1.1f%%',
                    startangle=140)
            plt.title('Payment Distribution by Membership Type')
            plt.tight_layout()
            payment_pie_report_path = os.path.join(self.reports_dir, 'payment_distribution_pie_report.jpeg')
            plt.savefig(payment_pie_report_path, format='jpeg')
            plt.close()
            self.log_status(f"Payment Distribution Pie Report generated at {payment_pie_report_path}")

        except Exception as e:
            self.log_status(f"Failed to generate Payment Report: {e}")
            logger.error(f"Failed to generate Payment Report: {e}")

    def generate_membership_fees_report(self):
        """
        Generates the Membership Fees Received Report:
        - Total membership fees received from gym users.
        Saves the report as 'membership_fees_report.jpeg'.
        """
        try:
            members = self.data_loader.get_data("members")
            logger.debug(f"Loaded members data: {members}")

            # Filter gym users
            gym_users = [m for m in members if m.get('user_type') == "Gym User"]
            total_membership_fees = sum(m.get('cost', 0) for m in gym_users)
            self.log_status(f"Total Membership Fees Received: {total_membership_fees}")

            # Plot Membership Fees
            membership_types = [m.get('membership_type', 'N/A') for m in gym_users]
            fees = [m.get('cost', 0) for m in gym_users]
            df_membership = pd.DataFrame({
                'Membership Type': membership_types,
                'Fee': fees
            })

            fees_by_type = df_membership.groupby('Membership Type')['Fee'].sum().reset_index()

            plt.figure(figsize=(10, 6))
            plt.bar(fees_by_type['Membership Type'], fees_by_type['Fee'], color='green')
            plt.xlabel('Membership Type')
            plt.ylabel('Total Fees Received')
            plt.title('Membership Fees Received by Type')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            membership_fees_report_path = os.path.join(self.reports_dir, 'membership_fees_report.jpeg')
            plt.savefig(membership_fees_report_path, format='jpeg')
            plt.close()
            self.log_status(f"Membership Fees Report generated at {membership_fees_report_path}")

        except Exception as e:
            self.log_status(f"Failed to generate Membership Fees Report: {e}")
            logger.error(f"Failed to generate Membership Fees Report: {e}")

    def generate_appointments_vs_staff_cost_report(self, appointment_fee=50):
        """
        Generates the Appointments Fee Received vs. Total Staff Cost Report:
        - Appointments Fee Received: Total number of class registrations multiplied by appointment_fee.
        - Total Staff Cost: Sum of 'cost' for training, wellbeing, and management staff.
        Saves the report as 'appointments_vs_staff_cost_report.jpeg'.
        """
        try:
            classes = self.data_loader.get_data("classes")
            logger.debug(f"Loaded classes data: {classes}")

            # Calculate total number of class registrations
            total_registrations = sum(len(cls.get('registered_users', [])) for cls in classes)
            appointments_fee_received = total_registrations * appointment_fee
            self.log_status(f"Total Appointments: {total_registrations}")
            self.log_status(f"Appointments Fee Received (@${appointment_fee} per appointment): {appointments_fee_received}")

            # Calculate total staff cost (Training, Wellbeing, Management Staff)
            members = self.data_loader.get_data("members")
            staff_types = ["Training Staff", "Wellbeing Staff", "Management Staff"]
            total_staff_cost = sum(m.get('cost', 0) for m in members if m.get('user_type') in staff_types)
            self.log_status(f"Total Staff Cost (Training, Wellbeing, Management): {total_staff_cost}")

            # Prepare data for comparison
            report_data = {
                'Revenue': [appointments_fee_received],
                'Cost': [total_staff_cost]
            }
            df_report = pd.DataFrame(report_data, index=['Appointments Fee Received vs Staff Cost'])

            # Plot Comparison
            df_report.plot(kind='bar', figsize=(8, 6), color=['blue', 'orange'])
            plt.ylabel('Amount ($)')
            plt.title('Appointments Fee Received vs. Total Staff Cost')
            plt.xticks(rotation=0)
            plt.tight_layout()
            appointments_vs_staff_report_path = os.path.join(self.reports_dir, 'appointments_vs_staff_cost_report.jpeg')
            plt.savefig(appointments_vs_staff_report_path, format='jpeg')
            plt.close()
            self.log_status(f"Appointments vs Staff Cost Report generated at {appointments_vs_staff_report_path}")

        except Exception as e:
            self.log_status(f"Failed to generate Appointments vs Staff Cost Report: {e}")
            logger.error(f"Failed to generate Appointments vs Staff Cost Report: {e}")

    def generate_all_reports(self):
        """
        Generates all reports: Attendance, Membership Growth, Payment, Appointments vs Staff Cost, Membership Fees.
        """
        self.log_status("Starting generation of all reports.")
        self.generate_attendance_report()
        self.generate_membership_growth_report()
        self.generate_payment_report()
        self.generate_appointments_vs_staff_cost_report()
        self.generate_membership_fees_report()
        self.log_status("All reports have been generated successfully.")

'''
if __name__ == "__main__":
    from database.data_loader import DataLoader  # Ensure this path is correct based on your project structure

    # Test the frame independently
    root = tk.Tk()
    root.title("Report Management Test")

    data_loader = DataLoader()  # Initialize DataLoader

    report_frame = ReportManagementFrame(root, data_loader)
    report_frame.pack(expand=True, fill='both')

    root.mainloop()
'''