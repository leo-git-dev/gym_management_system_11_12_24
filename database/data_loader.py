# database/data_loader.py

import json
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataLoader:
    # Define the base directory relative to this file's location
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))

    # Updated data_sources to use only JSON
    data_sources = {
        "members": {
            "file": os.path.join(base_dir, "members.json"),
            "type": "json"
        },
        "payments": {
            "file": os.path.join(base_dir, "payments.json"),
            "type": "json"
        },
        "appointments": {
            "file": os.path.join(base_dir, "appointments.json"),
            "type": "json"
        },
        "attendance": {
            "file": os.path.join(base_dir, "attendance.json"),
            "type": "json"
        },
        "gyms": {
            "file": os.path.join(base_dir, "gyms.json"),
            "type": "json"
        },
        "locations": {
            "file": os.path.join(base_dir, "locations.json"),
            "type": "json"
        },
        "classes": {
            "file": os.path.join(base_dir, "classes.json"),
            "type": "json"
        },
        "staff_roles": {
            "file": os.path.join(base_dir, "staff_roles.json"),
            "type": "json"
        }
    }

    @staticmethod
    def get_data(source_name):
        """Retrieve data from the specified JSON source."""
        source = DataLoader.data_sources.get(source_name)
        if not source:
            logger.error(f"Data source '{source_name}' not found.")
            raise ValueError(f"Data source '{source_name}' not found.")

        file_path = source["file"]
        if not os.path.exists(file_path):
            DataLoader._initialize_file(source)

        if source["type"] == "json":
            try:
                with open(file_path, "r") as f:
                    data = json.load(f)
                # Ensure data is a list
                if not isinstance(data, list):
                    logger.warning(f"Data in {source_name}.json is not a list. Resetting to empty list.")
                    data = []
            except json.JSONDecodeError:
                logger.warning(f"{source_name}.json is empty or malformed. Initializing as empty list.")
                data = []
                DataLoader.save_data(source_name, data)
            except Exception as e:
                logger.error(f"Error reading {source_name}.json: {e}")
                raise
            return data

    @staticmethod
    def save_data(source_name, data):
        """Save data to the specified JSON source."""
        source = DataLoader.data_sources.get(source_name)
        if not source:
            logger.error(f"Data source '{source_name}' not found.")
            raise ValueError(f"Data source '{source_name}' not found.")

        file_path = source["file"]
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        if source["type"] == "json":
            try:
                with open(file_path, "w") as f:
                    json.dump(data, f, indent=4)
                logger.info(f"Data saved to {source_name}.json successfully.")
            except Exception as e:
                logger.error(f"Failed to save data to {source_name}.json: {e}")
                raise

    @staticmethod
    def _initialize_file(source):
        """Initialize a new JSON data file with an empty list."""
        file_path = source["file"]
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        try:
            with open(file_path, "w") as f:
                json.dump([], f, indent=4)
            logger.info(f"Initialized JSON file: {file_path}")
        except Exception as e:
            logger.error(f"Failed to initialize {source['file']}: {e}")
            raise

    @staticmethod
    def _normalize_data(data, required_fields):
        """Ensure all required fields are present in each data entry."""
        for entry in data:
            for field in required_fields:
                if field not in entry:
                    entry[field] = ""  # Assign a default value if missing
        return data

'''
import csv
import json
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataLoader:
    base_dir = os.path.join("../gym_management_system", "database")

    data_sources = {
        "members": {
            "file": os.path.join(base_dir, "members.csv"),
            "type": "csv",
            "headers": [
                "member_id", "name", "user_type", "membership_type", "join_date", "gym_id", "gym_name",
                "role", "activities", "schedule", "cost", "activity", "expertise"
            ]
        },
        "payments": {
            "file": os.path.join(base_dir, "payments.csv"),
            "type": "csv",
            "headers": ["payment_id", "member_id", "member_name", "gym_id", "gym_name", "amount", "date", "status"]
        },
        "appointments": {"file": os.path.join(base_dir, "appointments.json"), "type": "json"},
        "attendance": {
            "file": os.path.join(base_dir, "attendance.csv"),
            "type": "csv",
            "headers": ["attendance_id", "member_id", "class_id", "date", "time", "workout_zone", "equipment_used"]
        },
        "gyms": {"file": os.path.join(base_dir, "gyms.csv"), "type": "csv", "headers": ["gym_id", "gym_name", "city"]},
        "locations": {"file": os.path.join(base_dir, "locations.json"), "type": "json"},
        "classes": {"file": os.path.join(base_dir, "classes.json"), "type": "json"},
        "staff_roles": {"file": os.path.join(base_dir, "staff_roles.json"), "type": "json"}
    }

    @staticmethod
    def get_data(source_name):
        """Retrieve data from the specified source."""
        source = DataLoader.data_sources.get(source_name)
        if not source:
            raise ValueError(f"Data source {source_name} not found.")

        file_path = source["file"]
        if not os.path.exists(file_path):
            DataLoader._initialize_file(source)

        if source["type"] == "csv":
            with open(file_path, "r") as f:
                data = list(csv.DictReader(f))
            return DataLoader._normalize_data(data, source["headers"])
        elif source["type"] == "json":
            with open(file_path, "r") as f:
                return json.load(f)

    @staticmethod
    def save_data(source_name, data):
        """Save data to the specified source."""
        source = DataLoader.data_sources.get(source_name)
        if not source:
            raise ValueError(f"Data source {source_name} not found.")

        file_path = source["file"]
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        if source["type"] == "csv":
            with open(file_path, "w", newline="") as f:
                headers = source["headers"]
                if data:
                    extra_headers = set(data[0].keys()) - set(headers)
                    headers += list(extra_headers)
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                writer.writerows(data)
        elif source["type"] == "json":
            with open(file_path, "w") as f:
                json.dump(data, f, indent=4)

    @staticmethod
    def _initialize_file(source):
        """Initialize a new data file with headers or an empty structure."""
        file_path = source["file"]
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        if source["type"] == "csv":
            with open(file_path, "w", newline="") as f:
                if headers := source.get("headers"):
                    writer = csv.writer(f)
                    writer.writerow(headers)
        elif source["type"] == "json":
            with open(file_path, "w") as f:
                json.dump([], f)
        logger.info(f"Initialized {source['type']} file: {file_path}")

    @staticmethod
    def _normalize_data(data, headers):
        """Normalize data to ensure all required fields are present."""
        for row in data:
            for header in headers:
                if header not in row:
                    row[header] = ""  # Assign default value
        return data
'''