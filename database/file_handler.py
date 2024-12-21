import csv
import json


class FileHandler:
    @staticmethod
    def read_csv(filepath):
        try:
            with open(filepath, mode="r") as file:
                return list(csv.DictReader(file))
        except FileNotFoundError:
            return []

    @staticmethod
    def write_csv(filepath, data, fieldnames):
        with open(filepath, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

    @staticmethod
    def read_json(filepath):
        try:
            with open(filepath, mode="r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    @staticmethod
    def write_json(filepath, data):
        with open(filepath, mode="w") as file:
            json.dump(data, file, indent=4)
