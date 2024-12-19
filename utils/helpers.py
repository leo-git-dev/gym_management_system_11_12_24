import uuid

def generate_unique_id(data, key):
    """
    Generate a unique ID based on existing data.

    :param data: List of dictionaries containing existing data.
    :param key: The key to check for uniqueness.
    :return: A unique string ID.
    """
    existing_ids = {item[key] for item in data if key in item}
    while True:
        new_id = str(uuid.uuid4())[:8]  # Generate a short unique ID
        if new_id not in existing_ids:
            return new_id


def validate_date(date_str):
    from datetime import datetime
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def format_currency(amount):
    return f"${amount:,.2f}"


def generate_payment_id(payments, prefix="P"):
    """
    Generates a unique payment ID with a prefix.
    :param payments: List of existing payments
    :param prefix: Prefix for the payment ID
    :return: A new unique payment ID
    """
    if not payments:  # If the list is empty
        return f"{prefix}1"
    existing_ids = [
        int(payment["payment_id"].replace(prefix, "")) for payment in payments if "payment_id" in payment
    ]
    return f"{prefix}{max(existing_ids, default=0) + 1}"

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