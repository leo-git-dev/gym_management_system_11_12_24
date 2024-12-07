import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from core.attendance_tracking import AttendanceTracker
from core.member_management import MemberManagement
from core.gym_management import GymManager
from core.class_activity_manager import ClassActivityManager


class AttendanceTrackingApp:
    def __init__(self, root):
        self.attendance_tree = None
        self.equipment_used_entry = None
        self.workout_zone_entry = None
        self.minute_dropdown = None
        self.hour_dropdown = None
        self.date_calendar = None
        self.class_dropdown = None
        self.member_id_entry = None
        self.view_tab = None
        self.record_tab = None
        self.manage_attendance_id_entry = None
        self.root = root
        self.root.title("Attendance Tracking")
        self.create_widgets()

    def create_widgets(self):
        # Tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True, fill="both")

        self.record_tab = ttk.Frame(notebook)
        self.view_tab = ttk.Frame(notebook)

        notebook.add(self.record_tab, text="Record Attendance")
        notebook.add(self.view_tab, text="View/Manage Attendance Records")

        self.create_record_tab()
        self.create_view_tab()

    def create_record_tab(self):
        ttk.Label(self.record_tab, text="Member ID:").grid(row=0, column=0, padx=5, pady=5)
        self.member_id_entry = ttk.Entry(self.record_tab)
        self.member_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.record_tab, text="Class ID:").grid(row=1, column=0, padx=5, pady=5)
        self.class_dropdown = ttk.Combobox(self.record_tab, values=self.get_class_ids())
        self.class_dropdown.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.record_tab, text="Date:").grid(row=2, column=0, padx=5, pady=5)
        self.date_calendar = Calendar(self.record_tab, selectmode="day", date_pattern="yyyy-mm-dd")
        self.date_calendar.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.record_tab, text="Time:").grid(row=3, column=0, padx=5, pady=5)
        self.hour_dropdown = ttk.Combobox(self.record_tab, values=[f"{i:02d}" for i in range(24)])
        self.hour_dropdown.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        self.minute_dropdown = ttk.Combobox(self.record_tab, values=[f"{i:02d}" for i in range(60)])
        self.minute_dropdown.grid(row=3, column=1, padx=(60, 5), pady=5, sticky="e")
        self.hour_dropdown.set("00")
        self.minute_dropdown.set("00")

        ttk.Label(self.record_tab, text="Workout Zone:").grid(row=4, column=0, padx=5, pady=5)
        self.workout_zone_entry = ttk.Entry(self.record_tab)
        self.workout_zone_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(self.record_tab, text="Equipment Used:").grid(row=5, column=0, padx=5, pady=5)
        self.equipment_used_entry = ttk.Entry(self.record_tab)
        self.equipment_used_entry.grid(row=5, column=1, padx=5, pady=5)

        record_button = ttk.Button(self.record_tab, text="Record Attendance", command=self.record_attendance)
        record_button.grid(row=6, column=0, columnspan=2, pady=10)

    def create_view_tab(self):
        self.attendance_tree = ttk.Treeview(
            self.view_tab,
            columns=("ID", "Member Name", "Gym Name", "Location", "Class", "Date", "Time", "Zone", "Equipment"),
            show="headings",
        )
        self.attendance_tree.heading("ID", text="Attendance ID")
        self.attendance_tree.heading("Member Name", text="Member Name")
        self.attendance_tree.heading("Gym Name", text="Gym Name")
        self.attendance_tree.heading("Location", text="Location")
        self.attendance_tree.heading("Class", text="Class")
        self.attendance_tree.heading("Date", text="Date")
        self.attendance_tree.heading("Time", text="Time")
        self.attendance_tree.heading("Zone", text="Workout Zone")
        self.attendance_tree.heading("Equipment", text="Equipment Used")
        self.attendance_tree.pack(expand=True, fill="both")

        view_button = ttk.Button(self.view_tab, text="Refresh", command=self.view_attendance_records)
        view_button.pack(pady=5)

        manage_frame = ttk.Frame(self.view_tab)
        manage_frame.pack(fill="x")

        ttk.Label(manage_frame, text="Attendance ID:").grid(row=0, column=0, padx=5, pady=5)
        self.manage_attendance_id_entry = ttk.Entry(manage_frame)
        self.manage_attendance_id_entry.grid(row=0, column=1, padx=5, pady=5)

        update_button = ttk.Button(manage_frame, text="Update", command=self.update_attendance)
        update_button.grid(row=0, column=2, padx=5, pady=5)

        delete_button = ttk.Button(manage_frame, text="Delete", command=self.delete_attendance)
        delete_button.grid(row=0, column=3, padx=5, pady=5)

    def record_attendance(self):
        member_id = self.member_id_entry.get()
        class_id = self.class_dropdown.get()
        date = self.date_calendar.get_date()
        time = f"{self.hour_dropdown.get()}:{self.minute_dropdown.get()}"
        workout_zone = self.workout_zone_entry.get() or "General"
        equipment_used = self.equipment_used_entry.get() or "None"

        try:
            AttendanceTracker.record_attendance(member_id, class_id, date, time, workout_zone, equipment_used)
            messagebox.showinfo("Success", "Attendance recorded successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to record attendance: {e}")

    def view_attendance_records(self):
        attendance_records = AttendanceTracker.view_attendance_records()
        for row in self.attendance_tree.get_children():
            self.attendance_tree.delete(row)
        for record in attendance_records:
            member = MemberManagement.search_member(member_id=record["member_id"])
            gym_name = member.get("gym_name", "Unknown")
            location = member.get("gym_location", "Unknown")
            self.attendance_tree.insert(
                "",
                "end",
                values=(
                    record["attendance_id"],
                    member["name"],
                    gym_name,
                    location,
                    record["class_id"],
                    record["date"],
                    record["time"],
                    record["workout_zone"],
                    record["equipment_used"],
                ),
            )

    def update_attendance(self):
        attendance_id = self.manage_attendance_id_entry.get()
        # Implement logic to update attendance record using AttendanceTracker.

    def delete_attendance(self):
        attendance_id = self.manage_attendance_id_entry.get()
        # Implement logic to delete attendance record using AttendanceTracker.

    def get_class_ids(self):
        activities = ClassActivityManager.view_all_classes()
        return [activity["class_id"] for activity in activities]


if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceTrackingApp(root)
    root.mainloop()


