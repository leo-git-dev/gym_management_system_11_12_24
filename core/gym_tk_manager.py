import tkinter as tk
from tkinter import ttk, messagebox
from core.gym_management import GymManager
from core.member_management import MemberManagement
from core.payments import PaymentManager


class GymManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gym Management")
        self.create_widgets()

    def create_widgets(self):
        # Tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")

        self.add_tab = ttk.Frame(self.notebook)
        self.view_tab = ttk.Frame(self.notebook)
        self.update_tab = ttk.Frame(self.notebook)
        self.zone_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.add_tab, text="Add Gym")
        self.notebook.add(self.view_tab, text="View All Gyms")
        self.notebook.add(self.update_tab, text="Update Gym")
        self.notebook.add(self.zone_tab, text="Manage Zones")

        # Tab callbacks to update the window title
        self.notebook.bind("<<NotebookTabChanged>>", lambda e: self.update_title())

        self.create_add_tab()
        self.create_view_tab()
        self.create_update_tab()
        self.create_zone_tab()

    def update_title(self):
        """Update the window title with the selected tab name."""
        current_tab = self.notebook.tab(self.notebook.select(), "text")
        self.root.title(f"Gym Management - {current_tab}")

    def create_add_tab(self):
        ttk.Label(self.add_tab, text="Gym Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.gym_name_entry = ttk.Entry(self.add_tab)
        self.gym_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(self.add_tab, text="City:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.city_entry = ttk.Entry(self.add_tab)
        self.city_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(self.add_tab, text="Manager Name:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.manager_name_entry = ttk.Entry(self.add_tab)
        self.manager_name_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(self.add_tab, text="Manager Contact:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.manager_contact_entry = ttk.Entry(self.add_tab)
        self.manager_contact_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(self.add_tab, text="Manager Email:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.manager_email_entry = ttk.Entry(self.add_tab)
        self.manager_email_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        add_button = ttk.Button(self.add_tab, text="Add Gym", command=self.add_gym)
        add_button.grid(row=5, column=0, columnspan=2, pady=10)

    def create_view_tab(self):
        # Create a frame to contain the Treeview and scrollbars
        tree_frame = ttk.Frame(self.view_tab)
        tree_frame.pack(expand=True, fill="both", padx=5, pady=5)

        # Create vertical scrollbar
        vert_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
        vert_scrollbar.pack(side="right", fill="y")

        # Create horizontal scrollbar
        horiz_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal")
        horiz_scrollbar.pack(side="bottom", fill="x")

        # Create Treeview with scrollbars
        self.gyms_tree = ttk.Treeview(
            tree_frame,
            columns=(
                "ID",
                "Name",
                "City",
                "Manager",
                "Contact",
                "Email",
                "Total Users",
                "Total Paid",
                "Total Pending",
                "Wellbeing Staff",
                "Wellbeing Cost",
                "Training Staff",
                "Training Cost",
                "Management Staff",
                "Management Cost",
                "Zones",
            ),
            show="headings",
            yscrollcommand=vert_scrollbar.set,
            xscrollcommand=horiz_scrollbar.set,
        )
        self.gyms_tree.pack(expand=True, fill="both")

        # Configure scrollbars to work with Treeview
        vert_scrollbar.config(command=self.gyms_tree.yview)
        horiz_scrollbar.config(command=self.gyms_tree.xview)

        # Define column headings
        self.gyms_tree.heading("ID", text="ID")
        self.gyms_tree.heading("Name", text="Name")
        self.gyms_tree.heading("City", text="City")
        self.gyms_tree.heading("Manager", text="Manager")
        self.gyms_tree.heading("Contact", text="Contact")
        self.gyms_tree.heading("Email", text="Email")
        self.gyms_tree.heading("Total Users", text="Total Users")
        self.gyms_tree.heading("Total Paid", text="Total Paid")
        self.gyms_tree.heading("Total Pending", text="Total Pending")
        self.gyms_tree.heading("Wellbeing Staff", text="Wellbeing Staff")
        self.gyms_tree.heading("Wellbeing Cost", text="Wellbeing Cost")
        self.gyms_tree.heading("Training Staff", text="Training Staff")
        self.gyms_tree.heading("Training Cost", text="Training Cost")
        self.gyms_tree.heading("Management Staff", text="Management Staff")
        self.gyms_tree.heading("Management Cost", text="Management Cost")
        self.gyms_tree.heading("Zones", text="Zones")

        # Adjust column widths
        for col in self.gyms_tree["columns"]:
            self.gyms_tree.column(col, width=120, anchor="center")

        # Refresh Button
        view_button = ttk.Button(self.view_tab, text="Refresh", command=self.view_all_gyms)
        view_button.pack(pady=10)

    def create_update_tab(self):
        ttk.Label(self.update_tab, text="Gym ID:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.update_gym_id_entry = ttk.Entry(self.update_tab)
        self.update_gym_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(self.update_tab, text="Field to Update:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.update_field_entry = ttk.Combobox(self.update_tab, values=["gym_name", "city", "manager_name", "manager_contact", "manager_email"], state="readonly")
        self.update_field_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(self.update_tab, text="New Value:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.update_value_entry = ttk.Entry(self.update_tab)
        self.update_value_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        update_button = ttk.Button(self.update_tab, text="Update Gym", command=self.update_gym)
        update_button.grid(row=3, column=0, columnspan=2, pady=10)

    def create_zone_tab(self):
        self.zones_tree = ttk.Treeview(self.zone_tab, columns=("Name", "ID", "Zones"), show="headings")
        self.zones_tree.heading("Name", text="Gym Name")
        self.zones_tree.heading("ID", text="Gym ID")
        self.zones_tree.heading("Zones", text="Zones")
        self.zones_tree.pack(expand=True, fill="both", padx=5, pady=5)

        controls_frame = ttk.Frame(self.zone_tab)
        controls_frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(controls_frame, text="Gym ID:").pack(side="left", padx=5, pady=5)
        self.zone_gym_id_entry = ttk.Entry(controls_frame)
        self.zone_gym_id_entry.pack(side="left", padx=5, pady=5)

        ttk.Label(controls_frame, text="Zone Name:").pack(side="left", padx=5, pady=5)
        self.zone_name_entry = ttk.Entry(controls_frame)
        self.zone_name_entry.pack(side="left", padx=5, pady=5)

        add_zone_button = ttk.Button(controls_frame, text="Add Zone", command=self.add_zone)
        add_zone_button.pack(side="left", padx=5, pady=5)

        delete_zone_button = ttk.Button(controls_frame, text="Delete Zone", command=self.delete_zone)
        delete_zone_button.pack(side="left", padx=5, pady=5)

        refresh_button = ttk.Button(controls_frame, text="Refresh Zones", command=self.view_zones)
        refresh_button.pack(side="left", padx=5, pady=5)

    def add_gym(self):
        name = self.gym_name_entry.get().strip()
        city = self.city_entry.get().strip()
        manager_name = self.manager_name_entry.get().strip()
        manager_contact = self.manager_contact_entry.get().strip()
        manager_email = self.manager_email_entry.get().strip()

        try:
            if not all([name, city, manager_name, manager_contact, manager_email]):
                raise ValueError("All fields are required.")

            GymManager.add_gym(name, city, manager_name, manager_contact, manager_email)
            messagebox.showinfo("Success", "Gym added successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add gym: {e}")

    def view_all_gyms(self):
        """
        Display gym details with added manager information, staff details, and financial metrics.
        """
        self.gyms_tree.delete(*self.gyms_tree.get_children())  # Clear existing table rows

        gyms = GymManager.view_all_gyms()

        for gym in gyms:
            gym_id = gym["gym_id"]
            manager_name = gym.get("manager_name", "N/A")
            manager_contact = gym.get("manager_contact", "N/A")
            manager_email = gym.get("manager_email", "N/A")  # Ensure email field is included

            # Calculate totals for gym users
            total_users = MemberManagement.count_users_by_gym(gym_id)

            # Calculate financial metrics
            total_paid = PaymentManager.calculate_total_membership_value(gym_id, status="Paid")
            total_pending = PaymentManager.calculate_total_membership_value(gym_id, status="Pending")

            # Get staff totals and costs
            staff_totals = MemberManagement.calculate_staff_totals_by_gym(gym_id)
            wellbeing_count = staff_totals["Wellbeing Staff"]["count"]
            wellbeing_cost = staff_totals["Wellbeing Staff"]["cost"]
            training_count = staff_totals["Training Staff"]["count"]
            training_cost = staff_totals["Training Staff"]["cost"]
            management_count = staff_totals["Management Staff"]["count"]
            management_cost = staff_totals["Management Staff"]["cost"]

            # Retrieve zones
            zones = ", ".join(GymManager.view_zones(gym_id)) or "No zones available"

            # Insert data into table
            self.gyms_tree.insert(
                "",
                "end",
                values=(
                    gym_id,
                    gym["gym_name"],
                    gym["city"],
                    manager_name,
                    manager_contact,
                    manager_email,
                    total_users,
                    f"${total_paid:.2f}",
                    f"${total_pending:.2f}",
                    wellbeing_count,
                    f"${wellbeing_cost:.2f}",
                    training_count,
                    f"${training_cost:.2f}",
                    management_count,
                    f"${management_cost:.2f}",
                    zones,
                ),
            )

    def update_gym(self):
        gym_id = self.update_gym_id_entry.get().strip()
        field = self.update_field_entry.get()
        new_value = self.update_value_entry.get().strip()

        try:
            if not all([gym_id, field, new_value]):
                raise ValueError("All fields are required.")
            GymManager.update_gym(gym_id, field, new_value)
            messagebox.showinfo("Success", "Gym updated successfully.")
            self.view_all_gyms()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update gym: {e}")

    def add_zone(self):
        gym_id = self.zone_gym_id_entry.get().strip()
        zone_name = self.zone_name_entry.get().strip()

        try:
            if not all([gym_id, zone_name]):
                raise ValueError("Gym ID and Zone Name are required.")

            GymManager.add_zone(gym_id, zone_name)
            messagebox.showinfo("Success", "Zone added successfully.")
            self.view_zones()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add zone: {e}")

    def delete_zone(self):
        gym_id = self.zone_gym_id_entry.get().strip()
        zone_name = self.zone_name_entry.get().strip()

        try:
            if not all([gym_id, zone_name]):
                raise ValueError("Gym ID and Zone Name are required.")

            GymManager.delete_zone(gym_id, zone_name)
            messagebox.showinfo("Success", "Zone deleted successfully.")
            self.view_zones()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete zone: {e}")

    def view_zones(self):
        gyms = GymManager.view_all_gyms()
        for row in self.zones_tree.get_children():
            self.zones_tree.delete(row)

        for gym in gyms:
            zones = ", ".join(gym["zones"]) if gym["zones"] else "No zones available"
            self.zones_tree.insert("", "end", values=(gym["gym_name"], gym["gym_id"], zones))


if __name__ == "__main__":
    root = tk.Tk()
    app = GymManagementApp(root)
    root.mainloop()



'''
import tkinter as tk
from tkinter import ttk, messagebox
from core.gym_management import GymManager


class GymManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gym Management")
        self.create_widgets()

    def create_widgets(self):
        # Tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")

        self.add_tab = ttk.Frame(self.notebook)
        self.view_tab = ttk.Frame(self.notebook)
        self.update_tab = ttk.Frame(self.notebook)
        self.zone_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.add_tab, text="Add Gym")
        self.notebook.add(self.view_tab, text="View All Gyms")
        self.notebook.add(self.update_tab, text="Update Gym")
        self.notebook.add(self.zone_tab, text="Manage Zones")

        self.create_add_tab()
        self.create_view_tab()
        self.create_update_tab()
        self.create_zone_tab()

    def create_add_tab(self):
        ttk.Label(self.add_tab, text="Gym Name:").grid(row=0, column=0, padx=5, pady=5)
        self.gym_name_entry = ttk.Entry(self.add_tab)
        self.gym_name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.add_tab, text="City:").grid(row=1, column=0, padx=5, pady=5)
        self.city_entry = ttk.Entry(self.add_tab)
        self.city_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.add_tab, text="Manager Name:").grid(row=2, column=0, padx=5, pady=5)
        self.manager_name_entry = ttk.Entry(self.add_tab)
        self.manager_name_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.add_tab, text="Manager Contact:").grid(row=3, column=0, padx=5, pady=5)
        self.manager_contact_entry = ttk.Entry(self.add_tab)
        self.manager_contact_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self.add_tab, text="Manager Email:").grid(row=4, column=0, padx=5, pady=5)
        self.manager_email_entry = ttk.Entry(self.add_tab)
        self.manager_email_entry.grid(row=4, column=1, padx=5, pady=5)

        add_button = ttk.Button(self.add_tab, text="Add Gym", command=self.add_gym)
        add_button.grid(row=5, column=0, columnspan=2, pady=10)

    def create_view_tab(self):
        self.gyms_tree = ttk.Treeview(self.view_tab, columns=("ID", "Name", "City", "Manager", "Contact"), show="headings")
        self.gyms_tree.heading("ID", text="ID")
        self.gyms_tree.heading("Name", text="Name")
        self.gyms_tree.heading("City", text="City")
        self.gyms_tree.heading("Manager", text="Manager")
        self.gyms_tree.heading("Contact", text="Contact")
        self.gyms_tree.pack(expand=True, fill="both", padx=5, pady=5)

        view_button = ttk.Button(self.view_tab, text="Refresh", command=self.view_all_gyms)
        view_button.pack(pady=10)

    def create_update_tab(self):
        ttk.Label(self.update_tab, text="Gym ID:").grid(row=0, column=0, padx=5, pady=5)
        self.update_gym_id_entry = ttk.Entry(self.update_tab)
        self.update_gym_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.update_tab, text="Field to Update:").grid(row=1, column=0, padx=5, pady=5)
        self.update_field_entry = ttk.Combobox(self.update_tab, values=["gym_name", "city", "manager_name", "manager_contact", "manager_email"])
        self.update_field_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.update_tab, text="New Value:").grid(row=2, column=0, padx=5, pady=5)
        self.update_value_entry = ttk.Entry(self.update_tab)
        self.update_value_entry.grid(row=2, column=1, padx=5, pady=5)

        update_button = ttk.Button(self.update_tab, text="Update Gym", command=self.update_gym)
        update_button.grid(row=3, column=0, columnspan=2, pady=10)

    def create_zone_tab(self):
        # Frame for tree view
        self.zones_tree = ttk.Treeview(self.zone_tab, columns=("Name", "ID", "Zones"), show="headings")
        self.zones_tree.heading("Name", text="Gym Name")
        self.zones_tree.heading("ID", text="Gym ID")
        self.zones_tree.heading("Zones", text="Zones")
        self.zones_tree.pack(expand=True, fill="both", padx=5, pady=5)

        # Frame for controls
        controls_frame = ttk.Frame(self.zone_tab)
        controls_frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(controls_frame, text="Gym ID:").pack(side="left", padx=5, pady=5)
        self.zone_gym_id_entry = ttk.Entry(controls_frame)
        self.zone_gym_id_entry.pack(side="left", padx=5, pady=5)

        ttk.Label(controls_frame, text="Zone Name:").pack(side="left", padx=5, pady=5)
        self.zone_name_entry = ttk.Entry(controls_frame)
        self.zone_name_entry.pack(side="left", padx=5, pady=5)

        add_zone_button = ttk.Button(controls_frame, text="Add Zone", command=self.add_zone)
        add_zone_button.pack(side="left", padx=5, pady=5)

        delete_zone_button = ttk.Button(controls_frame, text="Delete Zone", command=self.delete_zone)
        delete_zone_button.pack(side="left", padx=5, pady=5)

        refresh_button = ttk.Button(controls_frame, text="Refresh Zones", command=self.view_zones)
        refresh_button.pack(side="left", padx=5, pady=5)

    def add_gym(self):
        name = self.gym_name_entry.get()
        city = self.city_entry.get()
        manager_name = self.manager_name_entry.get()
        manager_contact = self.manager_contact_entry.get()
        manager_email = self.manager_email_entry.get()

        try:
            GymManager.add_gym(name, city, manager_name, manager_contact, manager_email)
            messagebox.showinfo("Success", "Gym added successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add gym: {e}")

    def view_all_gyms(self):
        gyms = GymManager.view_all_gyms()
        for row in self.gyms_tree.get_children():
            self.gyms_tree.delete(row)
        for gym in gyms:
            self.gyms_tree.insert("", "end", values=(gym["gym_id"], gym["gym_name"], gym["city"], gym["manager_name"], gym["manager_contact"]))

    def update_gym(self):
        gym_id = self.update_gym_id_entry.get()
        field = self.update_field_entry.get()
        new_value = self.update_value_entry.get()

        try:
            GymManager.update_gym(gym_id, field, new_value)
            messagebox.showinfo("Success", "Gym updated successfully.")
            self.view_all_gyms()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update gym: {e}")

    def add_zone(self):
        gym_id = self.zone_gym_id_entry.get()
        zone_name = self.zone_name_entry.get()

        try:
            GymManager.add_zone(gym_id, zone_name)
            messagebox.showinfo("Success", "Zone added successfully.")
            self.view_zones()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add zone: {e}")

    def delete_zone(self):
        gym_id = self.zone_gym_id_entry.get()
        zone_name = self.zone_name_entry.get()

        try:
            GymManager.delete_zone(gym_id, zone_name)
            messagebox.showinfo("Success", "Zone deleted successfully.")
            self.view_zones()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete zone: {e}")

    def view_zones(self):
        gyms = GymManager.view_all_gyms()
        for row in self.zones_tree.get_children():
            self.zones_tree.delete(row)
        for gym in gyms:
            zones = ", ".join(gym["zones"]) if gym["zones"] else "No zones available"
            self.zones_tree.insert("", "end", values=(gym["gym_name"], gym["gym_id"], zones))


if __name__ == "__main__":
    root = tk.Tk()
    app = GymManagementApp(root)
    root.mainloop()
'''
