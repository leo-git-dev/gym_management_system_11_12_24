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
