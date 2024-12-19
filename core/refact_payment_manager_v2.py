# core/refact_payment.py

import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from core.payments import PaymentManager
from core.member_management import MemberManagement


class PaymentManagementFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.update_payment_id_entry = None
        self.selected_payment_id = None
        self.create_widgets()

    def create_widgets(self):
        """Creates the tabs for Payment Management."""
        # Configure grid layout to make tabs expandable
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=0, sticky="nsew")

        self.add_tab = ttk.Frame(self.notebook)
        self.view_tab = ttk.Frame(self.notebook)
        self.update_tab = ttk.Frame(self.notebook)
        self.search_tab = ttk.Frame(self.notebook)  # Adding the Search tab

        self.notebook.add(self.add_tab, text="Add Payment")
        self.notebook.add(self.view_tab, text="View Payments")
        self.notebook.add(self.update_tab, text="Update/Delete Payment")
        self.notebook.add(self.search_tab, text="Search Payments")  # Adding the Search tab

        self.create_add_tab()
        self.create_view_tab()
        self.create_update_tab()
        self.create_search_tab()  # Creating the Search tab

    def create_add_tab(self):
        """Creates the Add Payment interface."""
        # Configure grid layout
        self.add_tab.columnconfigure(1, weight=1)
        for i in range(9):  # Updated to accommodate new fields
            self.add_tab.rowconfigure(i, weight=1)

        # Select User
        ttk.Label(self.add_tab, text="Select User (Gym Users only):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.user_dropdown = ttk.Combobox(
            self.add_tab,
            values=self.get_gym_user_names(),
            state="readonly"
        )
        self.user_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.user_dropdown.bind("<<ComboboxSelected>>", self.display_user_details)

        # User details table
        self.details_frame = ttk.Frame(self.add_tab)
        self.details_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Configure details_frame grid
        self.details_frame.columnconfigure(1, weight=1)

        # Amount
        ttk.Label(self.add_tab, text="Amount:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.amount_entry = ttk.Entry(self.add_tab)
        self.amount_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Payment Date
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

        # Payment Status
        ttk.Label(self.add_tab, text="Payment Status:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.status_dropdown = ttk.Combobox(
            self.add_tab,
            values=["Paid", "Pending"],
            state="readonly"
        )
        self.status_dropdown.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
        self.status_dropdown.set("Paid")  # Default value

        # Payment Type
        ttk.Label(self.add_tab, text="Payment Type:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.payment_type_dropdown = ttk.Combobox(
            self.add_tab,
            values=["Monthly", "Quarterly", "Annual"],
            state="readonly"
        )
        self.payment_type_dropdown.grid(row=5, column=1, padx=5, pady=5, sticky="ew")
        self.payment_type_dropdown.set("Select Payment Type")

        # Payment Method
        ttk.Label(self.add_tab, text="Payment Method:").grid(row=6, column=0, padx=5, pady=5, sticky="e")
        self.payment_method_dropdown = ttk.Combobox(
            self.add_tab,
            values=["Credit Card", "Direct Debit"],
            state="readonly"
        )
        self.payment_method_dropdown.grid(row=6, column=1, padx=5, pady=5, sticky="ew")
        self.payment_method_dropdown.set("Select Payment Method")

        # Discount Applied
        ttk.Label(self.add_tab, text="Apply Discount:").grid(row=7, column=0, padx=5, pady=5, sticky="e")
        self.discount_dropdown = ttk.Combobox(
            self.add_tab,
            values=["Yes", "No"],
            state="readonly"
        )
        self.discount_dropdown.grid(row=7, column=1, padx=5, pady=5, sticky="ew")
        self.discount_dropdown.set("No")  # Default value

        # Add Payment Button
        add_button = ttk.Button(self.add_tab, text="Add Payment", command=self.add_payment)
        add_button.grid(row=8, column=0, columnspan=2, pady=10)

    def display_user_details(self, event=None):
        """Displays selected gym user's details."""
        # Clear existing details
        for widget in self.details_frame.winfo_children():
            widget.destroy()

        user_name = self.user_dropdown.get()
        user = MemberManagement.search_member(name=user_name)

        if not user:
            ttk.Label(self.details_frame, text="No details found for the selected user.").grid(row=0, column=0, sticky="w")
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
            "Payment Type": user.get("payment_type", "N/A"),
            "Loyalty Points": user.get("loyalty_points", 0),
        }

        # Display filtered details in a table format
        headers = ["Field", "Value"]
        for col, header in enumerate(headers):
            ttk.Label(self.details_frame, text=header, font=("Helvetica", 10, "bold")).grid(row=0, column=col, padx=5, pady=5, sticky="w")

        for row, (field, value) in enumerate(filtered_details.items(), start=1):
            ttk.Label(self.details_frame, text=field).grid(row=row, column=0, padx=5, pady=5, sticky="w")
            ttk.Label(self.details_frame, text=value).grid(row=row, column=1, padx=5, pady=5, sticky="w")

    def add_payment(self):
        """Adds a payment for the selected user."""
        user_name = self.user_dropdown.get()
        amount = self.amount_entry.get()
        payment_date = self.payment_date_calendar.get_date()
        status = self.status_dropdown.get()
        payment_type = self.payment_type_dropdown.get()
        payment_method = self.payment_method_dropdown.get()
        discount_applied = self.discount_dropdown.get()

        try:
            # Validation
            if not user_name or user_name == "Select User":
                raise ValueError("Please select a valid user.")
            if not self.is_valid_amount(amount):
                raise ValueError("Amount must be a positive numeric value.")
            if payment_type not in ["Monthly", "Quarterly", "Annual"]:
                raise ValueError("Please select a valid payment type.")
            if payment_method not in ["Credit Card", "Direct Debit"]:
                raise ValueError("Please select a valid payment method.")
            if discount_applied not in ["Yes", "No"]:
                raise ValueError("Please select whether to apply a discount.")

            user = MemberManagement.search_member(name=user_name)
            if not user:
                raise ValueError("Selected user not found.")

            # Add payment
            PaymentManager.add_payment(
                member_id=user["member_id"],
                amount=float(amount),
                date=payment_date,
                status=status,
                payment_type=payment_type,
                payment_method=payment_method,
                discount_applied=discount_applied
            )
            messagebox.showinfo("Success", "Payment added successfully.")
            self.view_all_payments()  # Refresh payments view
            self.user_dropdown.set("")  # Reset user selection
            self.amount_entry.delete(0, tk.END)
            self.payment_type_dropdown.set("Select Payment Type")
            self.payment_method_dropdown.set("Select Payment Method")
            self.discount_dropdown.set("No")

        except ValueError as ve:
            messagebox.showwarning("Validation Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add payment: {e}")

    def is_valid_amount(self, amount):
        """Validates if the amount is a positive number."""
        try:
            amt = float(amount)
            return amt > 0
        except ValueError:
            return False

    def create_view_tab(self):
        """Creates the View Payments interface."""
        # Configure grid layout
        self.view_tab.columnconfigure(0, weight=1)
        self.view_tab.rowconfigure(0, weight=1)

        # Payments Treeview
        self.payments_tree = ttk.Treeview(
            self.view_tab,
            columns=("ID", "Member ID", "Name", "Gym", "Amount", "Date", "Status", "Payment Type", "Payment Method", "Discount Applied", "Note"),
            show="headings",
        )
        # Define headings
        headings = ["Payment ID", "Member ID", "Member Name", "Gym Name", "Amount", "Date", "Status", "Payment Type", "Payment Method", "Discount Applied", "Note"]
        for col, heading in enumerate(headings, start=1):
            self.payments_tree.heading(f"#{col}", text=heading)
            # Configure column widths and anchors
            if heading in ["Payment ID", "Member ID", "Payment Method", "Discount Applied"]:
                self.payments_tree.column(f"#{col}", width=120, anchor="center")
            elif heading == "Amount":
                self.payments_tree.column(f"#{col}", width=100, anchor="e")
            elif heading == "Date":
                self.payments_tree.column(f"#{col}", width=100, anchor="center")
            elif heading == "Status":
                self.payments_tree.column(f"#{col}", width=100, anchor="center")
            elif heading == "Payment Type":
                self.payments_tree.column(f"#{col}", width=120, anchor="center")
            elif heading == "Note":
                self.payments_tree.column(f"#{col}", width=200, anchor="w")
            else:
                self.payments_tree.column(f"#{col}", width=150, anchor="w")

        self.payments_tree.grid(row=0, column=0, sticky="nsew")

        # Scrollbars for Treeview
        scrollbar_vertical = ttk.Scrollbar(self.view_tab, orient=tk.VERTICAL, command=self.payments_tree.yview)
        scrollbar_horizontal = ttk.Scrollbar(self.view_tab, orient=tk.HORIZONTAL, command=self.payments_tree.xview)
        self.payments_tree.configure(yscroll=scrollbar_vertical.set, xscroll=scrollbar_horizontal.set)
        scrollbar_vertical.grid(row=0, column=1, sticky='ns')
        scrollbar_horizontal.grid(row=1, column=0, sticky='ew')

        # Refresh Button
        view_button = ttk.Button(self.view_tab, text="Refresh", command=self.view_all_payments)
        view_button.grid(row=2, column=0, pady=5, sticky="e")

        # Make the Treeview expandable
        self.view_tab.rowconfigure(0, weight=1)
        self.view_tab.columnconfigure(0, weight=1)

    def view_all_payments(self):
        """Displays all payments in the Treeview."""
        try:
            payments = PaymentManager.view_all_payments()
            # Clear existing entries
            for row in self.payments_tree.get_children():
                self.payments_tree.delete(row)
            # Insert new entries
            for payment in payments:
                self.payments_tree.insert(
                    "",
                    "end",
                    values=(
                        payment.get("payment_id", "N/A"),
                        payment.get("member_id", "N/A"),
                        payment.get("member_name", "N/A"),
                        payment.get("gym_name", "N/A"),
                        f"${float(payment.get('amount', 0)):.2f}",
                        payment.get("date", "N/A"),
                        payment.get("status", "N/A"),
                        payment.get("payment_type", "N/A"),
                        payment.get("payment_method", "N/A"),
                        payment.get("discount_applied", "No"),
                        payment.get("note", ""),
                    ),
                )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load payments: {e}")

    def create_update_tab(self):
        """Creates the Update/Delete Payment interface."""
        # Configure grid layout
        self.update_tab.columnconfigure(0, weight=1)
        self.update_tab.rowconfigure(0, weight=1)
        self.update_tab.rowconfigure(1, weight=1)

        # Payment Selection Frame
        selection_frame = ttk.Frame(self.update_tab)
        selection_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Configure selection_frame grid
        selection_frame.columnconfigure(0, weight=1)
        selection_frame.rowconfigure(1, weight=1)

        # Payment Selection Label
        ttk.Label(selection_frame, text="Select Payment to Update/Delete:").grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Payments Treeview within Update/Delete Tab
        self.update_payments_tree = ttk.Treeview(
            selection_frame,
            columns=("ID", "Member ID", "Name", "Gym", "Amount", "Date", "Status", "Payment Type", "Payment Method", "Discount Applied", "Note"),
            show="headings",
            height=10
        )
        # Define headings
        headings = ["Payment ID", "Member ID", "Member Name", "Gym Name", "Amount", "Date", "Status", "Payment Type", "Payment Method", "Discount Applied", "Note"]
        for col, heading in enumerate(headings, start=1):
            self.update_payments_tree.heading(f"#{col}", text=heading)
            # Configure column widths and anchors
            if heading in ["Payment ID", "Member ID", "Payment Method", "Discount Applied"]:
                self.update_payments_tree.column(f"#{col}", width=120, anchor="center")
            elif heading == "Amount":
                self.update_payments_tree.column(f"#{col}", width=100, anchor="e")
            elif heading == "Date":
                self.update_payments_tree.column(f"#{col}", width=100, anchor="center")
            elif heading == "Status":
                self.update_payments_tree.column(f"#{col}", width=100, anchor="center")
            elif heading == "Payment Type":
                self.update_payments_tree.column(f"#{col}", width=120, anchor="center")
            elif heading == "Note":
                self.update_payments_tree.column(f"#{col}", width=200, anchor="w")
            else:
                self.update_payments_tree.column(f"#{col}", width=150, anchor="w")

        self.update_payments_tree.grid(row=1, column=0, columnspan=3, pady=5, sticky="nsew")

        # Scrollbars for Update/Delete Treeview
        scrollbar_update_vertical = ttk.Scrollbar(selection_frame, orient=tk.VERTICAL, command=self.update_payments_tree.yview)
        scrollbar_update_horizontal = ttk.Scrollbar(selection_frame, orient=tk.HORIZONTAL, command=self.update_payments_tree.xview)
        self.update_payments_tree.configure(yscroll=scrollbar_update_vertical.set, xscroll=scrollbar_update_horizontal.set)
        scrollbar_update_vertical.grid(row=1, column=3, sticky='ns')
        scrollbar_update_horizontal.grid(row=2, column=0, columnspan=3, sticky='ew')

        # Bind selection
        self.update_payments_tree.bind("<<TreeviewSelect>>", self.on_payment_select)

        # Refresh Button
        refresh_update_button = ttk.Button(selection_frame, text="Refresh Payments", command=self.refresh_update_payments)
        refresh_update_button.grid(row=3, column=0, padx=5, pady=5, sticky="w")

        # Update Fields Frame
        fields_frame = ttk.Frame(self.update_tab)
        fields_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Configure fields_frame grid
        for i in range(9):  # Updated to accommodate new fields
            fields_frame.rowconfigure(i, weight=1)
        fields_frame.columnconfigure(1, weight=1)

        # Payment ID (Read-only)
        ttk.Label(fields_frame, text="Payment ID:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.update_payment_id_entry = ttk.Entry(fields_frame, state="readonly")
        self.update_payment_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # New Amount
        ttk.Label(fields_frame, text="New Amount:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.new_amount_entry = ttk.Entry(fields_frame)
        self.new_amount_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # New Date
        ttk.Label(fields_frame, text="New Date:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.new_payment_date_calendar = Calendar(
            fields_frame,
            selectmode="day",
            date_pattern="yyyy-mm-dd",
            background="white",
            foreground="gray",
            headersbackground="black",
        )
        self.new_payment_date_calendar.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # New Status
        ttk.Label(fields_frame, text="New Status:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.new_status_dropdown = ttk.Combobox(
            fields_frame,
            values=["Paid", "Pending"],
            state="readonly"
        )
        self.new_status_dropdown.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        self.new_status_dropdown.set("Paid")  # Default value

        # New Payment Type
        ttk.Label(fields_frame, text="New Payment Type:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.new_payment_type_dropdown = ttk.Combobox(
            fields_frame,
            values=["Monthly", "Quarterly", "Annual"],
            state="readonly"
        )
        self.new_payment_type_dropdown.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
        self.new_payment_type_dropdown.set("Select Payment Type")

        # New Payment Method
        ttk.Label(fields_frame, text="New Payment Method:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.new_payment_method_dropdown = ttk.Combobox(
            fields_frame,
            values=["Credit Card", "Direct Debit"],
            state="readonly"
        )
        self.new_payment_method_dropdown.grid(row=5, column=1, padx=5, pady=5, sticky="ew")
        self.new_payment_method_dropdown.set("Select Payment Method")

        # New Discount Applied
        ttk.Label(fields_frame, text="Apply Discount:").grid(row=6, column=0, padx=5, pady=5, sticky="e")
        self.new_discount_dropdown = ttk.Combobox(
            fields_frame,
            values=["Yes", "No"],
            state="readonly"
        )
        self.new_discount_dropdown.grid(row=6, column=1, padx=5, pady=5, sticky="ew")
        self.new_discount_dropdown.set("No")  # Default value

        # Note
        ttk.Label(fields_frame, text="Note:").grid(row=7, column=0, padx=5, pady=5, sticky="e")
        self.note_text = tk.Text(fields_frame, height=3, width=40, state='disabled')
        self.note_text.grid(row=7, column=1, padx=5, pady=5, sticky="ew")

        # Update and Delete Buttons
        buttons_frame = ttk.Frame(fields_frame)
        buttons_frame.grid(row=8, column=0, columnspan=2, pady=10)

        update_button = ttk.Button(buttons_frame, text="Update Payment", command=self.update_payment)
        update_button.grid(row=0, column=0, padx=5)

        delete_button = ttk.Button(buttons_frame, text="Delete Payment", command=self.delete_payment)
        delete_button.grid(row=0, column=1, padx=5)

        # Populate the Update/Delete Treeview
        self.refresh_update_payments()

    def on_payment_select(self, event):
        """Handles the selection of a payment from the Update/Delete Treeview."""
        selected_item = self.update_payments_tree.focus()
        if not selected_item:
            return
        values = self.update_payments_tree.item(selected_item, 'values')
        if not values:
            return

        # Populate the fields with selected payment details
        self.update_payment_id_entry.config(state='normal')
        self.update_payment_id_entry.delete(0, tk.END)
        self.update_payment_id_entry.insert(0, values[0])  # Payment ID
        self.update_payment_id_entry.config(state='readonly')

        self.new_amount_entry.delete(0, tk.END)
        self.new_amount_entry.insert(0, values[4].replace('$', ''))  # Amount

        # Set date in calendar
        try:
            self.new_payment_date_calendar.set_date(values[5])
        except:
            pass  # Handle invalid date formats gracefully

        self.new_status_dropdown.set(values[6])  # Status
        self.new_payment_type_dropdown.set(values[7])  # Payment Type
        self.new_payment_method_dropdown.set(values[8])  # Payment Method
        self.new_discount_dropdown.set(values[9])  # Discount Applied

        # Set Note
        note = values[10]
        self.note_text.config(state='normal')
        self.note_text.delete('1.0', tk.END)
        self.note_text.insert(tk.END, note)
        self.note_text.config(state='disabled')

    def refresh_update_payments(self):
        from core.member_management import MemberManagement
        """Refreshes the payments displayed in the Update/Delete Treeview."""
        try:
            payments = PaymentManager.view_all_payments()
            # Clear existing entries
            for row in self.update_payments_tree.get_children():
                self.update_payments_tree.delete(row)
            # Insert new entries
            for payment in payments:
                self.update_payments_tree.insert(
                    "",
                    "end",
                    values=(
                        payment.get("payment_id", "N/A"),
                        payment.get("member_id", "N/A"),
                        payment.get("member_name", "N/A"),
                        payment.get("gym_name", "N/A"),
                        f"${float(payment.get('amount', 0)):.2f}",
                        payment.get("date", "N/A"),
                        payment.get("status", "N/A"),
                        payment.get("payment_type", "N/A"),
                        payment.get("payment_method", "N/A"),
                        payment.get("discount_applied", "No"),
                        payment.get("note", ""),
                    ),
                )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load payments: {e}")

    def update_payment(self):
        from core.member_management import MemberManagement
        """Updates a payment's details."""
        payment_id = self.update_payment_id_entry.get().strip()
        new_amount = self.new_amount_entry.get().strip()
        new_date = self.new_payment_date_calendar.get_date()
        new_status = self.new_status_dropdown.get()
        new_payment_type = self.new_payment_type_dropdown.get()
        new_payment_method = self.new_payment_method_dropdown.get()
        new_discount_applied = self.new_discount_dropdown.get()
        note = self.note_text.get("1.0", tk.END).strip()

        try:
            # Validation
            if not payment_id:
                raise ValueError("Payment ID is required.")
            if new_amount and not self.is_valid_amount(new_amount):
                raise ValueError("Amount must be a positive numeric value.")
            if new_payment_type and new_payment_type not in ["Monthly", "Quarterly", "Annual"]:
                raise ValueError("Please select a valid payment type.")
            if new_payment_method and new_payment_method not in ["Credit Card", "Direct Debit"]:
                raise ValueError("Please select a valid payment method.")
            if new_discount_applied and new_discount_applied not in ["Yes", "No"]:
                raise ValueError("Please select a valid discount option.")

            # Update payment
            PaymentManager.update_payment(
                payment_id=payment_id,
                amount=float(new_amount) if new_amount else None,
                date=new_date if new_date else None,
                status=new_status if new_status else None,
                payment_type=new_payment_type if new_payment_type else None,
                payment_method=new_payment_method if new_payment_method else None,
                discount_applied=new_discount_applied if new_discount_applied else None
            )
            messagebox.showinfo("Success", "Payment updated successfully.")
            self.refresh_update_payments()
            self.view_all_payments()  # Refresh view

        except ValueError as ve:
            messagebox.showwarning("Validation Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update payment: {e}")

    def delete_payment(self):
        from core.member_management import MemberManagement
        """Deletes a payment based on Payment ID."""
        payment_id = self.update_payment_id_entry.get().strip()

        try:
            # Validation
            if not payment_id:
                raise ValueError("Payment ID is required.")

            # Confirm deletion
            confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete Payment ID {payment_id}?")
            if not confirm:
                return

            # Delete payment
            PaymentManager.delete_payment(payment_id=payment_id)
            messagebox.showinfo("Success", "Payment deleted successfully.")
            self.refresh_update_payments()
            self.view_all_payments()  # Refresh view

            # Clear update fields
            self.update_payment_id_entry.config(state='normal')
            self.update_payment_id_entry.delete(0, tk.END)
            self.update_payment_id_entry.config(state='readonly')
            self.new_amount_entry.delete(0, tk.END)
            self.new_payment_date_calendar.set_date('')
            self.new_status_dropdown.set("Paid")
            self.new_payment_type_dropdown.set("Select Payment Type")
            self.new_payment_method_dropdown.set("Select Payment Method")
            self.new_discount_dropdown.set("No")
            self.note_text.config(state='normal')
            self.note_text.delete("1.0", tk.END)
            self.note_text.config(state='disabled')

        except ValueError as ve:
            messagebox.showwarning("Validation Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete payment: {e}")

    def create_search_tab(self):
        from core.member_management import MemberManagement
        """Creates the Search Payments interface."""
        # Configure grid layout
        self.search_tab.columnconfigure(0, weight=1)
        self.search_tab.rowconfigure(4, weight=1)

        frame = ttk.Frame(self.search_tab)
        frame.grid(row=0, column=0, sticky="nsew")

        # Configure frame grid
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(4, weight=1)

        # Search by Gym Frame
        gym_search_frame = ttk.LabelFrame(frame, text="Search by Gym")
        gym_search_frame.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="ew")
        gym_search_frame.columnconfigure(1, weight=1)

        # Gym Selection
        ttk.Label(gym_search_frame, text="Select Gym:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.search_gym_dropdown = ttk.Combobox(
            gym_search_frame,
            values=self.get_all_gym_names(),
            state="readonly"
        )
        self.search_gym_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.search_gym_dropdown.set("Select Gym")

        # Search Gym Button
        search_gym_button = ttk.Button(gym_search_frame, text="Search", command=self.search_by_gym)
        search_gym_button.grid(row=0, column=2, padx=5, pady=5)

        # Search by User Name Frame
        user_search_frame = ttk.LabelFrame(frame, text="Search by User Name")
        user_search_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="ew")
        user_search_frame.columnconfigure(1, weight=1)

        # User Name Entry with Autocomplete
        ttk.Label(user_search_frame, text="User Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.search_user_name_var = tk.StringVar()
        self.search_user_name_entry = ttk.Combobox(
            user_search_frame,
            textvariable=self.search_user_name_var,
            values=self.get_gym_user_names(),
            state="readonly"
        )
        self.search_user_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.search_user_name_entry.set("Select User Name")

        # Search User Button
        search_user_button = ttk.Button(user_search_frame, text="Search", command=self.search_by_user_name)
        search_user_button.grid(row=0, column=2, padx=5, pady=5)

        # Refresh Button
        refresh_button = ttk.Button(frame, text="Refresh", command=self.refresh_search_results)
        refresh_button.grid(row=2, column=3, padx=10, pady=5, sticky="e")

        # Results Treeview
        self.search_results_tree = ttk.Treeview(
            frame,
            columns=("ID", "Member ID", "Name", "Gym", "Amount", "Date", "Status", "Payment Type", "Payment Method", "Discount Applied", "Note"),
            show="headings",
        )
        # Define headings
        headings = ["Payment ID", "Member ID", "Member Name", "Gym Name", "Amount", "Date", "Status", "Payment Type", "Payment Method", "Discount Applied", "Note"]
        for col, heading in enumerate(headings, start=1):
            self.search_results_tree.heading(f"#{col}", text=heading)
            # Configure column widths and anchors
            if heading in ["Payment ID", "Member ID", "Payment Method", "Discount Applied"]:
                self.search_results_tree.column(f"#{col}", width=120, anchor="center")
            elif heading == "Amount":
                self.search_results_tree.column(f"#{col}", width=100, anchor="e")
            elif heading == "Date":
                self.search_results_tree.column(f"#{col}", width=100, anchor="center")
            elif heading == "Status":
                self.search_results_tree.column(f"#{col}", width=100, anchor="center")
            elif heading == "Payment Type":
                self.search_results_tree.column(f"#{col}", width=120, anchor="center")
            elif heading == "Note":
                self.search_results_tree.column(f"#{col}", width=200, anchor="w")
            else:
                self.search_results_tree.column(f"#{col}", width=150, anchor="w")

        self.search_results_tree.grid(row=3, column=0, columnspan=4, pady=10, sticky="nsew")

        # Scrollbars for Search Results Treeview
        scrollbar_search_vertical = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.search_results_tree.yview)
        scrollbar_search_horizontal = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=self.search_results_tree.xview)
        self.search_results_tree.configure(yscroll=scrollbar_search_vertical.set, xscroll=scrollbar_search_horizontal.set)
        scrollbar_search_vertical.grid(row=3, column=4, sticky='ns')
        scrollbar_search_horizontal.grid(row=4, column=0, columnspan=4, sticky='ew')

    def search_by_gym(self):
        from core.member_management import MemberManagement
        """Searches for payments based on selected gym."""
        gym_name = self.search_gym_dropdown.get()

        if gym_name == "Select Gym":
            messagebox.showwarning("Selection Error", "Please select a gym to search.")
            return

        try:
            # Retrieve payments for the selected gym
            payments = PaymentManager.view_all_payments()
            filtered_payments = [p for p in payments if p.get("gym_name", "").lower() == gym_name.lower()]

            # Update the search results tree
            for row in self.search_results_tree.get_children():
                self.search_results_tree.delete(row)

            for payment in filtered_payments:
                self.search_results_tree.insert(
                    "",
                    "end",
                    values=(
                        payment.get("payment_id", "N/A"),
                        payment.get("member_id", "N/A"),
                        payment.get("member_name", "N/A"),
                        payment.get("gym_name", "N/A"),
                        f"${float(payment.get('amount', 0)):.2f}",
                        payment.get("date", "N/A"),
                        payment.get("status", "N/A"),
                        payment.get("payment_type", "N/A"),
                        payment.get("payment_method", "N/A"),
                        payment.get("discount_applied", "No"),
                        payment.get("note", ""),
                    ),
                )

            if not filtered_payments:
                messagebox.showinfo("No Results", f"No payments found for Gym: {gym_name}.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to search payments by gym: {e}")

    def search_by_user_name(self):
        from core.member_management import MemberManagement
        """Searches for payments based on selected user name."""
        user_name = self.search_user_name_entry.get()

        if user_name == "Select User Name":
            messagebox.showwarning("Selection Error", "Please select a user name to search.")
            return

        try:
            # Retrieve payments for the selected user
            payments = PaymentManager.view_all_payments()
            filtered_payments = [p for p in payments if p.get("member_name", "").lower() == user_name.lower()]

            # Update the search results tree
            for row in self.search_results_tree.get_children():
                self.search_results_tree.delete(row)

            for payment in filtered_payments:
                self.search_results_tree.insert(
                    "",
                    "end",
                    values=(
                        payment.get("payment_id", "N/A"),
                        payment.get("member_id", "N/A"),
                        payment.get("member_name", "N/A"),
                        payment.get("gym_name", "N/A"),
                        f"${float(payment.get('amount', 0)):.2f}",
                        payment.get("date", "N/A"),
                        payment.get("status", "N/A"),
                        payment.get("payment_type", "N/A"),
                        payment.get("payment_method", "N/A"),
                        payment.get("discount_applied", "No"),
                        payment.get("note", ""),
                    ),
                )

            if not filtered_payments:
                messagebox.showinfo("No Results", f"No payments found for User: {user_name}.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to search payments by user name: {e}")

    def refresh_search_results(self):
        """Refreshes the search results by clearing inputs and results."""
        # Reset Gym Search
        self.search_gym_dropdown.set("Select Gym")

        # Reset User Name Search
        self.search_user_name_entry.set("Select User Name")

        # Clear Search Results
        for row in self.search_results_tree.get_children():
            self.search_results_tree.delete(row)

    def get_gym_user_names(self):
        from core.member_management import MemberManagement
        """Retrieve all Gym User names from the MemberManagement system."""
        try:
            members = MemberManagement.view_all_members()
            return [member["name"] for member in members if member["user_type"] == "Gym User"]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch gym user names: {e}")
            return []

    def get_all_gym_names(self):
        """Retrieve all Gym names from the MemberManagement system."""
        try:
            members = MemberManagement.view_all_members()
            gym_names = set(member["gym_name"] for member in members if member.get("gym_name"))
            return sorted(list(gym_names))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch gym names: {e}")
            return []


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Payment Management System")
    root.geometry("1400x900")  # Increased size to accommodate more columns
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    app = PaymentManagementFrame(root)
    app.grid(row=0, column=0, sticky='nsew')
    root.mainloop()




