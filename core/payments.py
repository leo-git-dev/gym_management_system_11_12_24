# core/payments.py

from utils.helpers import generate_payment_id
from database.data_loader import DataLoader


class PaymentManager:
    @staticmethod
    def add_payment(member_id, amount, date, status, payment_type=None):
        """Add a new payment record to the database."""
        members = DataLoader.get_data("members")
        payments = DataLoader.get_data("payments")  # Load payments data

        # Validate member existence
        member = next((m for m in members if m["member_id"] == member_id), None)
        if not member:
            raise ValueError(f"Member ID {member_id} does not exist.")

        # Validate payment amount
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Payment amount must be greater than zero.")
        except ValueError as e:
            raise ValueError(f"Invalid payment amount: {e}")

        # Validate payment type
        valid_payment_types = ["Monthly", "Quarterly", "Annual"]
        if payment_type not in valid_payment_types:
            raise ValueError(f"Invalid payment type '{payment_type}'. "
                             f"Valid options are: {valid_payment_types}")

        # Retrieve gym details from the member's information
        gym_name = member.get("gym_name", "Unknown")

        # Generate a unique payment ID
        new_payment_id = generate_payment_id(payments, prefix="P")

        # Create a new payment record
        new_payment = {
            "payment_id": new_payment_id,
            "member_id": member_id,
            "member_name": member["name"],  # Add member's name for reference
            "gym_name": gym_name,
            "amount": f"{amount:.2f}",  # Store amount as a formatted string
            "date": date,
            "status": status,
            "payment_type": payment_type
        }
        payments.append(new_payment)

        # Save the updated payments data
        DataLoader.save_data("payments", payments)
        print(f"Payment added successfully for Member ID: {member_id} at Gym: {gym_name} with Payment Type: {payment_type}.")

    @staticmethod
    def validate_payment_type(payment_type):
        """
        Validate the payment type against available options.
        :param payment_type: The payment type to validate.
        :return: True if valid, raises ValueError otherwise.
        """
        valid_payment_types = ["Monthly", "Quarterly", "Annual"]
        if payment_type not in valid_payment_types:
            raise ValueError(f"Invalid payment type '{payment_type}'. "
                             f"Valid options are: {valid_payment_types}")
        return True

    @staticmethod
    def view_all_payments(payment_type=None):
        """
        Retrieve all payment records, optionally filtered by payment_type.
        :param payment_type: (Optional) Filter payments by this type.
        :return: List of payment records.
        """
        payments = DataLoader.get_data("payments")
        if payment_type:
            PaymentManager.validate_payment_type(payment_type)
            payments = [p for p in payments if p.get("payment_type") == payment_type]
        return payments

    @staticmethod
    def update_payment(payment_id, amount=None, date=None, status=None, payment_type=None):
        """
        Update an existing payment record.
        :param payment_id: ID of the payment to update.
        :param amount: (Optional) New amount.
        :param date: (Optional) New date.
        :param status: (Optional) New status.
        :param payment_type: (Optional) New payment type.
        :return: None
        """
        payments = DataLoader.get_data("payments")  # Load payments data
        payment = next((p for p in payments if p["payment_id"] == payment_id), None)

        if not payment:
            raise ValueError(f"Payment ID {payment_id} not found.")

        # Update the provided fields
        if amount is not None:
            try:
                amount = float(amount)
                if amount <= 0:
                    raise ValueError("Amount must be greater than zero.")
                payment["amount"] = f"{amount:.2f}"
            except ValueError as e:
                raise ValueError(f"Invalid amount: {e}")
        if date is not None:
            payment["date"] = date
        if status is not None:
            payment["status"] = status
        if payment_type is not None:
            PaymentManager.validate_payment_type(payment_type)
            payment["payment_type"] = payment_type

        # Save the updated payments list
        DataLoader.save_data("payments", payments)
        print(f"Payment ID {payment_id} updated successfully.")

    @staticmethod
    def delete_payment(payment_id):
        """
        Delete a payment record from the database.
        :param payment_id: ID of the payment to delete.
        :return: None
        """
        payments = DataLoader.get_data("payments")  # Load payments data
        updated_payments = [p for p in payments if p["payment_id"] != payment_id]

        if len(updated_payments) == len(payments):
            raise ValueError(f"Payment ID {payment_id} not found.")

        # Save the updated payments list
        DataLoader.save_data("payments", updated_payments)
        print(f"Payment ID {payment_id} deleted successfully.")

    @staticmethod
    def get_payments_by_member_id(member_id):
        """
        Retrieve all payment records for a specific member by their Member ID.
        :param member_id: The Member ID to search for.
        :return: A list of payment records for the given Member ID.
        """
        try:
            payments = DataLoader.get_data("payments")  # Assuming payments are stored in a JSON file or database
            # Filter payments by Member ID
            return [payment for payment in payments if payment["member_id"] == member_id]
        except Exception as e:
            print(f"Error fetching payments for Member ID {member_id}: {e}")
            return []

    @staticmethod
    def calculate_total_membership_value(gym_id, status):
        """
        Calculate the total membership value for gym users in a given gym by payment status.
        :param gym_id: The ID of the gym.
        :param status: The payment status to filter by (e.g., "Paid", "Pending").
        :return: Total membership value as a float.
        """
        members = DataLoader.get_data("members")
        payments = DataLoader.get_data("payments")

        # Filter gym users belonging to the gym
        gym_user_ids = {
            member["member_id"]
            for member in members
            if member["gym_id"] == gym_id and member["user_type"] == "Gym User"
        }

        # Calculate the total for payments with the given status
        total = sum(
            float(payment["amount"])
            for payment in payments
            if payment["status"] == status and payment["member_id"] in gym_user_ids
        )

        return total
