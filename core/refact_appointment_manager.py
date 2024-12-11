# core/appointment_management.py

import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from core.appointments import AppointmentManager
from core.member_management import MemberManagement
from core.gym_management import GymManager
import logging
import re
from database.data_loader import DataLoader

# Configure logging
logging.basicConfig(
    filename='logs/appointment_management.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AppointmentManagementFrame(ttk.Frame):
    def __init__(self, parent, data_loader:DataLoader):
        super().__init__(parent)
        self.parent = parent  # The Notebook or main application frame
        self.create_widgets()

    def create_widgets(self):
        # Create Tabs within this frame
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")

        # Create Frames for Tabs
        self.schedule_tab = ttk.Frame(self.notebook)
        self.view_tab = ttk.Frame(self.notebook)
        self.update_tab = ttk.Frame(self.notebook)
        self.delete_tab = ttk.Frame(self.notebook)
        self.search_tab = ttk.Frame(self.notebook)

        # Add Tabs to Notebook
        self.notebook.add(self.schedule_tab, text="Schedule")
        self.notebook.add(self.view_tab, text="View All")
        self.notebook.add(self.update_tab, text="Update")
        self.notebook.add(self.delete_tab, text="Delete")
        self.notebook.add(self.search_tab, text="Search")

        # Initialize Tabs
        self.create_schedule_tab()
        self.create_view_tab()
        self.create_update_tab()
        self.create_delete_tab()
        self.create_search_tab()

        # Bind tab change to update title if needed
        # Uncomment and modify if you want to handle title updates
        # self.notebook.bind("<<NotebookTabChanged>>", lambda e: self.update_title(self.notebook.tab(self.notebook.select(), "text")))

    def update_title(self, title):
        """Update window title with the current tab name."""
        # Assuming the main application handles the window title,
        # you might want to emit an event or call a callback instead.
        # For now, we'll leave this method empty.
        pass

    # Schedule Appointment Tab
    def create_schedule_tab(self):
        ttk.Label(self.schedule_tab, text="Schedule Appointment", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        # Member Name
        ttk.Label(self.schedule_tab, text="Member Name:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.member_name_cb = ttk.Combobox(self.schedule_tab, values=self.get_gym_users(), state="readonly")
        self.member_name_cb.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Wellbeing Staff Name
        ttk.Label(self.schedule_tab, text="Wellbeing Staff Name:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.wellbeing_name_cb = ttk.Combobox(self.schedule_tab, values=self.get_wellbeing_staff(), state="readonly")
        self.wellbeing_name_cb.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Select Date
        ttk.Label(self.schedule_tab, text="Select Date:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.schedule_date_cal = Calendar(self.schedule_tab, selectmode="day", date_pattern="yyyy-mm-dd")
        self.schedule_date_cal.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Select Time
        ttk.Label(self.schedule_tab, text="Select Time:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.schedule_time_cb = ttk.Combobox(self.schedule_tab, values=self.get_time_intervals(), state="readonly")
        self.schedule_time_cb.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        # Payment Status
        ttk.Label(self.schedule_tab, text="Payment Status:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.payment_status_cb = ttk.Combobox(self.schedule_tab, values=["Paid", "Pending"], state="readonly")
        self.payment_status_cb.set("Pending")  # Default to "Pending"
        self.payment_status_cb.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        # Schedule Appointment Button
        schedule_button = ttk.Button(self.schedule_tab, text="Schedule Appointment", command=self.schedule_appointment)
        schedule_button.grid(row=6, column=0, columnspan=2, pady=10)

    def schedule_appointment(self):
        member_name = self.member_name_cb.get()
        wellbeing_name = self.wellbeing_name_cb.get()
        date = self.schedule_date_cal.get_date()
        time = self.schedule_time_cb.get()
        payment_status = self.payment_status_cb.get()

        if not member_name or not wellbeing_name or not date or not time or not payment_status:
            messagebox.showerror("Error", "All fields are required.")
            logger.error("Schedule Appointment failed: Missing required fields.")
            return

        # Get member_id from member_name
        member = MemberManagement.search_member(name=member_name)
        if not member:
            messagebox.showerror("Error", "Selected member not found.")
            logger.error(f"Schedule Appointment failed: Member '{member_name}' not found.")
            return
        member_id = member["member_id"]

        # Get wellbeing staff member_id
        wellbeing_staff = MemberManagement.search_member(name=wellbeing_name)
        if not wellbeing_staff or wellbeing_staff["user_type"] != "Wellbeing Staff":
            messagebox.showerror("Error", "Selected wellbeing staff not found or invalid.")
            logger.error(f"Schedule Appointment failed: Wellbeing staff '{wellbeing_name}' not found or invalid.")
            return
        wellbeing_id = wellbeing_staff["member_id"]

        # Determine cost based on activity
        activity = wellbeing_staff.get("activity", "Unknown")
        if activity.lower() == "nutrition":
            cost = 250
        else:
            # Assume anything else is wellbeing type like physiotherapy
            cost = 350

        # Check if already booked at this date/time for this staff
        if AppointmentManager.is_double_booked(wellbeing_id, date, time):
            messagebox.showerror("Error", "This wellbeing staff is already booked at the selected date & time.")
            logger.warning(f"Schedule Appointment failed: Wellbeing staff '{wellbeing_id}' is double booked on {date} at {time}.")
            return

        try:
            AppointmentManager.schedule_appointment(member_id, wellbeing_id, date, time, cost, payment_status)
            messagebox.showinfo("Success", "Appointment scheduled successfully.")
            logger.info(f"Appointment scheduled successfully for member '{member_id}' with wellbeing staff '{wellbeing_id}' on {date} at {time}.")
            self.clear_schedule_form()
            self.view_all_appointments()
            self.load_update_appointments()
            self.load_delete_appointments()
            self.search_appointments()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to schedule appointment: {e}")
            logger.error(f"Failed to schedule appointment for member '{member_id}': {e}")

    def clear_schedule_form(self):
        """Clear all input fields in the Schedule Appointment form."""
        self.member_name_cb.set("")
        self.wellbeing_name_cb.set("")
        self.schedule_date_cal.selection_clear()
        self.schedule_time_cb.set("")
        self.payment_status_cb.set("Pending")
        logger.debug("Schedule Appointment form cleared.")

    # View All Appointments Tab
    def create_view_tab(self):
        ttk.Label(self.view_tab, text="View All Appointments", font=("Helvetica", 16)).pack(pady=10)

        columns = ("ID", "Wellbeing Staff Name", "Specialty", "Gym User Name", "Gym Name", "Date", "Time", "Cost", "Status")
        self.view_tree = ttk.Treeview(self.view_tab, columns=columns, show="headings")
        for col in columns:
            self.view_tree.heading(col, text=col)
            self.view_tree.column(col, anchor="center")
        self.view_tree.pack(expand=True, fill="both", padx=10, pady=10)

        # Refresh Button to Load Appointments
        refresh_button = ttk.Button(self.view_tab, text="Refresh", command=self.view_all_appointments)
        refresh_button.pack(pady=5)

    def view_all_appointments(self):
        """Populate the view_tree with all appointments from the database."""
        try:
            appointments = AppointmentManager.view_all_appointments_enriched()
            for row in self.view_tree.get_children():
                self.view_tree.delete(row)
            for appt in appointments:
                self.view_tree.insert("", "end", values=(
                    appt["appointment_id"],
                    appt["wellbeing_staff_name"],
                    appt["specialty"],
                    appt["gym_user_name"],
                    appt["gym_name"],
                    appt["date"],
                    appt["time"],
                    appt["cost"],
                    appt["status"]
                ))
            logger.info("All appointments loaded into the view successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load appointments: {e}")
            logger.error(f"Failed to load appointments: {e}")

    # Update Appointment Tab
    def create_update_tab(self):
        ttk.Label(self.update_tab, text="Update Appointment", font=("Helvetica", 16)).pack(pady=10)

        # Instruction
        ttk.Label(self.update_tab, text="Please select an appointment from the table below").pack(pady=5)

        # Appointment Table
        columns = ("ID", "Wellbeing Staff Name", "Specialty", "Gym User Name", "Gym Name", "Date", "Time", "Cost", "Status")
        self.update_tree = ttk.Treeview(self.update_tab, columns=columns, show="headings", selectmode="browse")
        for col in columns:
            self.update_tree.heading(col, text=col)
            self.update_tree.column(col, anchor="center")
        self.update_tree.pack(expand=True, fill="both", padx=10, pady=10)
        self.update_tree.bind("<<TreeviewSelect>>", self.on_update_select)

        # Update Fields
        update_frame = ttk.Frame(self.update_tab)
        update_frame.pack(pady=5)

        # New Date
        ttk.Label(update_frame, text="New Date:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.update_date_cal = Calendar(update_frame, selectmode="day", date_pattern="yyyy-mm-dd")
        self.update_date_cal.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # New Time
        ttk.Label(update_frame, text="New Time:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.update_time_cb = ttk.Combobox(update_frame, values=self.get_time_intervals(), state="readonly")
        self.update_time_cb.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Update Button
        update_button = ttk.Button(update_frame, text="Update Appointment", command=self.update_appointment)
        update_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Refresh Button
        refresh_button = ttk.Button(self.update_tab, text="Refresh", command=self.load_update_appointments)
        refresh_button.pack(pady=5)

        self.load_update_appointments()

    def load_update_appointments(self):
        """Load appointments into the update_tree."""
        try:
            appointments = AppointmentManager.view_all_appointments_enriched()
            for row in self.update_tree.get_children():
                self.update_tree.delete(row)
            for appt in appointments:
                self.update_tree.insert("", "end", values=(
                    appt["appointment_id"],
                    appt["wellbeing_staff_name"],
                    appt["specialty"],
                    appt["gym_user_name"],
                    appt["gym_name"],
                    appt["date"],
                    appt["time"],
                    appt["cost"],
                    appt["status"]
                ))
            logger.info("Appointments loaded into the update table successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load appointments for update: {e}")
            logger.error(f"Failed to load appointments for update: {e}")

    def on_update_select(self, event):
        """Handle selection in the update_tree."""
        selection = self.update_tree.selection()
        if selection:
            item = self.update_tree.item(selection[0])
            self.selected_update_appt_id = item["values"][0]  # ID is the first column
            logger.debug(f"Selected appointment for update: {self.selected_update_appt_id}")
        else:
            self.selected_update_appt_id = None

    def update_appointment(self):
        """Update the selected appointment with new date and time."""
        if not hasattr(self, 'selected_update_appt_id') or not self.selected_update_appt_id:
            messagebox.showerror("Error", "Please select an appointment to update.")
            logger.warning("Update Appointment failed: No appointment selected.")
            return

        new_date = self.update_date_cal.get_date()
        new_time = self.update_time_cb.get()

        if not new_date or not new_time:
            messagebox.showerror("Error", "Please select both new date and new time.")
            logger.warning("Update Appointment failed: New date or time not selected.")
            return

        try:
            # Retrieve appointment details
            appt = AppointmentManager.get_appointment_by_id(self.selected_update_appt_id)
            if not appt:
                messagebox.showerror("Error", "Selected appointment not found.")
                logger.error(f"Update Appointment failed: Appointment ID {self.selected_update_appt_id} not found.")
                return

            wellbeing_id = appt["trainer_id"]

            # Check for double booking, excluding the current appointment
            if AppointmentManager.is_double_booked(wellbeing_id, new_date, new_time, exclude_id=self.selected_update_appt_id):
                messagebox.showerror("Error", "This wellbeing staff is already booked at the selected date & time.")
                logger.warning(f"Update Appointment failed: Wellbeing staff '{wellbeing_id}' is double booked on {new_date} at {new_time}.")
                return

            # Perform the update
            AppointmentManager.update_appointment(self.selected_update_appt_id, new_date, new_time)
            messagebox.showinfo("Success", "Appointment updated successfully.")
            logger.info(f"Appointment '{self.selected_update_appt_id}' updated successfully to {new_date} at {new_time}.")
            self.load_update_appointments()
            self.view_all_appointments()
            self.load_delete_appointments()
            self.search_appointments()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update appointment: {e}")
            logger.error(f"Failed to update appointment '{self.selected_update_appt_id}': {e}")

    # Delete Appointment Tab
    def create_delete_tab(self):
        ttk.Label(self.delete_tab, text="Delete Appointment", font=("Helvetica", 16)).pack(pady=10)

        # Instruction
        ttk.Label(self.delete_tab, text="Please select an appointment from the table below").pack(pady=5)

        # Appointment Table
        columns = ("ID", "Wellbeing Staff Name", "Specialty", "Gym User Name", "Gym Name", "Date", "Time", "Cost", "Status")
        self.delete_tree = ttk.Treeview(self.delete_tab, columns=columns, show="headings", selectmode="browse")
        for col in columns:
            self.delete_tree.heading(col, text=col)
            self.delete_tree.column(col, anchor="center")
        self.delete_tree.pack(expand=True, fill="both", padx=10, pady=10)
        self.delete_tree.bind("<<TreeviewSelect>>", self.on_delete_select)

        # Delete Button
        delete_button = ttk.Button(self.delete_tab, text="Delete Appointment", command=self.delete_appointment)
        delete_button.pack(pady=10)

        # Refresh Button
        refresh_button = ttk.Button(self.delete_tab, text="Refresh", command=self.load_delete_appointments)
        refresh_button.pack(pady=5)

        self.load_delete_appointments()

    def load_delete_appointments(self):
        """Load appointments into the delete_tree."""
        try:
            appointments = AppointmentManager.view_all_appointments_enriched()
            for row in self.delete_tree.get_children():
                self.delete_tree.delete(row)
            for appt in appointments:
                self.delete_tree.insert("", "end", values=(
                    appt["appointment_id"],
                    appt["wellbeing_staff_name"],
                    appt["specialty"],
                    appt["gym_user_name"],
                    appt["gym_name"],
                    appt["date"],
                    appt["time"],
                    appt["cost"],
                    appt["status"]
                ))
            logger.info("Appointments loaded into the delete table successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load appointments for deletion: {e}")
            logger.error(f"Failed to load appointments for deletion: {e}")

    def on_delete_select(self, event):
        """Handle selection in the delete_tree."""
        selection = self.delete_tree.selection()
        if selection:
            item = self.delete_tree.item(selection[0])
            self.selected_delete_appt_id = item["values"][0]  # ID is the first column
            logger.debug(f"Selected appointment for deletion: {self.selected_delete_appt_id}")
        else:
            self.selected_delete_appt_id = None

    def delete_appointment(self):
        """Delete the selected appointment."""
        if not hasattr(self, 'selected_delete_appt_id') or not self.selected_delete_appt_id:
            messagebox.showerror("Error", "Please select an appointment to delete.")
            logger.warning("Delete Appointment failed: No appointment selected.")
            return

        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete the selected appointment?")
        if not confirm:
            logger.info(f"Delete Appointment operation canceled by user for appointment '{self.selected_delete_appt_id}'.")
            return

        try:
            AppointmentManager.delete_appointment(self.selected_delete_appt_id)
            messagebox.showinfo("Success", "Appointment deleted successfully.")
            logger.info(f"Appointment '{self.selected_delete_appt_id}' deleted successfully.")
            self.load_delete_appointments()
            self.view_all_appointments()
            self.load_update_appointments()
            self.search_appointments()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete appointment: {e}")
            logger.error(f"Failed to delete appointment '{self.selected_delete_appt_id}': {e}")

    # Search Appointment Tab
    def create_search_tab(self):
        ttk.Label(self.search_tab, text="Search Appointments", font=("Helvetica", 16)).pack(pady=10)

        # Search Criteria
        search_frame = ttk.Frame(self.search_tab)
        search_frame.pack(pady=5)

        ttk.Label(search_frame, text="Select Wellbeing Staff:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.search_wellbeing_cb = ttk.Combobox(search_frame, values=self.get_wellbeing_staff(), state="readonly")
        self.search_wellbeing_cb.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Search Button
        search_button = ttk.Button(search_frame, text="Search", command=self.search_appointments)
        search_button.grid(row=1, column=0, columnspan=2, pady=10)

        # Search Results Table
        columns = ("ID", "Wellbeing Staff Name", "Specialty", "Gym User Name", "Gym Name", "Date", "Time", "Cost", "Status")
        self.search_tree = ttk.Treeview(self.search_tab, columns=columns, show="headings")
        for col in columns:
            self.search_tree.heading(col, text=col)
            self.search_tree.column(col, anchor="center")
        self.search_tree.pack(expand=True, fill="both", padx=10, pady=10)

    def search_appointments(self):
        """Search appointments based on wellbeing staff name."""
        wellbeing_name = self.search_wellbeing_cb.get()
        if not wellbeing_name:
            messagebox.showerror("Error", "Please select a wellbeing staff.")
            logger.warning("Search Appointments failed: No wellbeing staff selected.")
            return

        try:
            appointments = AppointmentManager.search_appointments_by_wellbeing_name(wellbeing_name)
            for row in self.search_tree.get_children():
                self.search_tree.delete(row)
            for appt in appointments:
                self.search_tree.insert("", "end", values=(
                    appt["appointment_id"],
                    appt["wellbeing_staff_name"],
                    appt["specialty"],
                    appt["gym_user_name"],
                    appt["gym_name"],
                    appt["date"],
                    appt["time"],
                    appt["cost"],
                    appt["status"]
                ))
            logger.info(f"Appointments searched successfully for wellbeing staff '{wellbeing_name}'.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to search appointments: {e}")
            logger.error(f"Failed to search appointments for wellbeing staff '{wellbeing_name}': {e}")

    def get_gym_users(self):
        """Return list of gym user names."""
        try:
            users = MemberManagement.view_all_members()
            gym_users = [u["name"] for u in users if u["user_type"] == "Gym User"]
            logger.debug(f"Retrieved gym user names: {gym_users}")
            return gym_users
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load gym users: {e}")
            logger.error(f"Failed to load gym users: {e}")
            return []

    def get_wellbeing_staff(self):
        """Return list of wellbeing staff names."""
        try:
            users = MemberManagement.view_all_members()
            wellbeing_staff = [u["name"] for u in users if u["user_type"] == "Wellbeing Staff"]
            logger.debug(f"Retrieved wellbeing staff names: {wellbeing_staff}")
            return wellbeing_staff
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load wellbeing staff: {e}")
            logger.error(f"Failed to load wellbeing staff: {e}")
            return []

    def get_time_intervals(self):
        """Generate a list of time intervals."""
        intervals = []
        for hour in range(6, 24):
            for minute in (0, 30):
                intervals.append(f"{hour:02d}:{minute:02d}")
        logger.debug(f"Generated time intervals: {intervals}")
        return intervals

    def load_update_appointments(self):
        """Load appointments into the update_tree."""
        try:
            appointments = AppointmentManager.view_all_appointments_enriched()
            for row in self.update_tree.get_children():
                self.update_tree.delete(row)
            for appt in appointments:
                self.update_tree.insert("", "end", values=(
                    appt["appointment_id"],
                    appt["wellbeing_staff_name"],
                    appt["specialty"],
                    appt["gym_user_name"],
                    appt["gym_name"],
                    appt["date"],
                    appt["time"],
                    appt["cost"],
                    appt["status"]
                ))
            logger.info("Appointments loaded into the update table successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load appointments for update: {e}")
            logger.error(f"Failed to load appointments for update: {e}")

    def load_delete_appointments(self):
        """Load appointments into the delete_tree."""
        try:
            appointments = AppointmentManager.view_all_appointments_enriched()
            for row in self.delete_tree.get_children():
                self.delete_tree.delete(row)
            for appt in appointments:
                self.delete_tree.insert("", "end", values=(
                    appt["appointment_id"],
                    appt["wellbeing_staff_name"],
                    appt["specialty"],
                    appt["gym_user_name"],
                    appt["gym_name"],
                    appt["date"],
                    appt["time"],
                    appt["cost"],
                    appt["status"]
                ))
            logger.info("Appointments loaded into the delete table successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load appointments for deletion: {e}")
            logger.error(f"Failed to load appointments for deletion: {e}")

    # Utility Methods
    def get_gym_users(self):
        """Return list of gym user names."""
        try:
            users = MemberManagement.view_all_members()
            gym_users = [u["name"] for u in users if u["user_type"] == "Gym User"]
            logger.debug(f"Retrieved gym user names: {gym_users}")
            return gym_users
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load gym users: {e}")
            logger.error(f"Failed to load gym users: {e}")
            return []

    def get_wellbeing_staff(self):
        """Return list of wellbeing staff names."""
        try:
            users = MemberManagement.view_all_members()
            wellbeing_staff = [u["name"] for u in users if u["user_type"] == "Wellbeing Staff"]
            logger.debug(f"Retrieved wellbeing staff names: {wellbeing_staff}")
            return wellbeing_staff
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load wellbeing staff: {e}")
            logger.error(f"Failed to load wellbeing staff: {e}")
            return []

    def get_time_intervals(self):
        """Generate a list of time intervals."""
        intervals = []
        for hour in range(6, 24):
            for minute in (0, 30):
                intervals.append(f"{hour:02d}:{minute:02d}")
        logger.debug(f"Generated time intervals: {intervals}")
        return intervals
