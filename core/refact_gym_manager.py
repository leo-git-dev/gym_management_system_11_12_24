# core/gym_tk_manager.py

import tkinter as tk
from tkinter import ttk, messagebox
from core.gym_management import GymManager
import re
from database.data_loader import DataLoader

def is_valid_zone_name(zone_name):
    """Validate the zone name."""
    if len(zone_name) < 3 or len(zone_name) > 30:
        return False
    if not re.match("^[A-Za-z0-9 ]+$", zone_name):
        return False
    return True

class GymManagementFrame(ttk.Frame):
    def __init__(self, parent, data_loader:DataLoader):
        super().__init__(parent)
        self.parent = parent  # The Notebook
        self.create_widgets()

    def create_widgets(self):
        # Create Notebook for Tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")

        # Create Tabs
        self.add_tab = ttk.Frame(self.notebook)
        self.view_tab = ttk.Frame(self.notebook)
        self.update_tab = ttk.Frame(self.notebook)
        self.manage_zones_tab = ttk.Frame(self.notebook)  # Use a single frame

        # Add Tabs to Notebook
        self.notebook.add(self.add_tab, text="Add Gym")
        self.notebook.add(self.view_tab, text="View All Gyms")
        self.notebook.add(self.update_tab, text="Update Gym")
        self.notebook.add(self.manage_zones_tab, text="Manage Zones")  # Add the single frame

        # Bind tab change to update title
        self.notebook.bind("<<NotebookTabChanged>>", lambda e: self.update_title())

        # Initialize Tabs
        self.create_add_gym_tab()
        self.create_view_gym_tab()
        self.create_update_gym_tab()
        self.create_manage_zones_tab()

    def update_title(self):
        current_tab = self.notebook.tab(self.notebook.select(), "text")
        # Assuming the main application title includes "Gym Management System"
        # Adjust as necessary based on the main application's title configuration
        self.master.title(f"Gym Management System - {current_tab}")

    def create_add_gym_tab(self):
        """Create the Add Gym tab with input fields and a submission button."""
        # Labels and Entry Fields for Adding Gym
        labels = ["Gym Name:", "City:", "Manager Name:", "Manager Contact:", "Manager Email:"]
        self.add_entries = {}

        for idx, text in enumerate(labels):
            label = ttk.Label(self.add_tab, text=text)
            label.grid(row=idx, column=0, padx=10, pady=10, sticky="e")
            entry = ttk.Entry(self.add_tab, width=30)
            entry.grid(row=idx, column=1, padx=10, pady=10, sticky="w")
            self.add_entries[text] = entry

        # Add Gym Button
        add_button = ttk.Button(self.add_tab, text="Add Gym", command=self.add_gym)
        add_button.grid(row=len(labels), column=0, columnspan=2, pady=20)

    def create_view_gym_tab(self):
        """Create the View All Gyms tab with a Treeview to display gym details."""
        # Frame for Treeview and Scrollbars
        tree_frame = ttk.Frame(self.view_tab)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")

        # Define Columns
        columns = (
            "ID",
            "Name",
            "City",
            "Manager",
            "Contact",
            "Email",
            "Total Members",
            "Total Paid",
            "Total Pending",
            "Wellbeing Staff",
            "Wellbeing Cost",
            "Training Staff",
            "Training Cost",
            "Management Staff",
            "Management Cost",
            "Zones",
        )

        # Create Treeview
        self.gyms_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set
        )

        # Configure Scrollbars
        vsb.config(command=self.gyms_tree.yview)
        hsb.config(command=self.gyms_tree.xview)
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")
        self.gyms_tree.pack(fill="both", expand=True)

        # Define Headings
        for col in columns:
            self.gyms_tree.heading(col, text=col)
            self.gyms_tree.column(col, width=100, anchor="center")

        # Bind Double-Click for Detailed View
        self.gyms_tree.bind("<Double-1>", self.on_gym_double_click)

        # Buttons Frame
        buttons_frame = ttk.Frame(self.view_tab)
        buttons_frame.pack(pady=10)

        # Refresh Button
        refresh_button = ttk.Button(buttons_frame, text="Refresh", command=self.view_all_gyms)
        refresh_button.pack(side="left", padx=5)

        # Delete Button
        delete_button = ttk.Button(buttons_frame, text="Delete Gym", command=self.delete_selected_gym)
        delete_button.pack(side="left", padx=5)

        # Initial Load
        self.view_all_gyms()

    def create_update_gym_tab(self):
        """Create the Update Gym tab with selection and update fields."""
        # Labels and Comboboxes for Updating Gym
        ttk.Label(self.update_tab, text="Select Gym:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.update_gym_combo = ttk.Combobox(self.update_tab, values=self.get_all_gym_names(), state="readonly", width=28)
        self.update_gym_combo.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        ttk.Label(self.update_tab, text="Field to Update:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.update_field_combo = ttk.Combobox(
            self.update_tab,
            values=["gym_name", "city", "manager_name", "manager_contact", "manager_email"],
            state="readonly",
            width=28
        )
        self.update_field_combo.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        ttk.Label(self.update_tab, text="New Value:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.update_value_entry = ttk.Entry(self.update_tab, width=30)
        self.update_value_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Update Gym Button
        update_button = ttk.Button(self.update_tab, text="Update Gym", command=self.update_gym)
        update_button.grid(row=3, column=0, columnspan=2, pady=20)

    def create_manage_zones_tab(self):
        """Create the Manage Zones tab with gym selection and zone operations."""
        # Frame for Gym Selection
        selection_frame = ttk.Frame(self.manage_zones_tab, padding=20)
        selection_frame.pack(fill='x', expand=True)

        gym_label = ttk.Label(selection_frame, text="Select Gym:")
        gym_label.grid(row=0, column=0, sticky='w', pady=5)

        self.manage_zones_gym_combobox = ttk.Combobox(selection_frame, state="readonly")
        self.manage_zones_gym_combobox.grid(row=0, column=1, pady=5, sticky='ew')
        self.manage_zones_gym_combobox.bind("<<ComboboxSelected>>", self.display_zones)

        # Configure grid weights
        selection_frame.columnconfigure(1, weight=1)

        # Frame for Zones List
        zones_frame = ttk.Frame(self.manage_zones_tab, padding=20)
        zones_frame.pack(fill='both', expand=True)

        # Treeview to display zones
        self.zones_tree = ttk.Treeview(zones_frame, columns=("Zone Name",), show='headings', selectmode='browse')
        self.zones_tree.heading("Zone Name", text="Zone Name")
        self.zones_tree.column("Zone Name", anchor='center')
        self.zones_tree.pack(fill='both', expand=True, side='left')

        # Scrollbar for Treeview
        scrollbar = ttk.Scrollbar(zones_frame, orient="vertical", command=self.zones_tree.yview)
        self.zones_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(fill='y', side='right')

        # Frame for Zone Operations
        operations_frame = ttk.Frame(self.manage_zones_tab, padding=20)
        operations_frame.pack(fill='x', expand=True)

        # Add Zone Section
        add_label = ttk.Label(operations_frame, text="Zone Name:")
        add_label.grid(row=0, column=0, sticky='w', pady=5)

        self.add_zone_entry = ttk.Entry(operations_frame, width=20)
        self.add_zone_entry.grid(row=0, column=1, pady=5, sticky='w')

        add_zone_button = ttk.Button(operations_frame, text="Add Zone", command=self.add_zone_to_selected_gym)
        add_zone_button.grid(row=0, column=2, padx=10, pady=5)

        # Update Zone Section
        update_label = ttk.Label(operations_frame, text="New Zone Name:")
        update_label.grid(row=1, column=0, sticky='w', pady=5)

        self.update_zone_entry = ttk.Entry(operations_frame, width=20)
        self.update_zone_entry.grid(row=1, column=1, pady=5, sticky='w')

        update_zone_button = ttk.Button(operations_frame, text="Update Selected Zone", command=self.update_zone)
        update_zone_button.grid(row=1, column=2, padx=10, pady=5)

        # Delete Zone Button
        delete_zone_button = ttk.Button(operations_frame, text="Delete Selected Zone", command=self.delete_zone)
        delete_zone_button.grid(row=2, column=2, padx=10, pady=5)

        # Configure grid weights
        operations_frame.columnconfigure(1, weight=1)

        # Initialize zones_tree before refreshing the gym list
        self.display_zones()

        # Refresh Gym List after zones_tree is initialized
        self.refresh_manage_zones_gym_list()

    def add_gym(self):
        """Handle adding a new gym."""
        # Retrieve input data
        name = self.add_entries["Gym Name:"].get().strip()
        city = self.add_entries["City:"].get().strip()
        manager_name = self.add_entries["Manager Name:"].get().strip()
        manager_contact = self.add_entries["Manager Contact:"].get().strip()
        manager_email = self.add_entries["Manager Email:"].get().strip()

        try:
            # Validate inputs
            if not all([name, city, manager_name, manager_contact, manager_email]):
                raise ValueError("All fields are required.")

            # Add gym via GymManager
            GymManager.add_gym(name, city, manager_name, manager_contact, manager_email)
            messagebox.showinfo("Success", f"Gym '{name}' added successfully.")

            # Clear input fields
            for entry in self.add_entries.values():
                entry.delete(0, tk.END)

            # Refresh Gym Lists
            self.view_all_gyms()
            self.update_gym_combo['values'] = self.get_all_gym_names()
            self.refresh_manage_zones_gym_list()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add gym: {e}")

    def view_all_gyms(self):
        """Retrieve and display all gyms in the Treeview."""
        try:
            # Clear existing data
            for item in self.gyms_tree.get_children():
                self.gyms_tree.delete(item)

            # Retrieve gym data
            gyms = GymManager.view_all_gyms()

            for gym in gyms:
                self.gyms_tree.insert("", "end", values=(
                    gym["gym_id"],
                    gym["gym_name"],
                    gym["city"],
                    gym["manager_name"],
                    gym["manager_contact"],
                    gym["manager_email"],
                    gym.get("total_members", 0),
                    f"${gym.get('revenue', {}).get('Total Paid', 0):.2f}",
                    f"${gym.get('revenue', {}).get('Total Pending', 0):.2f}",
                    gym.get("activities", {}).get("Wellbeing Staff", {}).get("count", 0),
                    f"${gym.get('activities', {}).get('Wellbeing Staff', {}).get('cost', 0):.2f}",
                    gym.get("activities", {}).get("Training Staff", {}).get("count", 0),
                    f"${gym.get('activities', {}).get('Training Staff', {}).get('cost', 0):.2f}",
                    gym.get("activities", {}).get("Management Staff", {}).get("count", 0),
                    f"${gym.get('activities', {}).get('Management Staff', {}).get('cost', 0):.2f}",
                    ", ".join(gym["zones"]) if gym.get("zones") else "No Zones"
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to retrieve gyms: {e}")

    def delete_selected_gym(self):
        """Handle deletion of the selected gym."""
        selected = self.gyms_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a gym to delete.")
            return

        gym_values = self.gyms_tree.item(selected[0])["values"]
        gym_id = gym_values[0]
        gym_name = gym_values[1]

        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete gym '{gym_name}' (ID: {gym_id})?")
        if not confirm:
            return

        try:
            GymManager.delete_gym(gym_id)
            messagebox.showinfo("Success", f"Gym '{gym_name}' deleted successfully.")
            self.view_all_gyms()
            self.zones_tree.delete(*self.zones_tree.get_children())
            self.display_zones()
            self.update_gym_combo['values'] = self.get_all_gym_names()
            self.refresh_manage_zones_gym_list()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete gym: {e}")

    def update_gym(self):
        """Handle updating gym details."""
        gym_name = self.update_gym_combo.get()
        field = self.update_field_combo.get()
        new_value = self.update_value_entry.get().strip()

        try:
            # Validate inputs
            if not gym_name:
                raise ValueError("Please select a gym to update.")
            if not field:
                raise ValueError("Please select a field to update.")
            if not new_value:
                raise ValueError("Please enter a new value.")

            # Retrieve gym ID
            gyms = GymManager.view_all_gyms()
            gym = next((g for g in gyms if g["gym_name"] == gym_name), None)
            if not gym:
                raise ValueError("Selected gym not found.")

            gym_id = gym["gym_id"]

            # Update gym via GymManager
            GymManager.update_gym(gym_id, field, new_value)
            messagebox.showinfo("Success", f"Gym '{gym_name}' updated successfully.")

            # Refresh Gym Lists
            self.view_all_gyms()
            self.update_gym_combo['values'] = self.get_all_gym_names()
            self.refresh_manage_zones_gym_list()

            # Clear update fields
            self.update_gym_combo.set('')
            self.update_field_combo.set('')
            self.update_value_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update gym: {e}")

    def on_gym_double_click(self, event):
        """Display detailed information about the selected gym."""
        selected = self.gyms_tree.selection()
        if not selected:
            return

        gym_values = self.gyms_tree.item(selected[0])["values"]
        gym_id = gym_values[0]
        gym_name = gym_values[1]
        city = gym_values[2]
        manager_name = gym_values[3]
        manager_contact = gym_values[4]
        manager_email = gym_values[5]
        total_members = gym_values[6]
        total_paid = gym_values[7]
        total_pending = gym_values[8]
        wellbeing_staff = gym_values[9]
        wellbeing_cost = gym_values[10]
        training_staff = gym_values[11]
        training_cost = gym_values[12]
        management_staff = gym_values[13]
        management_cost = gym_values[14]
        zones = gym_values[15]

        details = (
            f"Gym ID: {gym_id}\n"
            f"Name: {gym_name}\n"
            f"City: {city}\n"
            f"Manager Name: {manager_name}\n"
            f"Manager Contact: {manager_contact}\n"
            f"Manager Email: {manager_email}\n"
            f"Total Members: {total_members}\n"
            f"Total Paid: {total_paid}\n"
            f"Total Pending: {total_pending}\n"
            f"Wellbeing Staff: {wellbeing_staff}\n"
            f"Wellbeing Cost: {wellbeing_cost}\n"
            f"Training Staff: {training_staff}\n"
            f"Training Cost: {training_cost}\n"
            f"Management Staff: {management_staff}\n"
            f"Management Cost: {management_cost}\n"
            f"Zones: {zones}"
        )

        messagebox.showinfo("Gym Details", details)

    def get_all_gym_names(self):
        """Retrieve all gym names for the combobox."""
        try:
            gyms = GymManager.view_all_gyms()
            return [gym["gym_name"] for gym in gyms]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to retrieve gym names: {e}")
            return []

    def refresh_manage_zones_gym_list(self):
        """Refresh the list of gyms in the Manage Zones Combobox."""
        try:
            gyms = GymManager.view_all_gyms()
            self.manage_zones_gyms = gyms  # Store gyms for easy access
            gym_names = [gym["gym_name"] for gym in gyms]
            self.manage_zones_gym_combobox['values'] = gym_names
            if gym_names:
                self.manage_zones_gym_combobox.current(0)
                self.display_zones()
            else:
                self.manage_zones_gym_combobox.set('')  # Clear selection if no gyms are available
                self.zones_tree.delete(*self.zones_tree.get_children())
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh gym list: {e}")

    def display_zones(self, event=None):
        """Display zones for the selected gym in the Treeview."""
        selected_gym_name = self.manage_zones_gym_combobox.get().strip()
        if not selected_gym_name:
            return

        # Retrieve gym_id based on gym_name
        selected_gym = next((gym for gym in self.manage_zones_gyms if gym["gym_name"] == selected_gym_name), None)
        if not selected_gym:
            messagebox.showerror("Selection Error", "Selected gym not found.")
            return
        gym_id = selected_gym["gym_id"]

        # Retrieve zones for the gym
        zones = GymManager.view_zones(gym_id)

        # Clear existing zones in the Treeview
        self.zones_tree.delete(*self.zones_tree.get_children())

        # Insert zones into the Treeview
        for zone in zones:
            self.zones_tree.insert("", "end", values=(zone,))

    def add_zone_to_selected_gym(self):
        """Handle adding a new zone to the selected gym."""
        selected_gym_name = self.manage_zones_gym_combobox.get().strip()
        new_zone = self.add_zone_entry.get().strip()

        # Validation
        if not selected_gym_name:
            messagebox.showwarning("Input Error", "Please select a gym.")
            return
        if not new_zone:
            messagebox.showwarning("Input Error", "Please enter a zone name.")
            return
        if not is_valid_zone_name(new_zone):
            messagebox.showwarning("Input Error",
                                   "Zone name must be 3-30 characters long and contain only letters, numbers, and spaces.")
            return

        # Confirmation Dialog
        confirm = messagebox.askyesno("Confirm Addition",
                                      f"Are you sure you want to add zone '{new_zone}' to '{selected_gym_name}'?")
        if not confirm:
            return

        # Retrieve gym_id based on gym_name
        selected_gym = next((gym for gym in self.manage_zones_gyms if gym["gym_name"] == selected_gym_name), None)
        if not selected_gym:
            messagebox.showerror("Selection Error", "Selected gym not found.")
            return
        gym_id = selected_gym["gym_id"]

        # Attempt to add the zone
        try:
            GymManager.add_zone(gym_id, new_zone)
            messagebox.showinfo("Success", f"Zone '{new_zone}' added to '{selected_gym_name}'.")
            self.add_zone_entry.delete(0, tk.END)  # Clear the entry field
            self.display_zones()  # Refresh the zones list
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def update_zone(self):
        """Handle updating the selected zone."""
        selected_item = self.zones_tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a zone to update.")
            return

        old_zone_name = self.zones_tree.item(selected_item, "values")[0]
        new_zone_name = self.update_zone_entry.get().strip()

        if not new_zone_name:
            messagebox.showwarning("Input Error", "Please enter a new zone name.")
            return
        if not is_valid_zone_name(new_zone_name):
            messagebox.showwarning("Input Error",
                                   "Zone name must be 3-30 characters long and contain only letters, numbers, and spaces.")
            return

        selected_gym_name = self.manage_zones_gym_combobox.get().strip()
        selected_gym = next((gym for gym in self.manage_zones_gyms if gym["gym_name"] == selected_gym_name), None)
        if not selected_gym:
            messagebox.showerror("Selection Error", "Selected gym not found.")
            return
        gym_id = selected_gym["gym_id"]

        # Confirmation Dialog
        confirm = messagebox.askyesno("Confirm Update",
                                      f"Are you sure you want to rename zone '{old_zone_name}' to '{new_zone_name}'?")
        if not confirm:
            return

        # Attempt to update the zone
        try:
            GymManager.update_zone(gym_id, old_zone_name, new_zone_name)
            messagebox.showinfo("Success", f"Zone '{old_zone_name}' updated to '{new_zone_name}'.")
            self.update_zone_entry.delete(0, tk.END)  # Clear the entry field
            self.display_zones()  # Refresh the zones list
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def delete_zone(self):
        """Handle deleting the selected zone."""
        selected_item = self.zones_tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a zone to delete.")
            return

        zone_name = self.zones_tree.item(selected_item, "values")[0]
        selected_gym_name = self.manage_zones_gym_combobox.get().strip()
        selected_gym = next((gym for gym in self.manage_zones_gyms if gym["gym_name"] == selected_gym_name), None)
        if not selected_gym:
            messagebox.showerror("Selection Error", "Selected gym not found.")
            return
        gym_id = selected_gym["gym_id"]

        # Confirmation Dialog
        confirm = messagebox.askyesno("Confirm Deletion",
                                      f"Are you sure you want to delete zone '{zone_name}' from '{selected_gym_name}'?")
        if not confirm:
            return

        # Attempt to delete the zone
        try:
            GymManager.delete_zone(gym_id, zone_name)
            messagebox.showinfo("Success", f"Zone '{zone_name}' deleted from '{selected_gym_name}'.")
            self.display_zones()  # Refresh the zones list
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
