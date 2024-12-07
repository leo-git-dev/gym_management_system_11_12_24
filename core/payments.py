from utils.helpers import generate_payment_id
from database.data_loader import DataLoader


class PaymentManager:
    @staticmethod
    def add_payment(member_id, amount, date, status):
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
            "status": status
        }
        payments.append(new_payment)

        # Save the updated payments data
        DataLoader.save_data("payments", payments)
        print(f"Payment added successfully for Member ID: {member_id} at Gym: {gym_name}.")

    @staticmethod
    def view_all_payments():
        return DataLoader.get_data("payments")

    @staticmethod
    def update_payment(payment_id, amount=None, date=None, status=None):
        payments = DataLoader.get_data("payments")  # Load payments data
        payment = next((p for p in payments if p["payment_id"] == payment_id), None)

        if not payment:
            raise ValueError(f"Payment ID {payment_id} not found.")

        # Update the provided fields
        if amount:
            payment["amount"] = f"{float(amount):.2f}"
        if date:
            payment["date"] = date
        if status:
            payment["status"] = status

        # Save the updated payments list
        DataLoader.save_data("payments", payments)
        print(f"Payment ID {payment_id} updated successfully.")

    @staticmethod
    def delete_payment(payment_id):
        payments = DataLoader.get_data("payments")  # Load payments data
        updated_payments = [p for p in payments if p["payment_id"] != payment_id]

        if len(updated_payments) == len(payments):
            raise ValueError(f"Payment ID {payment_id} not found.")

        # Save the updated payments list
        DataLoader.save_data("payments", updated_payments)
        print(f"Payment ID {payment_id} deleted successfully.")

'''

from utils.helpers import generate_unique_id
from database.data_loader import DataLoader


class PaymentManager:
    @staticmethod
    def add_payment(member_id, amount, date, status):
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Payment amount must be greater than zero.")
        except ValueError as e:
            print(f"Invalid payment amount: {e}")
            return

        payments = DataLoader.get_data("payments")
        new_payment_id = generate_unique_id(payments, "payment_id")

        new_payment = {
            "payment_id": f"P{new_payment_id}",
            "member_id": member_id,
            "amount": str(amount),  # Store amount as string for consistency in CSV
            "date": date,
            "status": status
        }
        payments.append(new_payment)
        DataLoader.save_data("payments", payments)
        print(f"Payment added successfully with ID: P{new_payment_id}")

    @staticmethod
    def view_all_payments():
        return DataLoader.get_data("payments")
'''