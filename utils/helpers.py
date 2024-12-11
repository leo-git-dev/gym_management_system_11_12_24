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

'''
def generate_unique_id(data_list, id_field, prefix='C'):
    """
    Generate a unique ID by incrementing the highest existing ID.

    :param data_list: List of existing data dictionaries.
    :param id_field: The field name containing the ID.
    :param prefix: The prefix for the ID (e.g., 'C' for classes).
    :return: An integer representing the new unique ID.
    """
    max_id = 0
    for item in data_list:
        current_id_str = item.get(id_field, "")
        if current_id_str.startswith(prefix):
            try:
                # Strip the prefix and convert the remaining part to int
                current_id = int(current_id_str[len(prefix):])
                if current_id > max_id:
                    max_id = current_id
            except ValueError:
                # Handle cases where the ID doesn't follow the expected format
                continue
    return max_id + 1
'''

'''
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
'''

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
