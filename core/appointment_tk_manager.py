import tkinter as tk
from tkinter import ttk, messagebox

from core.appointments import AppointmentManager


class AppointmentManagerApp:
    def __init__(self, root):
        self.search_member_entry = None
        self.search_results = None
        self.search_trainer_entry = None
        self.delete_id_entry = None
        self.update_time_entry = None
        self.trainer_id_entry = None
        self.update_date_entry = None
        self.time_entry = None
        self.date_entry = None
        self.update_id_entry = None
        self.search_tab = None
        self.delete_tab = None
        self.update_tab = None
        self.view_tab = None
        self.member_id_entry = None
        self.schedule_tab = None
        self.appointments_tree = None
        self.root = root
        self.root.title("Appointment Manager")
        self.create_widgets()

    def create_widgets(self):
        # Tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True, fill="both")

        self.schedule_tab = ttk.Frame(notebook)
        self.view_tab = ttk.Frame(notebook)
        self.update_tab = ttk.Frame(notebook)
        self.delete_tab = ttk.Frame(notebook)
        self.search_tab = ttk.Frame(notebook)

        notebook.add(self.schedule_tab, text="Schedule")
        notebook.add(self.view_tab, text="View All")
        notebook.add(self.update_tab, text="Update")
        notebook.add(self.delete_tab, text="Delete")
        notebook.add(self.search_tab, text="Search")

        self.create_schedule_tab()
        self.create_view_tab()
        self.create_update_tab()
        self.create_delete_tab()
        self.create_search_tab()

    def create_schedule_tab(self):
        ttk.Label(self.schedule_tab, text="Member ID:").grid(row=0, column=0, padx=5, pady=5)
        self.member_id_entry = ttk.Entry(self.schedule_tab)
        self.member_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.schedule_tab, text="Trainer ID:").grid(row=1, column=0, padx=5, pady=5)
        self.trainer_id_entry = ttk.Entry(self.schedule_tab)
        self.trainer_id_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.schedule_tab, text="Date (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5)
        self.date_entry = ttk.Entry(self.schedule_tab)
        self.date_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.schedule_tab, text="Time (HH:MM):").grid(row=3, column=0, padx=5, pady=5)
        self.time_entry = ttk.Entry(self.schedule_tab)
        self.time_entry.grid(row=3, column=1, padx=5, pady=5)

        schedule_button = ttk.Button(self.schedule_tab, text="Schedule Appointment", command=self.schedule_appointment)
        schedule_button.grid(row=4, column=0, columnspan=2, pady=10)

    def create_view_tab(self):
        self.appointments_tree = ttk.Treeview(self.view_tab, columns=("ID", "Member ID", "Trainer ID", "Date", "Time"), show="headings")
        self.appointments_tree.heading("ID", text="ID")
        self.appointments_tree.heading("Member ID", text="Member ID")
        self.appointments_tree.heading("Trainer ID", text="Trainer ID")
        self.appointments_tree.heading("Date", text="Date")
        self.appointments_tree.heading("Time", text="Time")
        self.appointments_tree.pack(expand=True, fill="both")

        view_button = ttk.Button(self.view_tab, text="Refresh", command=self.view_all_appointments)
        view_button.pack(pady=5)

    def create_update_tab(self):
        ttk.Label(self.update_tab, text="Appointment ID:").grid(row=0, column=0, padx=5, pady=5)
        self.update_id_entry = ttk.Entry(self.update_tab)
        self.update_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.update_tab, text="New Date (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=5)
        self.update_date_entry = ttk.Entry(self.update_tab)
        self.update_date_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.update_tab, text="New Time (HH:MM):").grid(row=2, column=0, padx=5, pady=5)
        self.update_time_entry = ttk.Entry(self.update_tab)
        self.update_time_entry.grid(row=2, column=1, padx=5, pady=5)

        update_button = ttk.Button(self.update_tab, text="Update Appointment", command=self.update_appointment)
        update_button.grid(row=3, column=0, columnspan=2, pady=10)

    def create_delete_tab(self):
        ttk.Label(self.delete_tab, text="Appointment ID:").grid(row=0, column=0, padx=5, pady=5)
        self.delete_id_entry = ttk.Entry(self.delete_tab)
        self.delete_id_entry.grid(row=0, column=1, padx=5, pady=5)

        delete_button = ttk.Button(self.delete_tab, text="Delete Appointment", command=self.delete_appointment)
        delete_button.grid(row=1, column=0, columnspan=2, pady=10)

    def create_search_tab(self):
        ttk.Label(self.search_tab, text="Member ID:").grid(row=0, column=0, padx=5, pady=5)
        self.search_member_entry = ttk.Entry(self.search_tab)
        self.search_member_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.search_tab, text="Trainer Name:").grid(row=1, column=0, padx=5, pady=5)
        self.search_trainer_entry = ttk.Entry(self.search_tab)
        self.search_trainer_entry.grid(row=1, column=1, padx=5, pady=5)

        search_button = ttk.Button(self.search_tab, text="Search", command=self.search_appointments)
        search_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.search_results = tk.Text(self.search_tab, height=15, wrap="word")
        self.search_results.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    def schedule_appointment(self):
        member_id = self.member_id_entry.get()
        trainer_id = self.trainer_id_entry.get()
        date = self.date_entry.get()
        time = self.time_entry.get()

        try:
            AppointmentManager.schedule_appointment(member_id, trainer_id, date, time)
            messagebox.showinfo("Success", "Appointment scheduled successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to schedule appointment: {e}")

    def view_all_appointments(self):
        appointments = AppointmentManager.view_all_appointments()
        for row in self.appointments_tree.get_children():
            self.appointments_tree.delete(row)
        for appt in appointments:
            self.appointments_tree.insert("", "end", values=(appt["appointment_id"], appt["member_id"], appt["trainer_id"], appt["date"], appt["time"]))

    def update_appointment(self):
        appointment_id = self.update_id_entry.get()
        new_date = self.update_date_entry.get()
        new_time = self.update_time_entry.get()

        if AppointmentManager.update_appointment(appointment_id, new_date, new_time):
            messagebox.showinfo("Success", "Appointment updated successfully.")
        else:
            messagebox.showerror("Error", "Failed to update appointment.")

    def delete_appointment(self):
        appointment_id = self.delete_id_entry.get()

        if AppointmentManager.delete_appointment(appointment_id):
            messagebox.showinfo("Success", "Appointment deleted successfully.")
        else:
            messagebox.showerror("Error", "Appointment not found.")

    def search_appointments(self):
        member_id = self.search_member_entry.get()
        trainer_name = self.search_trainer_entry.get()

        results = AppointmentManager.search_appointments(member_id=member_id, trainer_name=trainer_name)
        self.search_results.delete("1.0", tk.END)
        for result in results:
            self.search_results.insert(tk.END, f"{result}\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = AppointmentManagerApp(root)
    root.mainloop()
