import unittest
from unittest.mock import patch, MagicMock
from core.payments import PaymentManager
from utils.helpers import generate_payment_id


class TestPaymentManager(unittest.TestCase):

    @patch("database.data_loader.DataLoader.get_data")
    @patch("database.data_loader.DataLoader.save_data")
    @patch("utils.helpers.generate_payment_id")
    def test_add_payment(self, mock_generate_payment_id, mock_save_data, mock_get_data):
        # Mock data for members and payments
        mock_members = [
            {"member_id": "123", "name": "John Doe", "gym_id": "G1", "gym_name": "Gym A"},
        ]
        mock_payments = []

        # Mock return values
        mock_get_data.side_effect = lambda key: mock_members if key == "members" else mock_payments
        mock_generate_payment_id.return_value = "P1"  # Correct ID with prefix

        # Call the method under test
        PaymentManager.add_payment("123", 100.0, "2024-01-01", "Paid")

        # Verify results
        self.assertEqual(len(mock_payments), 1)
        self.assertEqual(mock_payments[0]["payment_id"], "P1")
        self.assertEqual(mock_payments[0]["member_id"], "123")
        self.assertEqual(mock_payments[0]["amount"], "100.00")
        self.assertEqual(mock_payments[0]["status"], "Paid")

        mock_save_data.assert_called_once_with("payments", mock_payments)

    @patch("database.data_loader.DataLoader.get_data")
    def test_view_all_payments(self, mock_get_data):
        mock_payments = [
            {"payment_id": "P1", "member_id": "123", "amount": "100.00", "date": "2024-01-01", "status": "Paid"}
        ]
        mock_get_data.return_value = mock_payments

        result = PaymentManager.view_all_payments()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["payment_id"], "P1")

    @patch("database.data_loader.DataLoader.get_data")
    @patch("database.data_loader.DataLoader.save_data")
    def test_update_payment(self, mock_save_data, mock_get_data):
        mock_payments = [
            {"payment_id": "P1", "member_id": "123", "amount": "100.00", "date": "2024-01-01", "status": "Paid"}
        ]
        mock_get_data.return_value = mock_payments

        PaymentManager.update_payment("P1", amount=200.0, status="Pending")

        self.assertEqual(mock_payments[0]["amount"], "200.00")
        self.assertEqual(mock_payments[0]["status"], "Pending")
        mock_save_data.assert_called_once_with("payments", mock_payments)

    @patch("database.data_loader.DataLoader.get_data")
    @patch("database.data_loader.DataLoader.save_data")
    def test_delete_payment(self, mock_save_data, mock_get_data):
        mock_payments = [
            {"payment_id": "P1", "member_id": "123", "amount": "100.00", "date": "2024-01-01", "status": "Paid"}
        ]
        mock_get_data.return_value = mock_payments.copy()  # Use a copy to avoid mutation issues

        PaymentManager.delete_payment("P1")
        updated_payments = [p for p in mock_payments if p["payment_id"] != "P1"]

        self.assertEqual(len(updated_payments), 0)
        mock_save_data.assert_called_once_with("payments", updated_payments)

    @patch("database.data_loader.DataLoader.get_data")
    def test_get_payments_by_member_id(self, mock_get_data):
        mock_payments = [
            {"payment_id": "P1", "member_id": "123", "amount": "100.00", "status": "Paid"},
            {"payment_id": "P2", "member_id": "456", "amount": "200.00", "status": "Pending"}
        ]
        mock_get_data.return_value = mock_payments

        result = PaymentManager.get_payments_by_member_id("123")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["payment_id"], "P1")

    @patch("database.data_loader.DataLoader.get_data")
    def test_calculate_total_membership_value(self, mock_get_data):
        mock_members = [
            {"member_id": "123", "gym_id": "G1", "user_type": "Gym User"},
            {"member_id": "456", "gym_id": "G1", "user_type": "Gym User"}
        ]
        mock_payments = [
            {"payment_id": "P1", "member_id": "123", "amount": "100.00", "status": "Paid"},
            {"payment_id": "P2", "member_id": "456", "amount": "200.00", "status": "Paid"},
            {"payment_id": "P3", "member_id": "123", "amount": "50.00", "status": "Pending"}
        ]
        mock_get_data.side_effect = lambda key: mock_members if key == "members" else mock_payments

        total = PaymentManager.calculate_total_membership_value("G1", "Paid")
        self.assertEqual(total, 300.0)


if __name__ == "__main__":
    unittest.main()
