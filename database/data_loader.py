import csv
import json
import os

class DataLoader:
    # Define the base directory for the database files
    base_dir = os.path.join("../st_marys_fitness", "database")

    # Data source definitions
    data_sources = {
        "members": {"file": os.path.join(base_dir, "members.csv"), "type": "csv"},
        "payments": {"file": os.path.join(base_dir, "payments.csv"), "type": "csv"},
        "appointments": {"file": os.path.join(base_dir, "appointments.json"), "type": "json"},
        "attendance": {"file": os.path.join(base_dir, "attendance.csv"), "type": "csv"},
        "gyms": {"file": "database/gyms.csv", "type": "csv"},
        "locations": {"file": "database/locations.json", "type": "json"}  # Added this
    }

    @staticmethod
    def get_data(source_name):
        """Retrieve data from the specified source."""
        source = DataLoader.data_sources.get(source_name)
        if not source:
            raise ValueError(f"Data source {source_name} not found.")
        try:
            if source["type"] == "csv":
                with open(source["file"], "r") as f:
                    return list(csv.DictReader(f))
            elif source["type"] == "json":
                with open(source["file"], "r") as f:
                    return json.load(f)
            else:
                raise ValueError(f"Unsupported data type for source {source_name}.")
        except FileNotFoundError:
            print(f"File not found: {source['file']}")
            return []  # Return an empty list if the file doesn't exist

    @staticmethod
    def save_data(source_name, data):
        if source_name not in DataLoader.data_sources:
            raise ValueError(f"Data source {source_name} not found.")

        source = DataLoader.data_sources[source_name]
        file_path = source["file"]

        if source["type"] == "csv":
            with open(file_path, "w", newline="") as f:
                # Dynamically determine the fieldnames from the first item in data
                fieldnames = data[0].keys() if data else []
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
                print(f"Data saved to {file_path} successfully.")

        elif source["type"] == "json":
            with open(file_path, "w") as f:
                json.dump(data, f, indent=4)
                print(f"Data saved to {file_path} successfully.")