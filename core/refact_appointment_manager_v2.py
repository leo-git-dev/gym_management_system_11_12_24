import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from core.appointments import AppointmentManager
from core.member_management import MemberManagement
from core.gym_management import GymManager
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AppointmentManagerFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.selected_update_appt_id = None
        self.selected_delete_appt_id = None
        self.create_widgets()

    def create_widgets(self):
        # Create Notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")

        # Tabs
        self.schedule_tab = ttk.Frame(self.notebook)
        self.view_tab = ttk.Frame(self.notebook)
        self.update_tab = ttk.Frame(self.notebook)
        self.delete_tab = ttk.Frame(self.notebook)
        self.search_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.schedule_tab, text="Schedule")
        self.notebook.add(self.view_tab, text="View All")
        self.notebook.add(self.update_tab, text="Update")
        self.notebook.add(self.delete_tab, text="Delete")
        self.notebook.add(self.search_tab, text="Search")

        # Add global refresh button at the bottom
        refresh_button = ttk.Button(self, text="Refresh", command=self.refresh_tab)
        refresh_button.pack(pady=10)

        # Data fields
        self.member_name_cb = None
        self.wellbeing_name_cb = None
        self.schedule_date_cal = None
        self.schedule_time_cb = None
        self.payment_status_cb = None

        self.view_tree = None
        self.update_tree = None
        self.update_date_cal = None
        self.update_time_cb = None
        self.delete_tree = None
        self.search_wellbeing_cb = None
        self.search_tree = None

        self.create_schedule_tab()
        self.create_view_tab()
        self.create_update_tab()
        self.create_delete_tab()
        self.create_search_tab()

    def refresh_tab(self):
        """Refresh the currently active tab."""
        current_tab = self.notebook.index(self.notebook.select())
        if current_tab == 0:  # Schedule Tab
            self.refresh_schedule_tab()
        elif current_tab == 1:  # View All Tab
            self.view_all_appointments()
        elif current_tab == 2:  # Update Tab
            self.load_update_appointments()
        elif current_tab == 3:  # Delete Tab
            self.load_delete_appointments()
        elif current_tab == 4:  # Search Tab
            self.refresh_search_tab()
        else:
            messagebox.showinfo("Info", "Nothing to refresh on this tab.")

    def refresh_schedule_tab(self):
        """Refresh the dropdown lists in the Schedule tab."""
        self.member_name_cb["values"] = self.get_gym_users()
        self.wellbeing_name_cb["values"] = self.get_wellbeing_staff()

    def refresh_search_tab(self):
        """Refresh the dropdown and search tree in the Search tab."""
        self.search_wellbeing_cb["values"] = self.get_wellbeing_staff()
        # Clear the search tree
        for row in self.search_tree.get_children():
            self.search_tree.delete(row)

    def get_gym_users(self):
        """Return list of gym user names."""
        users = MemberManagement.view_all_members()
        return [u["name"] for u in users if u["user_type"] == "Gym User"]

    def get_wellbeing_staff(self):
        """Return list of wellbeing staff names."""
        users = MemberManagement.view_all_members()
        return [u["name"] for u in users if u["user_type"] == "Wellbeing Staff"]

    def get_time_intervals(self):
        intervals = []
        for hour in range(6, 24):
            for minute in (0, 30):
                intervals.append(f"{hour:02d}:{minute:02d}")
        return intervals

    # Schedule Appointment Tab
    def create_schedule_tab(self):
        ttk.Label(self.schedule_tab, text="Member Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.member_name_cb = ttk.Combobox(self.schedule_tab, values=self.get_gym_users(), state="readonly")
        self.member_name_cb.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(self.schedule_tab, text="Wellbeing Staff Name:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.wellbeing_name_cb = ttk.Combobox(self.schedule_tab, values=self.get_wellbeing_staff(), state="readonly")
        self.wellbeing_name_cb.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(self.schedule_tab, text="Select Date:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.schedule_date_cal = Calendar(self.schedule_tab, selectmode="day", date_pattern="yyyy-mm-dd")
        self.schedule_date_cal.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(self.schedule_tab, text="Select Time:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.schedule_time_cb = ttk.Combobox(self.schedule_tab, values=self.get_time_intervals(), state="readonly")
        self.schedule_time_cb.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(self.schedule_tab, text="Payment Status:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.payment_status_cb = ttk.Combobox(self.schedule_tab, values=["Paid", "Pending"], state="readonly")
        self.payment_status_cb.set("Pending")  # Default to "Pending"
        self.payment_status_cb.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        schedule_button = ttk.Button(self.schedule_tab, text="Schedule Appointment", command=self.schedule_appointment)
        schedule_button.grid(row=5, column=0, columnspan=2, pady=10)

    def schedule_appointment(self):
        member_name = self.member_name_cb.get()
        wellbeing_name = self.wellbeing_name_cb.get()
        date = self.schedule_date_cal.get_date()
        time = self.schedule_time_cb.get()
        payment_status = self.payment_status_cb.get()

        if not member_name or not wellbeing_name or not date or not time or not payment_status:
            messagebox.showerror("Error", "All fields are required.")
            return

        member = MemberManagement.search_member(name=member_name)
        if not member:
            messagebox.showerror("Error", "Selected member not found.")
            return
        member_id = member["member_id"]

        wellbeing_staff = MemberManagement.search_member(name=wellbeing_name)
        if not wellbeing_staff or wellbeing_staff["user_type"] != "Wellbeing Staff":
            messagebox.showerror("Error", "Selected wellbeing staff not found or invalid.")
            return
        wellbeing_id = wellbeing_staff["member_id"]

        activity = wellbeing_staff.get("activity", "Unknown")
        if activity.lower() == "nutrition":
            cost = 250
        else:
            cost = 350

        if AppointmentManager.is_double_booked(wellbeing_id, date, time):
            messagebox.showerror("Error", "This wellbeing staff is already booked at the selected date & time.")
            return

        try:
            AppointmentManager.schedule_appointment(member_id, wellbeing_id, date, time, cost, payment_status)
            messagebox.showinfo("Success", "Appointment scheduled successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to schedule appointment: {e}")

    # View All Appointments Tab
    def create_view_tab(self):
        columns = ("ID", "Wellbeing Staff Name", "Specialty", "Gym User Name", "Gym Name", "Date", "Time", "Cost", "Status")
        self.view_tree = ttk.Treeview(self.view_tab, columns=columns, show="headings")
        for col in columns:
            self.view_tree.heading(col, text=col)
        self.view_tree.pack(expand=True, fill="both")

    def view_all_appointments(self):
        for row in self.view_tree.get_children():
            self.view_tree.delete(row)
        appointments = AppointmentManager.view_all_appointments_enriched()
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

    # Update Appointment Tab
    def create_update_tab(self):
        caption = ttk.Label(self.update_tab, text="Please select from table below", font=("Helvetica", 10, "bold"))
        caption.pack(pady=5)

        columns = ("ID", "Wellbeing Staff Name", "Specialty", "Gym User Name", "Gym Name", "Date", "Time", "Cost", "Status")
        self.update_tree = ttk.Treeview(self.update_tab, columns=columns, show="headings")
        for col in columns:
            self.update_tree.heading(col, text=col)
        self.update_tree.bind("<<TreeviewSelect>>", self.on_update_select)
        self.update_tree.pack(expand=True, fill="both")

        frame = ttk.Frame(self.update_tab)
        frame.pack(pady=5)

        ttk.Label(frame, text="New Date:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.update_date_cal = Calendar(frame, selectmode="day", date_pattern="yyyy-mm-dd")
        self.update_date_cal.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(frame, text="New Time:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.update_time_cb = ttk.Combobox(frame, values=self.get_time_intervals(), state="readonly")
        self.update_time_cb.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        update_button = ttk.Button(frame, text="Update Appointment", command=self.update_appointment)
        update_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.load_update_appointments()

    def load_update_appointments(self):
        for row in self.update_tree.get_children():
            self.update_tree.delete(row)
        appointments = AppointmentManager.view_all_appointments_enriched()
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

    def on_update_select(self, event):
        selection = self.update_tree.selection()
        if selection:
            item = self.update_tree.item(selection[0])
            self.selected_update_appt_id = item["values"][0]  # ID is the first column

    def update_appointment(self):
        if not self.selected_update_appt_id:
            messagebox.showerror("Error", "Please select an appointment from the table.")
            return
        new_date = self.update_date_cal.get_date()
        new_time = self.update_time_cb.get()
        if not new_date or not new_time:
            messagebox.showerror("Error", "Please select date and time.")
            return

        appt = AppointmentManager.get_appointment_by_id(self.selected_update_appt_id)
        if not appt:
            messagebox.showerror("Error", "Appointment not found.")
            return

        wellbeing_id = appt["trainer_id"]
        if AppointmentManager.is_double_booked(wellbeing_id, new_date, new_time, exclude_id=self.selected_update_appt_id):
            messagebox.showerror("Error", "This wellbeing staff is already booked at the selected date & time.")
            return

        if AppointmentManager.update_appointment(self.selected_update_appt_id, new_date, new_time):
            messagebox.showinfo("Success", "Appointment updated successfully.")
            self.load_update_appointments()
        else:
            messagebox.showerror("Error", "Failed to update appointment.")

    # Delete Appointment Tab
    def create_delete_tab(self):
        caption = ttk.Label(self.delete_tab, text="Please select from table below", font=("Helvetica", 10, "bold"))
        caption.pack(pady=5)

        columns = ("ID", "Wellbeing Staff Name", "Specialty", "Gym User Name", "Gym Name", "Date", "Time", "Cost", "Status")
        self.delete_tree = ttk.Treeview(self.delete_tab, columns=columns, show="headings")
        for col in columns:
            self.delete_tree.heading(col, text=col)
        self.delete_tree.bind("<<TreeviewSelect>>", self.on_delete_select)
        self.delete_tree.pack(expand=True, fill="both")

        delete_button = ttk.Button(self.delete_tab, text="Delete Appointment", command=self.delete_appointment)
        delete_button.pack(pady=10)

        self.load_delete_appointments()

    def load_delete_appointments(self):
        for row in self.delete_tree.get_children():
            self.delete_tree.delete(row)
        appointments = AppointmentManager.view_all_appointments_enriched()
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

    def on_delete_select(self, event):
        selection = self.delete_tree.selection()
        if selection:
            item = self.delete_tree.item(selection[0])
            self.selected_delete_appt_id = item["values"][0]

    def delete_appointment(self):
        if not self.selected_delete_appt_id:
            messagebox.showerror("Error", "Please select an appointment from the table.")
            return

        if AppointmentManager.delete_appointment(self.selected_delete_appt_id):
            messagebox.showinfo("Success", "Appointment deleted successfully.")
            self.load_delete_appointments()
        else:
            messagebox.showerror("Error", "Appointment not found or could not be deleted.")

    # Search Appointment Tab
    def create_search_tab(self):
        ttk.Label(self.search_tab, text="Select Wellbeing Staff:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.search_wellbeing_cb = ttk.Combobox(self.search_tab, values=self.get_wellbeing_staff(), state="readonly")
        self.search_wellbeing_cb.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        search_button = ttk.Button(self.search_tab, text="Search", command=self.search_appointments)
        search_button.grid(row=1, column=0, columnspan=2, pady=10)

        columns = ("ID", "Wellbeing Staff Name", "Specialty", "Gym User Name", "Gym Name", "Date", "Time", "Cost", "Status")
        self.search_tree = ttk.Treeview(self.search_tab, columns=columns, show="headings")
        for col in columns:
            self.search_tree.heading(col, text=col)
        self.search_tree.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        self.search_tab.grid_columnconfigure(0, weight=1)
        self.search_tab.grid_columnconfigure(1, weight=1)
        self.search_tab.grid_rowconfigure(2, weight=1)

    def search_appointments(self):
        wellbeing_name = self.search_wellbeing_cb.get()
        if not wellbeing_name:
            messagebox.showerror("Error", "Please select a wellbeing staff.")
            return

        for row in self.search_tree.get_children():
            self.search_tree.delete(row)

        appointments = AppointmentManager.search_appointments_by_wellbeing_name(wellbeing_name)
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





'''import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from core.appointments import AppointmentManager
from core.member_management import MemberManagement
from core.gym_management import GymManager
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AppointmentManagerFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.selected_update_appt_id = None
        self.selected_delete_appt_id = None
        self.create_widgets()

    def create_widgets(self):
        # Create Notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")

        # Tabs
        self.schedule_tab = ttk.Frame(self.notebook)
        self.view_tab = ttk.Frame(self.notebook)
        self.update_tab = ttk.Frame(self.notebook)
        self.delete_tab = ttk.Frame(self.notebook)
        self.search_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.schedule_tab, text="Schedule")
        self.notebook.add(self.view_tab, text="View All")
        self.notebook.add(self.update_tab, text="Update")
        self.notebook.add(self.delete_tab, text="Delete")
        self.notebook.add(self.search_tab, text="Search")

        # Data fields
        self.member_name_cb = None
        self.wellbeing_name_cb = None
        self.schedule_date_cal = None
        self.schedule_time_cb = None
        self.payment_status_cb = None

        self.view_tree = None

        self.update_tree = None
        self.update_date_cal = None
        self.update_time_cb = None

        self.delete_tree = None

        self.search_wellbeing_cb = None
        self.search_tree = None

        self.create_schedule_tab()
        self.create_view_tab()
        self.create_update_tab()
        self.create_delete_tab()
        self.create_search_tab()

    def get_gym_users(self):
        """Return list of gym user names."""
        users = MemberManagement.view_all_members()
        return [u["name"] for u in users if u["user_type"] == "Gym User"]

    def get_wellbeing_staff(self):
        """Return list of wellbeing staff names."""
        users = MemberManagement.view_all_members()
        return [u["name"] for u in users if u["user_type"] == "Wellbeing Staff"]

    def get_time_intervals(self):
        intervals = []
        for hour in range(6, 24):
            for minute in (0, 30):
                intervals.append(f"{hour:02d}:{minute:02d}")
        return intervals

    # Schedule Appointment Tab
    def create_schedule_tab(self):
        ttk.Label(self.schedule_tab, text="Member Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.member_name_cb = ttk.Combobox(self.schedule_tab, values=self.get_gym_users(), state="readonly")
        self.member_name_cb.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(self.schedule_tab, text="Wellbeing Staff Name:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.wellbeing_name_cb = ttk.Combobox(self.schedule_tab, values=self.get_wellbeing_staff(), state="readonly")
        self.wellbeing_name_cb.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(self.schedule_tab, text="Select Date:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.schedule_date_cal = Calendar(self.schedule_tab, selectmode="day", date_pattern="yyyy-mm-dd")
        self.schedule_date_cal.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(self.schedule_tab, text="Select Time:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.schedule_time_cb = ttk.Combobox(self.schedule_tab, values=self.get_time_intervals(), state="readonly")
        self.schedule_time_cb.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Payment status field
        ttk.Label(self.schedule_tab, text="Payment Status:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.payment_status_cb = ttk.Combobox(self.schedule_tab, values=["Paid", "Pending"], state="readonly")
        self.payment_status_cb.set("Pending")  # Default to "Pending"
        self.payment_status_cb.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        schedule_button = ttk.Button(self.schedule_tab, text="Schedule Appointment", command=self.schedule_appointment)
        schedule_button.grid(row=5, column=0, columnspan=2, pady=10)

    def schedule_appointment(self):
        member_name = self.member_name_cb.get()
        wellbeing_name = self.wellbeing_name_cb.get()
        date = self.schedule_date_cal.get_date()
        time = self.schedule_time_cb.get()
        payment_status = self.payment_status_cb.get()

        if not member_name or not wellbeing_name or not date or not time or not payment_status:
            messagebox.showerror("Error", "All fields are required.")
            return

        # Get member_id from member_name
        member = MemberManagement.search_member(name=member_name)
        if not member:
            messagebox.showerror("Error", "Selected member not found.")
            return
        member_id = member["member_id"]

        # Get wellbeing staff member_id
        wellbeing_staff = MemberManagement.search_member(name=wellbeing_name)
        if not wellbeing_staff or wellbeing_staff["user_type"] != "Wellbeing Staff":
            messagebox.showerror("Error", "Selected wellbeing staff not found or invalid.")
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
            return

        try:
            AppointmentManager.schedule_appointment(member_id, wellbeing_id, date, time, cost, payment_status)
            messagebox.showinfo("Success", "Appointment scheduled successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to schedule appointment: {e}")

    # View All Appointments Tab
    def create_view_tab(self):
        columns = ("ID", "Wellbeing Staff Name", "Specialty", "Gym User Name", "Gym Name", "Date", "Time", "Cost", "Status")
        self.view_tree = ttk.Treeview(self.view_tab, columns=columns, show="headings")
        for col in columns:
            self.view_tree.heading(col, text=col)
        self.view_tree.pack(expand=True, fill="both")

        view_button = ttk.Button(self.view_tab, text="Refresh", command=self.view_all_appointments)
        view_button.pack(pady=5)

    def view_all_appointments(self):
        for row in self.view_tree.get_children():
            self.view_tree.delete(row)
        appointments = AppointmentManager.view_all_appointments_enriched()
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

    # Update Appointment Tab
    def create_update_tab(self):
        caption = ttk.Label(self.update_tab, text="Please select from table below", font=("Helvetica", 10, "bold"))
        caption.pack(pady=5)

        columns = ("ID", "Wellbeing Staff Name", "Specialty", "Gym User Name", "Gym Name", "Date", "Time", "Cost", "Status")
        self.update_tree = ttk.Treeview(self.update_tab, columns=columns, show="headings")
        for col in columns:
            self.update_tree.heading(col, text=col)
        self.update_tree.bind("<<TreeviewSelect>>", self.on_update_select)
        self.update_tree.pack(expand=True, fill="both")

        frame = ttk.Frame(self.update_tab)
        frame.pack(pady=5)

        ttk.Label(frame, text="New Date:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.update_date_cal = Calendar(frame, selectmode="day", date_pattern="yyyy-mm-dd")
        self.update_date_cal.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(frame, text="New Time:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.update_time_cb = ttk.Combobox(frame, values=self.get_time_intervals(), state="readonly")
        self.update_time_cb.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        update_button = ttk.Button(frame, text="Update Appointment", command=self.update_appointment)
        update_button.grid(row=2, column=0, columnspan=2, pady=10)

        refresh_button = ttk.Button(self.update_tab, text="Refresh", command=self.load_update_appointments)
        refresh_button.pack(pady=5)

        self.load_update_appointments()

    def load_update_appointments(self):
        for row in self.update_tree.get_children():
            self.update_tree.delete(row)
        appointments = AppointmentManager.view_all_appointments_enriched()
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

    def on_update_select(self, event):
        selection = self.update_tree.selection()
        if selection:
            item = self.update_tree.item(selection[0])
            self.selected_update_appt_id = item["values"][0]  # ID is the first column

    def update_appointment(self):
        if not self.selected_update_appt_id:
            messagebox.showerror("Error", "Please select an appointment from the table.")
            return
        new_date = self.update_date_cal.get_date()
        new_time = self.update_time_cb.get()
        if not new_date or not new_time:
            messagebox.showerror("Error", "Please select date and time.")
            return

        appt = AppointmentManager.get_appointment_by_id(self.selected_update_appt_id)
        if not appt:
            messagebox.showerror("Error", "Appointment not found.")
            return

        wellbeing_id = appt["trainer_id"]
        if AppointmentManager.is_double_booked(wellbeing_id, new_date, new_time, exclude_id=self.selected_update_appt_id):
            messagebox.showerror("Error", "This wellbeing staff is already booked at the selected date & time.")
            return

        if AppointmentManager.update_appointment(self.selected_update_appt_id, new_date, new_time):
            messagebox.showinfo("Success", "Appointment updated successfully.")
            self.load_update_appointments()
        else:
            messagebox.showerror("Error", "Failed to update appointment.")

    # Delete Appointment Tab
    def create_delete_tab(self):
        caption = ttk.Label(self.delete_tab, text="Please select from table below", font=("Helvetica", 10, "bold"))
        caption.pack(pady=5)

        columns = ("ID", "Wellbeing Staff Name", "Specialty", "Gym User Name", "Gym Name", "Date", "Time", "Cost", "Status")
        self.delete_tree = ttk.Treeview(self.delete_tab, columns=columns, show="headings")
        for col in columns:
            self.delete_tree.heading(col, text=col)
        self.delete_tree.bind("<<TreeviewSelect>>", self.on_delete_select)
        self.delete_tree.pack(expand=True, fill="both")

        delete_button = ttk.Button(self.delete_tab, text="Delete Appointment", command=self.delete_appointment)
        delete_button.pack(pady=10)

        self.load_delete_appointments()

    def load_delete_appointments(self):
        for row in self.delete_tree.get_children():
            self.delete_tree.delete(row)
        appointments = AppointmentManager.view_all_appointments_enriched()
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

    def on_delete_select(self, event):
        selection = self.delete_tree.selection()
        if selection:
            item = self.delete_tree.item(selection[0])
            self.selected_delete_appt_id = item["values"][0]

    def delete_appointment(self):
        if not self.selected_delete_appt_id:
            messagebox.showerror("Error", "Please select an appointment from the table.")
            return

        if AppointmentManager.delete_appointment(self.selected_delete_appt_id):
            messagebox.showinfo("Success", "Appointment deleted successfully.")
            self.load_delete_appointments()
        else:
            messagebox.showerror("Error", "Appointment not found or could not be deleted.")

    # Search Appointment Tab
    def create_search_tab(self):
        ttk.Label(self.search_tab, text="Select Wellbeing Staff:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.search_wellbeing_cb = ttk.Combobox(self.search_tab, values=self.get_wellbeing_staff(), state="readonly")
        self.search_wellbeing_cb.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        search_button = ttk.Button(self.search_tab, text="Search", command=self.search_appointments)
        search_button.grid(row=1, column=0, columnspan=2, pady=10)

        columns = ("ID", "Wellbeing Staff Name", "Specialty", "Gym User Name", "Gym Name", "Date", "Time", "Cost", "Status")
        self.search_tree = ttk.Treeview(self.search_tab, columns=columns, show="headings")
        for col in columns:
            self.search_tree.heading(col, text=col)
        self.search_tree.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        self.search_tab.grid_columnconfigure(0, weight=1)
        self.search_tab.grid_columnconfigure(1, weight=1)
        self.search_tab.grid_rowconfigure(2, weight=1)

    def search_appointments(self):
        wellbeing_name = self.search_wellbeing_cb.get()
        if not wellbeing_name:
            messagebox.showerror("Error", "Please select a wellbeing staff.")
            return

        for row in self.search_tree.get_children():
            self.search_tree.delete(row)

        appointments = AppointmentManager.search_appointments_by_wellbeing_name(wellbeing_name)
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
'''
def main():
    root = tk.Tk()
    app = AppointmentManagerFrame(root)
    app.pack(expand=True, fill='both')
    root.mainloop()

if __name__ == "__main__":
    main()
''''''