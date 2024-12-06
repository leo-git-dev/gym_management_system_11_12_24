def validate_date(date_str):
    from datetime import datetime
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def format_currency(amount):
    return f"${amount:,.2f}"


def generate_unique_id(data, id_field):
    """
    Generate a unique ID based on existing records.

    :param data: List of existing records.
    :param id_field: The field name containing the ID in each record.
    :return: A new unique ID as an integer.
    """
    if not data:  # If the list is empty
        return 1
    existing_ids = [int(item.get(id_field, 0)) for item in data if id_field in item]
    return max(existing_ids) + 1


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

'''
    if not data:
        return 1
    existing_ids = []
    for item in data:
        id_value = item[id_field]
        # Extract numeric part of the ID
        numeric_part = ''.join(filter(str.isdigit, id_value))
        if numeric_part.isdigit():
            existing_ids.append(int(numeric_part))
    return max(existing_ids) + 1 if existing_ids else 1 
    '''
