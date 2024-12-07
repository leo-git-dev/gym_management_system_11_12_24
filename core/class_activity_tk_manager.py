import tkinter as tk
from tkinter import ttk, messagebox
from core.class_activity_manager import ClassActivityManager


class ClassManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Class Management")
        self.create_widgets()

    def create_widgets(self):
        # Tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True, fill="both")

        self.add_tab = ttk.Frame(notebook)
        self.view_tab = ttk.Frame(notebook)

        notebook.add(self.add_tab, text="Add Class")
        notebook.add(self.view_tab, text="View/Manage Classes")

        self.create_add_tab()
        self.create_view_tab()

    def create_add_tab(self):
        ttk.Label(self.add_tab, text="Class Name:").grid(row=0, column=0, padx=5, pady=5)
        self.class_name_entry = ttk.Entry(self.add_tab)
        self.class_name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.add_tab, text="Trainer Name:").grid(row=1, column=0, padx=5, pady=5)
        self.trainer_name_entry = ttk.Entry(self.add_tab)
        self.trainer_name_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.add_tab, text="Schedule (Day/Time):").grid(row=2, column=0, padx=5, pady=5)
        self.schedule_entry = ttk.Entry(self.add_tab)
        self.schedule_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.add_tab, text="Capacity:").grid(row=3, column=0, padx=5, pady=5)
        self.capacity_entry = ttk.Entry(self.add_tab)
        self.capacity_entry.grid(row=3, column=1, padx=5, pady=5)

        add_button = ttk.Button(self.add_tab, text="Add Class", command=self.add_class)
        add_button.grid(row=4, column=0, columnspan=2, pady=10)

    def create_view_tab(self):
        self.classes_tree = ttk.Treeview(
            self.view_tab,
            columns=("ID", "Name", "Trainer", "Schedule", "Capacity"),
            show="headings",
        )
        self.classes_tree.heading("ID", text="Class ID")
        self.classes_tree.heading("Name", text="Class Name")
        self.classes_tree.heading("Trainer", text="Trainer Name")
        self.classes_tree.heading("Schedule", text="Schedule")
        self.classes_tree.heading("Capacity", text="Capacity")
        self.classes_tree.pack(expand=True, fill="both")

        view_button = ttk.Button(self.view_tab, text="Refresh", command=self.view_all_classes)
        view_button.pack(pady=5)

        manage_frame = ttk.Frame(self.view_tab)
        manage_frame.pack(fill="x")

        ttk.Label(manage_frame, text="Class ID:").grid(row=0, column=0, padx=5, pady=5)
        self.manage_class_id_entry = ttk.Entry(manage_frame)
        self.manage_class_id_entry.grid(row=0, column=1, padx=5, pady=5)

        update_button = ttk.Button(manage_frame, text="Update Class", command=self.update_class)
        update_button.grid(row=0, column=2, padx=5, pady=5)

        delete_button = ttk.Button(manage_frame, text="Delete Class", command=self.delete_class)
        delete_button.grid(row=0, column=3, padx=5, pady=5)

    def add_class(self):
        class_name = self.class_name_entry.get()
        trainer_name = self.trainer_name_entry.get()
        schedule = self.schedule_entry.get()
        capacity = self.capacity_entry.get()

        try:
            ClassActivityManager.add_class(class_name, trainer_name, schedule, capacity)
            messagebox.showinfo("Success", "Class added successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add class: {e}")

    def view_all_classes(self):
        classes = ClassActivityManager.view_all_classes()
        for row in self.classes_tree.get_children():
            self.classes_tree.delete(row)
        for cls in classes:
            self.classes_tree.insert(
                "",
                "end",
                values=(cls["class_id"], cls["class_name"], cls["trainer_name"], cls["schedule"], cls["capacity"]),
            )

    def update_class(self):
        class_id = self.manage_class_id_entry.get()
        # Implementation for updating a class goes here.

    def delete_class(self):
        class_id = self.manage_class_id_entry.get()

        try:
            ClassActivityManager.delete_class(class_id)
            messagebox.showinfo("Success", "Class deleted successfully.")
            self.view_all_classes()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete class: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ClassManagementApp(root)
    root.mainloop()
