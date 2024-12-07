import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from core.payments import PaymentManager
from core.member_management import MemberManagement

class PaymentManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Payment Management")
        self.selected_payment_id = None
        self.create_widgets()

    def create_widgets(self):
        # Tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")

        self.add_tab = ttk.Frame(self.notebook)
        self.view_tab = ttk.Frame(self.notebook)
        self.update_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.add_tab, text="Add Payment")
        self.notebook.add(self.view_tab, text="View Payments")
        self.notebook.add(self.update_tab, text="Update/Delete Payment")

        self.create_add_tab()
        self.create_view_tab()
        self.create_update_tab()

        # Add tab-switching callback to display tab name
        self.notebook.bind("<<NotebookTabChanged>>", lambda e: self.update_title(self.notebook.tab(self.notebook.select(), "text")))

    def update_title(self, title):
        """Update window title with the current tab name."""
        self.root.title(f"Payment Management - {title}")

    # Add Payment Tab
    def create_add_tab(self):
        ttk.Label(self.add_tab, text="Select User (Gym Users only):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.user_dropdown = ttk.Combobox(self.add_tab, values=self.get_gym_user_names(), state="readonly")
        self.user_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.user_dropdown.bind("<<ComboboxSelected>>", self.display_user_details)

        self.details_frame = ttk.Frame(self.add_tab)
        self.details_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        ttk.Label(self.add_tab, text="Amount:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.amount_entry = ttk.Entry(self.add_tab)
        self.amount_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(self.add_tab, text="Payment Date:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.payment_date_calendar = Calendar(
            self.add_tab,
            selectmode="day",
            date_pattern="yyyy-mm-dd",
            background="white",
            foreground="gray",
            headersbackground="black",
        )
        self.payment_date_calendar.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(self.add_tab, text="Payment Status:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.status_dropdown = ttk.Combobox(self.add_tab, values=["Paid", "Pending"], state="readonly")
        self.status_dropdown.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        self.status_dropdown.set("Paid")  # Default value

        ttk.Button(self.add_tab, text="Add Payment", command=self.add_payment).grid(row=5, column=0, columnspan=2, pady=10)

    def display_user_details(self, event=None):
        """Display selected gym user's details."""
        for widget in self.details_frame.winfo_children():
            widget.destroy()

        user_name = self.user_dropdown.get()
        user = MemberManagement.search_member(name=user_name)

        if not user:
            ttk.Label(self.details_frame, text="No details found for the selected user.").grid(row=0, column=0)
            return

        filtered_details = {
            "Member ID": user.get("member_id", "N/A"),
            "Name": user.get("name", "N/A"),
            "Membership Type": user.get("membership_type", "N/A"),
            "Join Date": user.get("join_date", "N/A"),
            "Gym ID": user.get("gym_id", "N/A"),
            "Gym Name": user.get("gym_name", "N/A"),
            "Monthly Fee": user.get("cost", "N/A"),
        }

        headers = ["Field", "Value"]
        for col, header in enumerate(headers):
            ttk.Label(self.details_frame, text=header, font=("Helvetica", 10, "bold")).grid(row=0, column=col, padx=5,
                                                                                            pady=5)

        for row, (field, value) in enumerate(filtered_details.items(), start=1):
            ttk.Label(self.details_frame, text=field).grid(row=row, column=0, padx=5, pady=5, sticky="w")
            ttk.Label(self.details_frame, text=value).grid(row=row, column=1, padx=5, pady=5, sticky="w")

    def add_payment(self):
        user_name = self.user_dropdown.get()
        amount = self.amount_entry.get()
        payment_date = self.payment_date_calendar.get_date()
        status = self.status_dropdown.get()

        try:
            if not amount.isdigit():
                raise ValueError("Amount must be a numeric value.")

            user = MemberManagement.search_member(name=user_name)
            if not user:
                raise ValueError("Selected user not found.")

            PaymentManager.add_payment(user["member_id"], amount, payment_date, status)
            messagebox.showinfo("Success", "Payment added successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add payment: {e}")

    # View Payments Tab
    def create_view_tab(self):
        self.payments_tree = ttk.Treeview(
            self.view_tab,
            columns=("ID", "Member ID", "Name", "Gym", "Amount", "Date", "Status"),
            show="headings",
        )
        self.payments_tree.heading("ID", text="Payment ID")
        self.payments_tree.heading("Member ID", text="Member ID")
        self.payments_tree.heading("Name", text="Member Name")
        self.payments_tree.heading("Gym", text="Gym Name")
        self.payments_tree.heading("Amount", text="Amount")
        self.payments_tree.heading("Date", text="Date")
        self.payments_tree.heading("Status", text="Status")
        self.payments_tree.pack(expand=True, fill="both")

        ttk.Button(self.view_tab, text="Refresh", command=self.view_all_payments).pack(pady=5)

    def view_all_payments(self):
        payments = PaymentManager.view_all_payments()
        for row in self.payments_tree.get_children():
            self.payments_tree.delete(row)
        for payment in payments:
            self.payments_tree.insert(
                "",
                "end",
                values=(
                    payment["payment_id"],
                    payment["member_id"],
                    payment["member_name"],
                    payment["gym_name"],
                    payment["amount"],
                    payment["date"],
                    payment["status"],
                ),
            )

    # Update/Delete Tab
    def create_update_tab(self):
        ttk.Label(self.update_tab, text="Select User:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.update_user_dropdown = ttk.Combobox(self.update_tab, values=self.get_gym_user_names(), state="readonly")
        self.update_user_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.update_user_dropdown.bind("<<ComboboxSelected>>", self.display_update_user_details)

        # User details
        self.update_details_frame = ttk.Frame(self.update_tab)
        self.update_details_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Payment records
        ttk.Label(self.update_tab, text="Payment Records: Please select payment to amend from table below:").grid(
            row=2, column=0, columnspan=2, padx=10, pady=5
        )
        self.payment_tree = ttk.Treeview(
            self.update_tab, columns=("ID", "Amount", "Date", "Status"), show="headings", height=5
        )
        self.payment_tree.heading("ID", text="Payment ID")
        self.payment_tree.heading("Amount", text="Amount")
        self.payment_tree.heading("Date", text="Date")
        self.payment_tree.heading("Status", text="Status")
        self.payment_tree.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.payment_tree.bind("<<TreeviewSelect>>", self.select_payment)

        # Update Fields
        ttk.Label(self.update_tab, text="Update Amount:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.update_amount_entry = ttk.Entry(self.update_tab)
        self.update_amount_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(self.update_tab, text="Update Date:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.update_date_calendar = Calendar(
            self.update_tab,
            selectmode="day",
            date_pattern="yyyy-mm-dd",
            background="white",
            foreground="gray",
            headersbackground="black",
        )
        self.update_date_calendar.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(self.update_tab, text="Update Status:").grid(row=6, column=0, padx=5, pady=5, sticky="e")
        self.update_status_dropdown = ttk.Combobox(self.update_tab, values=["Paid", "Pending"], state="readonly")
        self.update_status_dropdown.grid(row=6, column=1, padx=5, pady=5, sticky="w")

        ttk.Button(self.update_tab, text="Update Payment", command=self.update_payment).grid(row=7, column=0, pady=10, sticky="e")
        ttk.Button(self.update_tab, text="Delete Payment", command=self.delete_payment).grid(row=7, column=1, pady=10, sticky="w")

    def display_update_user_details(self, event=None):
        """Display selected user details and payment records."""
        # Clear user details and payment records
        for widget in self.update_details_frame.winfo_children():
            widget.destroy()
        for row in self.payment_tree.get_children():
            self.payment_tree.delete(row)

        user_name = self.update_user_dropdown.get()
        user = MemberManagement.search_member(name=user_name)

        if not user:
            ttk.Label(self.update_details_frame, text="No details found for the selected user.").grid(row=0, column=0)
            return

        # Display user details
        filtered_details = {
            "Member ID": user.get("member_id", "N/A"),
            "Name": user.get("name", "N/A"),
            "Membership Type": user.get("membership_type", "N/A"),
            "Join Date": user.get("join_date", "N/A"),
            "Gym ID": user.get("gym_id", "N/A"),
            "Gym Name": user.get("gym_name", "N/A"),
            "Monthly Fee": user.get("cost", "N/A"),
        }

        headers = ["Field", "Value"]
        for col, header in enumerate(headers):
            ttk.Label(self.update_details_frame, text=header, font=("Helvetica", 10, "bold")).grid(row=0, column=col, padx=5, pady=5)

        for row, (field, value) in enumerate(filtered_details.items(), start=1):
            ttk.Label(self.update_details_frame, text=field).grid(row=row, column=0, padx=5, pady=5, sticky="w")
            ttk.Label(self.update_details_frame, text=value).grid(row=row, column=1, padx=5, pady=5, sticky="w")

        # Fetch payment records
        payments = PaymentManager.get_payments_by_member_id(user["member_id"])
        for payment in payments:
            self.payment_tree.insert(
                "",
                "end",
                values=(payment["payment_id"], payment["amount"], payment["date"], payment["status"]),
            )

    def select_payment(self, event=None):
        """Handle selection of a payment record from the table."""
        selected_item = self.payment_tree.selection()
        if selected_item:
            selected_payment = self.payment_tree.item(selected_item)["values"]
            self.selected_payment_id = selected_payment[0]
            self.update_amount_entry.delete(0, tk.END)
            self.update_amount_entry.insert(0, selected_payment[1])
            self.update_date_calendar.set_date(selected_payment[2])
            self.update_status_dropdown.set(selected_payment[3])

    def update_payment(self):
        """Update payment details."""
        if not self.selected_payment_id:
            messagebox.showerror("Error", "Please select a payment to update.")
            return

        amount = self.update_amount_entry.get()
        date = self.update_date_calendar.get_date()
        status = self.update_status_dropdown.get()

        try:
            PaymentManager.update_payment(self.selected_payment_id, amount, date, status)
            messagebox.showinfo("Success", "Payment updated successfully.")
            self.display_update_user_details()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update payment: {e}")

    def delete_payment(self):
        """Delete selected payment."""
        if not self.selected_payment_id:
            messagebox.showerror("Error", "Please select a payment to delete.")
            return

        try:
            PaymentManager.delete_payment(self.selected_payment_id)
            messagebox.showinfo("Success", "Payment deleted successfully.")
            self.display_update_user_details()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete payment: {e}")

    def get_gym_user_names(self):
        """Retrieve all Gym User names from the MemberManagement system."""
        members = MemberManagement.view_all_members()
        return [member["name"] for member in members if member["user_type"] == "Gym User"]


if __name__ == "__main__":
    root = tk.Tk()
    app = PaymentManagementApp(root)
    root.mainloop()

'''import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from core.payments import PaymentManager
from core.member_management import MemberManagement


class PaymentManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Payment Management")
        self.selected_payment_id = None
        self.create_widgets()

    def create_widgets(self):
        # Tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True, fill="both")

        self.add_tab = ttk.Frame(notebook)
        self.view_tab = ttk.Frame(notebook)
        self.update_tab = ttk.Frame(notebook)

        notebook.add(self.add_tab, text="Add Payment")
        notebook.add(self.view_tab, text="View Payments")
        notebook.add(self.update_tab, text="Update/Delete Payment")

        self.create_add_tab()
        self.create_view_tab()
        self.create_update_tab()

        # Add tab-switching callback to display tab name
        notebook.bind("<<NotebookTabChanged>>", lambda e: self.update_title(notebook.tab(notebook.select(), "text")))

    def update_title(self, title):
        """Update window title with the current tab name."""
        self.root.title(f"Payment Management - {title}")

    def create_add_tab(self):
        # Select User
        ttk.Label(self.add_tab, text="Select User (Gym Users only):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.user_dropdown = ttk.Combobox(self.add_tab, values=self.get_gym_user_names(), state="readonly")
        self.user_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.user_dropdown.bind("<<ComboboxSelected>>", self.display_user_details)

        # User details table
        self.details_frame = ttk.Frame(self.add_tab)
        self.details_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Amount
        ttk.Label(self.add_tab, text="Amount:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.amount_entry = ttk.Entry(self.add_tab)
        self.amount_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Payment Date
        ttk.Label(self.add_tab, text="Payment Date:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.payment_date_calendar = Calendar(
            self.add_tab,
            selectmode="day",
            date_pattern="yyyy-mm-dd",
            background="white",
            foreground="gray",
            headersbackground="black",
            normalbackground="white",
            weekendbackground="black",
        )
        self.payment_date_calendar.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Payment Status
        ttk.Label(self.add_tab, text="Payment Status:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.status_dropdown = ttk.Combobox(self.add_tab, values=["Paid", "Pending"], state="readonly")
        self.status_dropdown.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        self.status_dropdown.set("Paid")  # Default value

        # Add Payment Button
        add_button = ttk.Button(self.add_tab, text="Add Payment", command=self.add_payment)
        add_button.grid(row=5, column=0, columnspan=2, pady=10)

    def display_user_details(self, event=None):
        """Display selected gym user's details."""
        # Clear existing details
        for widget in self.details_frame.winfo_children():
            widget.destroy()

        user_name = self.user_dropdown.get()
        user = MemberManagement.search_member(name=user_name)

        if not user:
            ttk.Label(self.details_frame, text="No details found for the selected user.").grid(row=0, column=0)
            return

        # Filter and rename user details
        filtered_details = {
            "Member ID": user.get("member_id", "N/A"),
            "Name": user.get("name", "N/A"),
            "Membership Type": user.get("membership_type", "N/A"),
            "Join Date": user.get("join_date", "N/A"),
            "Gym ID": user.get("gym_id", "N/A"),
            "Gym Name": user.get("gym_name", "N/A"),
            "Monthly Fee": user.get("cost", "N/A"),
        }

        # Display filtered details in a table format
        headers = ["Field", "Value"]
        for col, header in enumerate(headers):
            ttk.Label(self.details_frame, text=header, font=("Helvetica", 10, "bold")).grid(row=0, column=col, padx=5, pady=5)

        for row, (field, value) in enumerate(filtered_details.items(), start=1):
            ttk.Label(self.details_frame, text=field).grid(row=row, column=0, padx=5, pady=5, sticky="w")
            ttk.Label(self.details_frame, text=value).grid(row=row, column=1, padx=5, pady=5, sticky="w")

    def create_view_tab(self):
        self.payments_tree = ttk.Treeview(
            self.view_tab,
            columns=("ID", "Member ID", "Name", "Gym", "Amount", "Date", "Status"),
            show="headings",
        )
        self.payments_tree.heading("ID", text="Payment ID")
        self.payments_tree.heading("Member ID", text="Member ID")
        self.payments_tree.heading("Name", text="Member Name")
        self.payments_tree.heading("Gym", text="Gym Name")
        self.payments_tree.heading("Amount", text="Amount")
        self.payments_tree.heading("Date", text="Date")
        self.payments_tree.heading("Status", text="Status")
        self.payments_tree.pack(expand=True, fill="both")

        view_button = ttk.Button(self.view_tab, text="Refresh", command=self.view_all_payments)
        view_button.pack(pady=5)

    def create_update_tab(self):
        # Select payment ID
        ttk.Label(self.update_tab, text="Select Payment:").grid(row=0, column=0, padx=5, pady=5)
        self.update_payment_id_entry = ttk.Entry(self.update_tab)
        self.update_payment_id_entry.grid(row=0, column=1, padx=5, pady=5)

        # Update fields
        ttk.Label(self.update_tab, text="New Amount:").grid(row=1, column=0, padx=5, pady=5)
        self.new_amount_entry = ttk.Entry(self.update_tab)
        self.new_amount_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.update_tab, text="New Date:").grid(row=2, column=0, padx=5, pady=5)
        self.new_payment_date_calendar = Calendar(
            self.update_tab,
            selectmode="day",
            date_pattern="yyyy-mm-dd",
            background="white",
            foreground="gray",
            headersbackground="black",
            normalbackground="white",
            weekendbackground="black"
        )
        self.new_payment_date_calendar.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.update_tab, text="New Status:").grid(row=3, column=0, padx=5, pady=5)
        self.new_status_dropdown = ttk.Combobox(self.update_tab, values=["Paid", "Pending"], state="readonly")
        self.new_status_dropdown.grid(row=3, column=1, padx=5, pady=5)
        self.new_status_dropdown.set("Paid")  # Default value

        # Buttons
        update_button = ttk.Button(self.update_tab, text="Update Payment", command=self.update_payment)
        update_button.grid(row=4, column=0, pady=10, sticky="e")

        delete_button = ttk.Button(self.update_tab, text="Delete Payment", command=self.delete_payment)
        delete_button.grid(row=4, column=1, pady=10, sticky="w")

    def add_payment(self):
        user_name = self.user_dropdown.get()
        amount = self.amount_entry.get()
        payment_date = self.payment_date_calendar.get_date()
        status = self.status_dropdown.get()

        try:
            # Use Prepared Statements to prevent code injection
            if not amount.isdigit():
                raise ValueError("Amount must be a numeric value.")

            user = MemberManagement.search_member(name=user_name)
            if not user:
                raise ValueError("Selected user not found.")

            PaymentManager.add_payment(user["member_id"], amount, payment_date, status)
            messagebox.showinfo("Success", "Payment added successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add payment: {e}")

    def view_all_payments(self):
        payments = PaymentManager.view_all_payments()
        for row in self.payments_tree.get_children():
            self.payments_tree.delete(row)
        for payment in payments:
            self.payments_tree.insert(
                "",
                "end",
                values=(
                    payment["payment_id"],
                    payment["member_id"],
                    payment["member_name"],
                    payment["gym_name"],
                    payment["amount"],
                    payment["date"],
                    payment["status"],
                ),
            )

    def update_payment(self):
        payment_id = self.update_payment_id_entry.get()
        new_amount = self.new_amount_entry.get()
        new_date = self.new_payment_date_calendar.get_date()
        new_status = self.new_status_dropdown.get()

        try:
            PaymentManager.update_payment(payment_id, new_amount, new_date, new_status)
            messagebox.showinfo("Success", "Payment updated successfully.")
            self.view_all_payments()  # Refresh view
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update payment: {e}")

    def delete_payment(self):
        payment_id = self.update_payment_id_entry.get()

        try:
            PaymentManager.delete_payment(payment_id)
            messagebox.showinfo("Success", "Payment deleted successfully.")
            self.view_all_payments()  # Refresh view
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete payment: {e}")

    def get_gym_user_names(self):
        """Retrieve all Gym User names from the MemberManagement system."""
        members = MemberManagement.view_all_members()
        return [member["name"] for member in members if member["user_type"] == "Gym User"]


if __name__ == "__main__":
    root = tk.Tk()
    app = PaymentManagementApp(root)
    root.mainloop()
'''


'''import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from core.payments import PaymentManager
from core.member_management import MemberManagement


class PaymentManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Payment Management")
        self.selected_payment_id = None
        self.create_widgets()

    def create_widgets(self):
        # Tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True, fill="both")

        self.add_tab = ttk.Frame(notebook)
        self.view_tab = ttk.Frame(notebook)
        self.update_tab = ttk.Frame(notebook)

        notebook.add(self.add_tab, text="Add Payment")
        notebook.add(self.view_tab, text="View Payments")
        notebook.add(self.update_tab, text="Update/Delete Payment")

        self.create_add_tab()
        self.create_view_tab()
        self.create_update_tab()

    def create_add_tab(self):
        ttk.Label(self.add_tab, text="Member ID:").grid(row=0, column=0, padx=5, pady=5)
        self.member_id_entry = ttk.Entry(self.add_tab)
        self.member_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.add_tab, text="Amount:").grid(row=1, column=0, padx=5, pady=5)
        self.amount_entry = ttk.Entry(self.add_tab)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.add_tab, text="Payment Date:").grid(row=2, column=0, padx=5, pady=5)
        self.payment_date_calendar = Calendar(self.add_tab, selectmode="day", date_pattern="yyyy-mm-dd")
        self.payment_date_calendar.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.add_tab, text="Payment Status:").grid(row=3, column=0, padx=5, pady=5)
        self.status_dropdown = ttk.Combobox(self.add_tab, values=["Paid", "Pending"])
        self.status_dropdown.grid(row=3, column=1, padx=5, pady=5)
        self.status_dropdown.set("Paid")  # Default value

        add_button = ttk.Button(self.add_tab, text="Add Payment", command=self.add_payment)
        add_button.grid(row=4, column=0, columnspan=2, pady=10)

    def create_view_tab(self):
        self.payments_tree = ttk.Treeview(
            self.view_tab,
            columns=("ID", "Member ID", "Name", "Gym", "Amount", "Date", "Status"),
            show="headings",
        )
        self.payments_tree.heading("ID", text="Payment ID")
        self.payments_tree.heading("Member ID", text="Member ID")
        self.payments_tree.heading("Name", text="Member Name")
        self.payments_tree.heading("Gym", text="Gym Name")
        self.payments_tree.heading("Amount", text="Amount")
        self.payments_tree.heading("Date", text="Date")
        self.payments_tree.heading("Status", text="Status")
        self.payments_tree.pack(expand=True, fill="both")

        view_button = ttk.Button(self.view_tab, text="Refresh", command=self.view_all_payments)
        view_button.pack(pady=5)

    def create_update_tab(self):
        # Select payment ID
        ttk.Label(self.update_tab, text="Select Payment:").grid(row=0, column=0, padx=5, pady=5)
        self.update_payment_id_entry = ttk.Entry(self.update_tab)
        self.update_payment_id_entry.grid(row=0, column=1, padx=5, pady=5)

        # Update fields
        ttk.Label(self.update_tab, text="New Amount:").grid(row=1, column=0, padx=5, pady=5)
        self.new_amount_entry = ttk.Entry(self.update_tab)
        self.new_amount_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.update_tab, text="New Date:").grid(row=2, column=0, padx=5, pady=5)
        self.new_payment_date_calendar = Calendar(self.update_tab, selectmode="day", date_pattern="yyyy-mm-dd")
        self.new_payment_date_calendar.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.update_tab, text="New Status:").grid(row=3, column=0, padx=5, pady=5)
        self.new_status_dropdown = ttk.Combobox(self.update_tab, values=["Paid", "Pending"])
        self.new_status_dropdown.grid(row=3, column=1, padx=5, pady=5)
        self.new_status_dropdown.set("Paid")  # Default value

        # Buttons
        update_button = ttk.Button(self.update_tab, text="Update Payment", command=self.update_payment)
        update_button.grid(row=4, column=0, pady=10, sticky="e")

        delete_button = ttk.Button(self.update_tab, text="Delete Payment", command=self.delete_payment)
        delete_button.grid(row=4, column=1, pady=10, sticky="w")

    def add_payment(self):
        member_id = self.member_id_entry.get()
        amount = self.amount_entry.get()
        payment_date = self.payment_date_calendar.get_date()
        status = self.status_dropdown.get()

        try:
            PaymentManager.add_payment(member_id, amount, payment_date, status)
            messagebox.showinfo("Success", "Payment added successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add payment: {e}")

    def view_all_payments(self):
        payments = PaymentManager.view_all_payments()
        for row in self.payments_tree.get_children():
            self.payments_tree.delete(row)
        for payment in payments:
            self.payments_tree.insert(
                "",
                "end",
                values=(
                    payment["payment_id"],
                    payment["member_id"],
                    payment["member_name"],
                    payment["gym_name"],
                    payment["amount"],
                    payment["date"],
                    payment["status"],
                ),
            )

    def update_payment(self):
        payment_id = self.update_payment_id_entry.get()
        new_amount = self.new_amount_entry.get()
        new_date = self.new_payment_date_calendar.get_date()
        new_status = self.new_status_dropdown.get()

        try:
            PaymentManager.update_payment(payment_id, new_amount, new_date, new_status)
            messagebox.showinfo("Success", "Payment updated successfully.")
            self.view_all_payments()  # Refresh view
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update payment: {e}")

    def delete_payment(self):
        payment_id = self.update_payment_id_entry.get()

        try:
            PaymentManager.delete_payment(payment_id)
            messagebox.showinfo("Success", "Payment deleted successfully.")
            self.view_all_payments()  # Refresh view
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete payment: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = PaymentManagementApp(root)
    root.mainloop()
'''