'''# core/refact_payment.py

import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from core.payments import PaymentManager
from core.member_management import MemberManagement


class PaymentManagementFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.selected_payment_id = None
        self.create_widgets()

    def create_widgets(self):
        """Creates the tabs for Payment Management."""
        # Configure grid layout to make tabs expandable
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=0, sticky="nsew")

        self.add_tab = ttk.Frame(self.notebook)
        self.view_tab = ttk.Frame(self.notebook)
        self.update_tab = ttk.Frame(self.notebook)
        self.search_tab = ttk.Frame(self.notebook)  # Adding the Search tab

        self.notebook.add(self.add_tab, text="Add Payment")
        self.notebook.add(self.view_tab, text="View Payments")
        self.notebook.add(self.update_tab, text="Update/Delete Payment")
        self.notebook.add(self.search_tab, text="Search Payments")  # Adding the Search tab

        self.create_add_tab()
        self.create_view_tab()
        self.create_update_tab()
        self.create_search_tab()  # Creating the Search tab

    def create_add_tab(self):
        """Creates the Add Payment interface."""
        # Configure grid layout
        self.add_tab.columnconfigure(1, weight=1)
        for i in range(7):
            self.add_tab.rowconfigure(i, weight=1)

        # Select User
        ttk.Label(self.add_tab, text="Select User (Gym Users only):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.user_dropdown = ttk.Combobox(
            self.add_tab,
            values=self.get_gym_user_names(),
            state="readonly"
        )
        self.user_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.user_dropdown.bind("<<ComboboxSelected>>", self.display_user_details)

        # User details table
        self.details_frame = ttk.Frame(self.add_tab)
        self.details_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Configure details_frame grid
        self.details_frame.columnconfigure(1, weight=1)

        # Amount
        ttk.Label(self.add_tab, text="Amount:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.amount_entry = ttk.Entry(self.add_tab)
        self.amount_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Payment Date
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

        # Payment Status
        ttk.Label(self.add_tab, text="Payment Status:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.status_dropdown = ttk.Combobox(
            self.add_tab,
            values=["Paid", "Pending"],
            state="readonly"
        )
        self.status_dropdown.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
        self.status_dropdown.set("Paid")  # Default value

        # Payment Type
        ttk.Label(self.add_tab, text="Payment Type:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.payment_type_dropdown = ttk.Combobox(
            self.add_tab,
            values=["Monthly", "Quarterly", "Annual"],
            state="readonly"
        )
        self.payment_type_dropdown.grid(row=5, column=1, padx=5, pady=5, sticky="ew")
        self.payment_type_dropdown.set("Select Payment Type")

        # Add Payment Button
        add_button = ttk.Button(self.add_tab, text="Add Payment", command=self.add_payment)
        add_button.grid(row=6, column=0, columnspan=2, pady=10)

    def display_user_details(self, event=None):
        """Displays selected gym user's details."""
        # Clear existing details
        for widget in self.details_frame.winfo_children():
            widget.destroy()

        user_name = self.user_dropdown.get()
        user = MemberManagement.search_member(name=user_name)

        if not user:
            ttk.Label(self.details_frame, text="No details found for the selected user.").grid(row=0, column=0, sticky="w")
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
            "Payment Type": user.get("payment_type", "N/A"),
        }

        # Display filtered details in a table format
        headers = ["Field", "Value"]
        for col, header in enumerate(headers):
            ttk.Label(self.details_frame, text=header, font=("Helvetica", 10, "bold")).grid(row=0, column=col, padx=5, pady=5, sticky="w")

        for row, (field, value) in enumerate(filtered_details.items(), start=1):
            ttk.Label(self.details_frame, text=field).grid(row=row, column=0, padx=5, pady=5, sticky="w")
            ttk.Label(self.details_frame, text=value).grid(row=row, column=1, padx=5, pady=5, sticky="w")

    def add_payment(self):
        """Adds a payment for the selected user."""
        user_name = self.user_dropdown.get()
        amount = self.amount_entry.get()
        payment_date = self.payment_date_calendar.get_date()
        status = self.status_dropdown.get()
        payment_type = self.payment_type_dropdown.get()

        try:
            # Validation
            if not user_name or user_name == "Select User":
                raise ValueError("Please select a valid user.")
            if not self.is_valid_amount(amount):
                raise ValueError("Amount must be a positive numeric value.")
            if payment_type not in ["Monthly", "Quarterly", "Annual"]:
                raise ValueError("Please select a valid payment type.")

            user = MemberManagement.search_member(name=user_name)
            if not user:
                raise ValueError("Selected user not found.")

            # Add payment
            PaymentManager.add_payment(
                member_id=user["member_id"],
                amount=float(amount),
                date=payment_date,
                status=status,
                payment_type=payment_type
            )
            messagebox.showinfo("Success", "Payment added successfully.")
            self.view_all_payments()  # Refresh payments view
            self.user_dropdown.set("")  # Reset user selection
            self.amount_entry.delete(0, tk.END)
            self.payment_type_dropdown.set("Select Payment Type")

        except ValueError as ve:
            messagebox.showwarning("Validation Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add payment: {e}")

    def is_valid_amount(self, amount):
        """Validates if the amount is a positive number."""
        try:
            amt = float(amount)
            return amt > 0
        except ValueError:
            return False

    def create_view_tab(self):
        """Creates the View Payments interface."""
        # Configure grid layout
        self.view_tab.columnconfigure(0, weight=1)
        self.view_tab.rowconfigure(0, weight=1)

        # Payments Treeview
        self.payments_tree = ttk.Treeview(
            self.view_tab,
            columns=("ID", "Member ID", "Name", "Gym", "Amount", "Date", "Status", "Payment Type"),
            show="headings",
        )
        self.payments_tree.heading("ID", text="Payment ID")
        self.payments_tree.heading("Member ID", text="Member ID")
        self.payments_tree.heading("Name", text="Member Name")
        self.payments_tree.heading("Gym", text="Gym Name")
        self.payments_tree.heading("Amount", text="Amount")
        self.payments_tree.heading("Date", text="Date")
        self.payments_tree.heading("Status", text="Status")
        self.payments_tree.heading("Payment Type", text="Payment Type")

        # Configure columns for better display
        self.payments_tree.column("ID", width=100, anchor="center")
        self.payments_tree.column("Member ID", width=100, anchor="center")
        self.payments_tree.column("Name", width=150, anchor="w")
        self.payments_tree.column("Gym", width=150, anchor="w")
        self.payments_tree.column("Amount", width=80, anchor="e")
        self.payments_tree.column("Date", width=100, anchor="center")
        self.payments_tree.column("Status", width=80, anchor="center")
        self.payments_tree.column("Payment Type", width=100, anchor="center")

        self.payments_tree.grid(row=0, column=0, sticky="nsew")

        # Scrollbars for Treeview
        scrollbar_vertical = ttk.Scrollbar(self.view_tab, orient=tk.VERTICAL, command=self.payments_tree.yview)
        scrollbar_horizontal = ttk.Scrollbar(self.view_tab, orient=tk.HORIZONTAL, command=self.payments_tree.xview)
        self.payments_tree.configure(yscroll=scrollbar_vertical.set, xscroll=scrollbar_horizontal.set)
        scrollbar_vertical.grid(row=0, column=1, sticky='ns')
        scrollbar_horizontal.grid(row=1, column=0, sticky='ew')

        # Refresh Button
        view_button = ttk.Button(self.view_tab, text="Refresh", command=self.view_all_payments)
        view_button.grid(row=2, column=0, pady=5, sticky="e")

        # Make the Treeview expandable
        self.view_tab.rowconfigure(0, weight=1)
        self.view_tab.columnconfigure(0, weight=1)

    def view_all_payments(self):
        """Displays all payments in the Treeview."""
        try:
            payments = PaymentManager.view_all_payments()
            # Clear existing entries
            for row in self.payments_tree.get_children():
                self.payments_tree.delete(row)
            # Insert new entries
            for payment in payments:
                self.payments_tree.insert(
                    "",
                    "end",
                    values=(
                        payment.get("payment_id", "N/A"),
                        payment.get("member_id", "N/A"),
                        payment.get("member_name", "N/A"),
                        payment.get("gym_name", "N/A"),
                        f"${float(payment.get('amount', 0)):.2f}",
                        payment.get("date", "N/A"),
                        payment.get("status", "N/A"),
                        payment.get("payment_type", "N/A"),
                    ),
                )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load payments: {e}")

    def create_update_tab(self):
        """Creates the Update/Delete Payment interface."""
        # Configure grid layout
        self.update_tab.columnconfigure(0, weight=1)
        self.update_tab.rowconfigure(0, weight=1)
        self.update_tab.rowconfigure(1, weight=1)

        # Payment Selection Frame
        selection_frame = ttk.Frame(self.update_tab)
        selection_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Configure selection_frame grid
        selection_frame.columnconfigure(0, weight=1)
        selection_frame.rowconfigure(1, weight=1)

        # Payment Selection Label
        ttk.Label(selection_frame, text="Select Payment to Update/Delete:").grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Payments Treeview within Update/Delete Tab
        self.update_payments_tree = ttk.Treeview(
            selection_frame,
            columns=("ID", "Member ID", "Name", "Gym", "Amount", "Date", "Status", "Payment Type"),
            show="headings",
            height=10
        )
        self.update_payments_tree.heading("ID", text="Payment ID")
        self.update_payments_tree.heading("Member ID", text="Member ID")
        self.update_payments_tree.heading("Name", text="Member Name")
        self.update_payments_tree.heading("Gym", text="Gym Name")
        self.update_payments_tree.heading("Amount", text="Amount")
        self.update_payments_tree.heading("Date", text="Date")
        self.update_payments_tree.heading("Status", text="Status")
        self.update_payments_tree.heading("Payment Type", text="Payment Type")

        # Configure columns for better display
        self.update_payments_tree.column("ID", width=100, anchor="center")
        self.update_payments_tree.column("Member ID", width=100, anchor="center")
        self.update_payments_tree.column("Name", width=150, anchor="w")
        self.update_payments_tree.column("Gym", width=150, anchor="w")
        self.update_payments_tree.column("Amount", width=80, anchor="e")
        self.update_payments_tree.column("Date", width=100, anchor="center")
        self.update_payments_tree.column("Status", width=80, anchor="center")
        self.update_payments_tree.column("Payment Type", width=100, anchor="center")

        self.update_payments_tree.grid(row=1, column=0, columnspan=3, pady=5, sticky="nsew")

        # Scrollbars for Update/Delete Treeview
        scrollbar_update_vertical = ttk.Scrollbar(selection_frame, orient=tk.VERTICAL, command=self.update_payments_tree.yview)
        scrollbar_update_horizontal = ttk.Scrollbar(selection_frame, orient=tk.HORIZONTAL, command=self.update_payments_tree.xview)
        self.update_payments_tree.configure(yscroll=scrollbar_update_vertical.set, xscroll=scrollbar_update_horizontal.set)
        scrollbar_update_vertical.grid(row=1, column=3, sticky='ns')
        scrollbar_update_horizontal.grid(row=2, column=0, columnspan=3, sticky='ew')

        # Bind selection
        self.update_payments_tree.bind("<<TreeviewSelect>>", self.on_payment_select)

        # Refresh Button
        refresh_update_button = ttk.Button(selection_frame, text="Refresh Payments", command=self.refresh_update_payments)
        refresh_update_button.grid(row=3, column=0, padx=5, pady=5, sticky="w")

        # Update Fields Frame
        fields_frame = ttk.Frame(self.update_tab)
        fields_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Configure fields_frame grid
        for i in range(6):
            fields_frame.rowconfigure(i, weight=1)
        fields_frame.columnconfigure(1, weight=1)

        # Payment ID (Read-only)
        ttk.Label(fields_frame, text="Payment ID:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.update_payment_id_entry = ttk.Entry(fields_frame, state="readonly")
        self.update_payment_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # New Amount
        ttk.Label(fields_frame, text="New Amount:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.new_amount_entry = ttk.Entry(fields_frame)
        self.new_amount_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # New Date
        ttk.Label(fields_frame, text="New Date:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.new_payment_date_calendar = Calendar(
            fields_frame,
            selectmode="day",
            date_pattern="yyyy-mm-dd",
            background="white",
            foreground="gray",
            headersbackground="black",
        )
        self.new_payment_date_calendar.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # New Status
        ttk.Label(fields_frame, text="New Status:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.new_status_dropdown = ttk.Combobox(
            fields_frame,
            values=["Paid", "Pending"],
            state="readonly"
        )
        self.new_status_dropdown.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        self.new_status_dropdown.set("Paid")  # Default value

        # New Payment Type
        ttk.Label(fields_frame, text="New Payment Type:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.new_payment_type_dropdown = ttk.Combobox(
            fields_frame,
            values=["Monthly", "Quarterly", "Annual"],
            state="readonly"
        )
        self.new_payment_type_dropdown.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
        self.new_payment_type_dropdown.set("Select Payment Type")

        # Update and Delete Buttons
        buttons_frame = ttk.Frame(fields_frame)
        buttons_frame.grid(row=5, column=0, columnspan=2, pady=10)

        update_button = ttk.Button(buttons_frame, text="Update Payment", command=self.update_payment)
        update_button.grid(row=0, column=0, padx=5)

        delete_button = ttk.Button(buttons_frame, text="Delete Payment", command=self.delete_payment)
        delete_button.grid(row=0, column=1, padx=5)

        # Populate the Update/Delete Treeview
        self.refresh_update_payments()

    def on_payment_select(self, event):
        """Handles the selection of a payment from the Update/Delete Treeview."""
        selected_item = self.update_payments_tree.focus()
        if not selected_item:
            return
        values = self.update_payments_tree.item(selected_item, 'values')
        if not values:
            return

        # Populate the fields with selected payment details
        self.update_payment_id_entry.config(state='normal')
        self.update_payment_id_entry.delete(0, tk.END)
        self.update_payment_id_entry.insert(0, values[0])  # Payment ID
        self.update_payment_id_entry.config(state='readonly')

        self.new_amount_entry.delete(0, tk.END)
        self.new_amount_entry.insert(0, values[4].replace('$', ''))  # Amount

        # Set date in calendar
        try:
            self.new_payment_date_calendar.set_date(values[5])
        except:
            pass  # Handle invalid date formats gracefully

        self.new_status_dropdown.set(values[6])  # Status
        self.new_payment_type_dropdown.set(values[7])  # Payment Type

    def refresh_update_payments(self):
        """Refreshes the payments displayed in the Update/Delete Treeview."""
        try:
            payments = PaymentManager.view_all_payments()
            # Clear existing entries
            for row in self.update_payments_tree.get_children():
                self.update_payments_tree.delete(row)
            # Insert new entries
            for payment in payments:
                self.update_payments_tree.insert(
                    "",
                    "end",
                    values=(
                        payment.get("payment_id", "N/A"),
                        payment.get("member_id", "N/A"),
                        payment.get("member_name", "N/A"),
                        payment.get("gym_name", "N/A"),
                        f"${float(payment.get('amount', 0)):.2f}",
                        payment.get("date", "N/A"),
                        payment.get("status", "N/A"),
                        payment.get("payment_type", "N/A"),
                    ),
                )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load payments: {e}")

    def update_payment(self):
        """Updates a payment's details."""
        payment_id = self.update_payment_id_entry.get().strip()
        new_amount = self.new_amount_entry.get().strip()
        new_date = self.new_payment_date_calendar.get_date()
        new_status = self.new_status_dropdown.get()
        new_payment_type = self.new_payment_type_dropdown.get()

        try:
            # Validation
            if not payment_id:
                raise ValueError("Payment ID is required.")
            if new_amount and not self.is_valid_amount(new_amount):
                raise ValueError("Amount must be a positive numeric value.")
            if new_payment_type and new_payment_type not in ["Monthly", "Quarterly", "Annual"]:
                raise ValueError("Please select a valid payment type.")

            # Update payment
            PaymentManager.update_payment(
                payment_id=payment_id,
                amount=float(new_amount) if new_amount else None,
                date=new_date if new_date else None,
                status=new_status if new_status else None,
                payment_type=new_payment_type if new_payment_type else None
            )
            messagebox.showinfo("Success", "Payment updated successfully.")
            self.refresh_update_payments()
            self.view_all_payments()  # Refresh view

        except ValueError as ve:
            messagebox.showwarning("Validation Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update payment: {e}")

    def delete_payment(self):
        """Deletes a payment based on Payment ID."""
        payment_id = self.update_payment_id_entry.get().strip()

        try:
            # Validation
            if not payment_id:
                raise ValueError("Payment ID is required.")

            # Confirm deletion
            confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete Payment ID {payment_id}?")
            if not confirm:
                return

            # Delete payment
            PaymentManager.delete_payment(payment_id=payment_id)
            messagebox.showinfo("Success", "Payment deleted successfully.")
            self.refresh_update_payments()
            self.view_all_payments()  # Refresh view

        except ValueError as ve:
            messagebox.showwarning("Validation Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete payment: {e}")

    def create_search_tab(self):
        """Creates the Search Payments interface."""
        # Configure grid layout
        self.search_tab.columnconfigure(0, weight=1)
        self.search_tab.rowconfigure(4, weight=1)

        frame = ttk.Frame(self.search_tab)
        frame.grid(row=0, column=0, sticky="nsew")

        # Configure frame grid
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(4, weight=1)

        # Search by Gym Frame
        gym_search_frame = ttk.LabelFrame(frame, text="Search by Gym")
        gym_search_frame.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="ew")
        gym_search_frame.columnconfigure(1, weight=1)

        # Gym Selection
        ttk.Label(gym_search_frame, text="Select Gym:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.search_gym_dropdown = ttk.Combobox(
            gym_search_frame,
            values=self.get_all_gym_names(),
            state="readonly"
        )
        self.search_gym_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.search_gym_dropdown.set("Select Gym")

        # Search Gym Button
        search_gym_button = ttk.Button(gym_search_frame, text="Search", command=self.search_by_gym)
        search_gym_button.grid(row=0, column=2, padx=5, pady=5)

        # Search by User Name Frame
        user_search_frame = ttk.LabelFrame(frame, text="Search by User Name")
        user_search_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="ew")
        user_search_frame.columnconfigure(1, weight=1)

        # User Name Entry with Autocomplete
        ttk.Label(user_search_frame, text="User Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.search_user_name_var = tk.StringVar()
        self.search_user_name_entry = ttk.Combobox(
            user_search_frame,
            textvariable=self.search_user_name_var,
            values=self.get_gym_user_names(),
            state="readonly"
        )
        self.search_user_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.search_user_name_entry.set("Select User Name")

        # Search User Button
        search_user_button = ttk.Button(user_search_frame, text="Search", command=self.search_by_user_name)
        search_user_button.grid(row=0, column=2, padx=5, pady=5)

        # Refresh Button
        refresh_button = ttk.Button(frame, text="Refresh", command=self.refresh_search_results)
        refresh_button.grid(row=2, column=3, padx=10, pady=5, sticky="e")

        # Results Treeview
        self.search_results_tree = ttk.Treeview(
            frame,
            columns=("ID", "Member ID", "Name", "Gym", "Amount", "Date", "Status", "Payment Type"),
            show="headings",
        )
        self.search_results_tree.heading("ID", text="Payment ID")
        self.search_results_tree.heading("Member ID", text="Member ID")
        self.search_results_tree.heading("Name", text="Member Name")
        self.search_results_tree.heading("Gym", text="Gym Name")
        self.search_results_tree.heading("Amount", text="Amount")
        self.search_results_tree.heading("Date", text="Date")
        self.search_results_tree.heading("Status", text="Status")
        self.search_results_tree.heading("Payment Type", text="Payment Type")

        # Configure columns for better display
        self.search_results_tree.column("ID", width=100, anchor="center")
        self.search_results_tree.column("Member ID", width=100, anchor="center")
        self.search_results_tree.column("Name", width=150, anchor="w")
        self.search_results_tree.column("Gym", width=150, anchor="w")
        self.search_results_tree.column("Amount", width=80, anchor="e")
        self.search_results_tree.column("Date", width=100, anchor="center")
        self.search_results_tree.column("Status", width=80, anchor="center")
        self.search_results_tree.column("Payment Type", width=100, anchor="center")

        self.search_results_tree.grid(row=3, column=0, columnspan=4, pady=10, sticky="nsew")

        # Scrollbars for Search Results Treeview
        scrollbar_search_vertical = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.search_results_tree.yview)
        scrollbar_search_horizontal = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=self.search_results_tree.xview)
        self.search_results_tree.configure(yscroll=scrollbar_search_vertical.set, xscroll=scrollbar_search_horizontal.set)
        scrollbar_search_vertical.grid(row=3, column=4, sticky='ns')
        scrollbar_search_horizontal.grid(row=4, column=0, columnspan=4, sticky='ew')

    def search_by_gym(self):
        """Searches for payments based on selected gym."""
        gym_name = self.search_gym_dropdown.get()

        if gym_name == "Select Gym":
            messagebox.showwarning("Selection Error", "Please select a gym to search.")
            return

        try:
            # Retrieve payments for the selected gym
            payments = PaymentManager.view_all_payments()
            filtered_payments = [p for p in payments if p.get("gym_name", "").lower() == gym_name.lower()]

            # Update the search results tree
            for row in self.search_results_tree.get_children():
                self.search_results_tree.delete(row)

            for payment in filtered_payments:
                self.search_results_tree.insert(
                    "",
                    "end",
                    values=(
                        payment.get("payment_id", "N/A"),
                        payment.get("member_id", "N/A"),
                        payment.get("member_name", "N/A"),
                        payment.get("gym_name", "N/A"),
                        f"${float(payment.get('amount', 0)):.2f}",
                        payment.get("date", "N/A"),
                        payment.get("status", "N/A"),
                        payment.get("payment_type", "N/A"),
                    ),
                )

            if not filtered_payments:
                messagebox.showinfo("No Results", f"No payments found for Gym: {gym_name}.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to search payments by gym: {e}")

    def search_by_user_name(self):
        """Searches for payments based on selected user name."""
        user_name = self.search_user_name_entry.get()

        if user_name == "Select User Name":
            messagebox.showwarning("Selection Error", "Please select a user name to search.")
            return

        try:
            # Retrieve payments for the selected user
            payments = PaymentManager.view_all_payments()
            filtered_payments = [p for p in payments if p.get("member_name", "").lower() == user_name.lower()]

            # Update the search results tree
            for row in self.search_results_tree.get_children():
                self.search_results_tree.delete(row)

            for payment in filtered_payments:
                self.search_results_tree.insert(
                    "",
                    "end",
                    values=(
                        payment.get("payment_id", "N/A"),
                        payment.get("member_id", "N/A"),
                        payment.get("member_name", "N/A"),
                        payment.get("gym_name", "N/A"),
                        f"${float(payment.get('amount', 0)):.2f}",
                        payment.get("date", "N/A"),
                        payment.get("status", "N/A"),
                        payment.get("payment_type", "N/A"),
                    ),
                )

            if not filtered_payments:
                messagebox.showinfo("No Results", f"No payments found for User: {user_name}.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to search payments by user name: {e}")

    def refresh_search_results(self):
        """Refreshes the search results by clearing inputs and results."""
        # Reset Gym Search
        self.search_gym_dropdown.set("Select Gym")

        # Reset User Name Search
        self.search_user_name_entry.set("Select User Name")

        # Clear Search Results
        for row in self.search_results_tree.get_children():
            self.search_results_tree.delete(row)

    def get_gym_user_names(self):
        """Retrieve all Gym User names from the MemberManagement system."""
        try:
            members = MemberManagement.view_all_members()
            return [member["name"] for member in members if member["user_type"] == "Gym User"]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch gym user names: {e}")
            return []

    def get_all_gym_names(self):
        """Retrieve all Gym names from the MemberManagement system."""
        try:
            members = MemberManagement.view_all_members()
            gym_names = set(member["gym_name"] for member in members if member.get("gym_name"))
            return sorted(list(gym_names))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch gym names: {e}")
            return []


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Payment Management System")
    root.geometry("1200x800")
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    app = PaymentManagementFrame(root)
    app.grid(row=0, column=0, sticky='nsew')
    root.mainloop()
'''