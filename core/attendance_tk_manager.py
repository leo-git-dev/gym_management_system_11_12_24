# attendance_tracking_gui.py

import tkinter as tk
from tkinter import ttk, messagebox
from core.attendance_tracking import AttendanceManager
from core.class_activity_manager import ClassActivityManager
from core.member_management import MemberManagement
from core.gym_management import GymManager
from datetime import datetime

# Define constants for date format
DATE_FORMAT = "%Y-%m-%d"


class AttendanceTrackingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance Tracking")
        self.create_widgets()

    def create_widgets(self):
        # Main Frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill="both", expand=True)

        # Section 1: Mark Attendance
        mark_frame = ttk.LabelFrame(main_frame, text="Mark Attendance")
        mark_frame.pack(fill="x", pady=5)

        # Select Class
        ttk.Label(mark_frame, text="Select Class:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.mark_class_dropdown = ttk.Combobox(mark_frame, values=self.get_class_display_names(), state="readonly",
                                                width=50)
        self.mark_class_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.mark_class_dropdown.set("Select Class")
        self.mark_class_dropdown.bind("<<ComboboxSelected>>", self.load_mark_attendance_users)

        # Select Date
        ttk.Label(mark_frame, text="Select Date (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.mark_date_entry = ttk.Entry(mark_frame, width=53)
        self.mark_date_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.mark_date_entry.insert(0, datetime.now().strftime(DATE_FORMAT))  # Default to today

        # Users List with Checkboxes
        users_frame = ttk.LabelFrame(mark_frame, text="Registered Gym Users")
        users_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=10, sticky="ew")

        # Canvas and Scrollbar for Users List
        canvas = tk.Canvas(users_frame, height=200)
        scrollbar = ttk.Scrollbar(users_frame, orient="vertical", command=canvas.yview)
        self.users_inner_frame = ttk.Frame(canvas)

        self.users_inner_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.users_inner_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # List to hold checkbox variables
        self.mark_user_checkboxes = []

        # Mark Attendance Button
        mark_button = ttk.Button(mark_frame, text="Mark Attendance", command=self.mark_attendance)
        mark_button.grid(row=3, column=0, columnspan=2, pady=5)

        # Separator
        separator = ttk.Separator(main_frame, orient="horizontal")
        separator.pack(fill="x", pady=10)

        # Section 2: View Attendance
        view_frame = ttk.LabelFrame(main_frame, text="View Attendance")
        view_frame.pack(fill="x", pady=5)

        # Select Class for Viewing
        ttk.Label(view_frame, text="Select Class:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.view_class_dropdown = ttk.Combobox(view_frame, values=self.get_class_display_names(), state="readonly",
                                                width=50)
        self.view_class_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.view_class_dropdown.set("Select Class")

        # Select Date for Viewing
        ttk.Label(view_frame, text="Select Date (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.view_date_entry = ttk.Entry(view_frame, width=53)
        self.view_date_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.view_date_entry.insert(0, datetime.now().strftime(DATE_FORMAT))  # Default to today

        # View Attendance Button
        view_button = ttk.Button(view_frame, text="View Attendance", command=self.view_attendance)
        view_button.grid(row=2, column=0, columnspan=2, pady=5)

        # Attendance Display Treeview
        self.attendance_display_tree = ttk.Treeview(main_frame, columns=("User ID", "User Name", "Date", "Timestamp"),
                                                    show="headings")
        self.attendance_display_tree.heading("User ID", text="User ID")
        self.attendance_display_tree.heading("User Name", text="User Name")
        self.attendance_display_tree.heading("Date", text="Date")
        self.attendance_display_tree.heading("Timestamp", text="Timestamp")
        self.attendance_display_tree.pack(fill="both", expand=True, padx=5, pady=10)

    def get_class_display_names(self):
        """
        Retrieve all classes formatted with their IDs.

        :return: List of formatted class names.
        """
        classes = ClassActivityManager.view_all_classes()
        return [f"{cls['class_name']} (ID: {cls['class_id']})" for cls in classes]

    def load_mark_attendance_users(self, event=None):
        """
        Load gym users registered for the selected class and date.
        """
        selected_class = self.mark_class_dropdown.get()
        selected_date = self.mark_date_entry.get().strip()

        if not selected_class or selected_class == "Select Class":
            messagebox.showwarning("Validation Error", "Please select a class.")
            return

        # Extract class_id
        try:
            class_id = selected_class.split("(ID: ")[1].rstrip(")")
        except IndexError:
            messagebox.showerror("Error", "Invalid class selection format.")
            return

        # Validate date format
        try:
            datetime.strptime(selected_date, DATE_FORMAT)
        except ValueError:
            messagebox.showwarning("Validation Error", f"Please enter a valid date in {DATE_FORMAT} format.")
            return

        # Retrieve class details
        classes = ClassActivityManager.view_all_classes()
        cls = next((c for c in classes if c["class_id"] == class_id), None)
        if not cls:
            messagebox.showerror("Error", "Selected class not found.")
            return

        # Retrieve registered users
        registered_users_ids = cls.get("registered_users", [])
        if not registered_users_ids:
            messagebox.showinfo("Info", "No registered users for this class.")
            self.clear_mark_attendance_users()
            return

        # Retrieve user details
        members = MemberManagement.view_all_members()
        registered_users = [m for m in members if m["member_id"] in registered_users_ids]

        # Clear previous checkboxes
        self.clear_mark_attendance_users()

        # Retrieve existing attendance for this class and date to pre-check
        existing_attendance = AttendanceManager.get_attendance_by_class(class_id, date=selected_date)
        attended_user_ids = [record["user_id"] for record in existing_attendance]

        # Create checkboxes for each registered user
        for idx, user in enumerate(registered_users):
            var = tk.BooleanVar()
            if user["member_id"] in attended_user_ids:
                var.set(True)
            checkbox = ttk.Checkbutton(self.users_inner_frame, text=f"{user['name']} (ID: {user['member_id']})",
                                       variable=var)
            checkbox.grid(row=idx, column=0, sticky="w", padx=5, pady=2)
            self.mark_user_checkboxes.append((user["member_id"], var))

    def clear_mark_attendance_users(self):
        """
        Clear all user checkboxes in the Mark Attendance section.
        """
        for widget in self.users_inner_frame.winfo_children():
            widget.destroy()
        self.mark_user_checkboxes = []

    def mark_attendance(self):
        """
        Mark attendance based on selected users.
        """
        selected_class = self.mark_class_dropdown.get()
        selected_date = self.mark_date_entry.get().strip()

        if not selected_class or selected_class == "Select Class":
            messagebox.showwarning("Validation Error", "Please select a class.")
            return

        # Extract class_id
        try:
            class_id = selected_class.split("(ID: ")[1].rstrip(")")
        except IndexError:
            messagebox.showerror("Error", "Invalid class selection format.")
            return

        # Validate date format
        try:
            datetime.strptime(selected_date, DATE_FORMAT)
        except ValueError:
            messagebox.showwarning("Validation Error", f"Please enter a valid date in {DATE_FORMAT} format.")
            return

        # Iterate through checkboxes and add attendance records
        try:
            for user_id, var in self.mark_user_checkboxes:
                if var.get():
                    AttendanceManager.add_attendance(class_id, user_id, date=selected_date)
            messagebox.showinfo("Success", "Attendance marked successfully.")
            # Reload users to reflect changes
            self.load_mark_attendance_users()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to mark attendance: {e}")

    def view_attendance(self):
        """
        View attendance records based on selected class and date.
        """
        selected_class = self.view_class_dropdown.get()
        selected_date = self.view_date_entry.get().strip()

        if not selected_class or selected_class == "Select Class":
            messagebox.showwarning("Validation Error", "Please select a class.")
            return

        # Extract class_id
        try:
            class_id = selected_class.split("(ID: ")[1].rstrip(")")
        except IndexError:
            messagebox.showerror("Error", "Invalid class selection format.")
            return

        # Validate date format
        try:
            datetime.strptime(selected_date, DATE_FORMAT)
        except ValueError:
            messagebox.showwarning("Validation Error", f"Please enter a valid date in {DATE_FORMAT} format.")
            return

        # Retrieve attendance records
        attendance_records = AttendanceManager.get_attendance_by_class(class_id, date=selected_date)
        if not attendance_records:
            messagebox.showinfo("Info", "No attendance records found for the selected class and date.")
            self.clear_attendance_display()
            return

        # Retrieve user details
        members = MemberManagement.view_all_members()
        users_dict = {m["member_id"]: m["name"] for m in members}

        # Clear existing entries
        self.clear_attendance_display()

        # Insert attendance records
        for record in attendance_records:
            user_name = users_dict.get(record["user_id"], "Unknown User")
            self.attendance_display_tree.insert("", "end", values=(
                record["user_id"],
                user_name,
                record["date"],
                record["timestamp"]
            ))

    def clear_attendance_display(self):
        """
        Clear all entries in the attendance display treeview.
        """
        for row in self.attendance_display_tree.get_children():
            self.attendance_display_tree.delete(row)


def main():
    root = tk.Tk()
    app = AttendanceTrackingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()


