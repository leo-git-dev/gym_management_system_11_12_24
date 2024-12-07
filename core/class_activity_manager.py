from utils.helpers import generate_unique_id
from database.data_loader import DataLoader


class ClassActivityManager:
    @staticmethod
    def add_class(class_name, trainer_name, schedule, capacity):
        classes = DataLoader.get_data("classes")

        # Generate a unique class ID
        new_class_id = generate_unique_id(classes, "class_id")

        new_class = {
            "class_id": f"C{new_class_id}",
            "class_name": class_name,
            "trainer_name": trainer_name,
            "schedule": schedule,
            "capacity": int(capacity),
        }
        classes.append(new_class)
        DataLoader.save_data("classes", classes)
        print(f"Class '{class_name}' added successfully with ID: {new_class_id}")

    @staticmethod
    def view_all_classes():
        return DataLoader.get_data("classes")

    @staticmethod
    def update_class(class_id, field, new_value):
        classes = DataLoader.get_data("classes")
        class_to_update = next((c for c in classes if c["class_id"] == class_id), None)

        if not class_to_update:
            raise ValueError(f"Class ID {class_id} not found.")

        if field not in class_to_update:
            raise ValueError(f"Field '{field}' is not valid for classes.")

        # Update the specified field
        class_to_update[field] = new_value
        DataLoader.save_data("classes", classes)
        print(f"Class ID {class_id} updated successfully.")

    @staticmethod
    def delete_class(class_id):
        classes = DataLoader.get_data("classes")
        updated_classes = [c for c in classes if c["class_id"] != class_id]

        if len(updated_classes) == len(classes):
            raise ValueError(f"Class ID {class_id} not found.")

        DataLoader.save_data("classes", updated_classes)
        print(f"Class ID {class_id} deleted successfully.")
