from utils.helpers import generate_payment_id
from database.data_loader import DataLoader


class PaymentManager:
    @staticmethod
    def add_payment(member_id, amount, date, status):
        members = DataLoader.get_data("members")
        payments = DataLoader.get_data("payments")

        # Validate member existence
        member = next((m for m in members if m["member_id"] == member_id), None)
        if not member:
            print(f"Error: Member ID {member_id} does not exist.")
            return

        # Validate payment amount
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Payment amount must be greater than zero.")
        except ValueError as e:
            print(f"Invalid payment amount: {e}")
            return

        # Get gym details for the member
        gym_id = member.get("location_id", "Unknown")
        gym_name = member.get("location_name", "Unknown")

        # Generate a unique payment ID
        new_payment_id = generate_payment_id(payments, prefix="P")

        # Create a new payment record
        new_payment = {
            "payment_id": new_payment_id,
            "member_id": member_id,
            "member_name": member["name"],  # Add member's name for reference
            "gym_id": gym_id,
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