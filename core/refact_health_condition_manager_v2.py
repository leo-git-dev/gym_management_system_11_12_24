# refact_health_condition_manager_v2.py
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime, date
from core.member_management import MemberManagement
from core.health_condition_manager import HealthConditionManager
import math



class HealthConditionFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.is_logged_in = False
        self.create_login_screen()

    def create_login_screen(self):
        self.clear_widgets()
        frame = ttk.Frame(self)
        frame.grid(sticky="nsew", padx=20, pady=20)

        ttk.Label(frame, text="Secure Health Condition Area Login", font=("Helvetica", 14)).grid(row=0, column=0,
                                                                                                 columnspan=2, pady=10)

        ttk.Label(frame, text="Username:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.username_entry = ttk.Entry(frame)
        self.username_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(frame, text="Password:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.password_entry = ttk.Entry(frame, show="*")
        self.password_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        ttk.Button(frame, text="Login", command=self.handle_login).grid(row=3, column=0, columnspan=2, pady=10)

    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        # Simple demo logic: username=health_user, password=secret
        if username == "health_user" and password == "secret":
            self.is_logged_in = True
            self.create_health_form()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials.")

    def create_health_form(self):
        self.clear_widgets()
        frame = ttk.Frame(self)
        frame.grid(sticky="nsew", padx=20, pady=20)

        # Select gym member
        ttk.Label(frame, text="Select Gym Member:", font=("Helvetica", 12)).grid(row=0, column=0, sticky="e", padx=5,
                                                                                 pady=5)
        member_names = MemberManagement.get_all_member_names()
        self.member_name_var = tk.StringVar(value="Select Member")
        self.member_dropdown = ttk.Combobox(frame, textvariable=self.member_name_var, values=member_names,
                                            state="readonly")
        self.member_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.member_dropdown.bind("<<ComboboxSelected>>", self.load_member_info)

        # Member info area
        self.info_frame = ttk.Frame(frame)
        self.info_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        # Date of Birth
        ttk.Label(frame, text="Date of Birth:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.dob_calendar = Calendar(frame, selectmode="day", date_pattern="yyyy-mm-dd")
        self.dob_calendar.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.dob_calendar.bind("<<CalendarSelected>>", self.calculate_age)

        # Age Display
        ttk.Label(frame, text="Age:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.age_label = ttk.Label(frame, text="N/A")
        self.age_label.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Gender
        ttk.Label(frame, text="Gender:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.gender_var = tk.StringVar(value="Undisclosed")
        gender_options = ["Male", "Female", "Transgender Male", "Transgender Female", "Undisclosed"]
        self.gender_dropdown = ttk.Combobox(frame, textvariable=self.gender_var, values=gender_options,
                                            state="readonly")
        self.gender_dropdown.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        # Weight
        ttk.Label(frame, text="Weight (kg):").grid(row=5, column=0, sticky="e", padx=5, pady=5)
        kg_values = [str(i) for i in range(30, 201)]  # 30kg to 200kg
        g_values = [str(i * 100) for i in range(0, 10)]  # grams 0 to 900
        self.weight_kg_var = tk.StringVar(value="70")
        self.weight_kg_cb = ttk.Combobox(frame, textvariable=self.weight_kg_var, values=kg_values, state="readonly")
        self.weight_kg_cb.grid(row=5, column=1, sticky="w", padx=5, pady=5)
        self.weight_g_var = tk.StringVar(value="0")
        self.weight_g_cb = ttk.Combobox(frame, textvariable=self.weight_g_var, values=g_values, state="readonly")
        self.weight_g_cb.grid(row=5, column=2, sticky="w", padx=5, pady=5)

        # Height
        ttk.Label(frame, text="Height (cm):").grid(row=6, column=0, sticky="e", padx=5, pady=5)
        cm_values = [str(i) for i in range(100, 221)]  # 100cm to 220cm
        self.height_cm_var = tk.StringVar(value="170")
        self.height_cm_cb = ttk.Combobox(frame, textvariable=self.height_cm_var, values=cm_values, state="readonly")
        self.height_cm_cb.grid(row=6, column=1, padx=5, pady=5, sticky="w")

        # BMI Display
        ttk.Button(frame, text="Calculate BMI", command=self.calculate_bmi).grid(row=7, column=0, padx=5, pady=5,
                                                                                 sticky="e")
        self.bmi_label = ttk.Label(frame, text="N/A")
        self.bmi_label.grid(row=7, column=1, padx=5, pady=5, sticky="w")

        # BMI Classification
        ttk.Label(frame, text="BMI Classification:").grid(row=8, column=0, sticky="e", padx=5, pady=5)
        self.bmi_class_label = ttk.Label(frame, text="N/A")
        self.bmi_class_label.grid(row=8, column=1, padx=5, pady=5, sticky="w")

        # Pre-existing conditions
        ttk.Label(frame, text="Pre-existing medical conditions:").grid(row=9, column=0, sticky="e", padx=5, pady=5)
        self.conditions_text = tk.Text(frame, width=40, height=3)
        self.conditions_text.grid(row=9, column=1, columnspan=2, padx=5, pady=5, sticky="w")

        # Member's sport profile
        ttk.Label(frame, text="Member's Sport Profile:").grid(row=10, column=0, sticky="e", padx=5, pady=5)
        self.sport_profile_text = tk.Text(frame, width=40, height=3)
        self.sport_profile_text.grid(row=10, column=1, columnspan=2, padx=5, pady=5, sticky="w")

        # Further health details
        ttk.Label(frame, text="Further health details & medical conditions:").grid(row=11, column=0, sticky="e", padx=5,
                                                                                   pady=5)
        self.further_details_text = tk.Text(frame, width=40, height=5)
        self.further_details_text.grid(row=11, column=1, columnspan=2, padx=5, pady=5, sticky="w")

        ttk.Button(frame, text="Save", command=self.save_health_data).grid(row=12, column=0, columnspan=3, pady=10)

    def clear_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()

    def load_member_info(self, event):
        name = self.member_name_var.get()
        if not name or name == "Select Member":
            return
        member = MemberManagement.search_member(name=name)
        if not member:
            return
        # Display member info
        for w in self.info_frame.winfo_children():
            w.destroy()

        info_str = (
            f"ID: {member['member_id']}\n"
            f"Name: {member['name']}\n"
            f"User Type: {member['user_type']}\n"
            f"Gym: {member['gym_name']}\n"
            f"City: {member['city']}\n"
            f"Cost: {member['cost']}\n"
            f"Payment Type: {member['payment_type']}\n"
            f"Loyalty Points: {member.get('loyalty_points', 0)}\n"
        )
        ttk.Label(self.info_frame, text=info_str, justify="left").pack(anchor="w")

        # Load existing health data if any
        health_data = HealthConditionManager.get_member_health(member["member_id"])
        if health_data:
            # Populate fields
            if "dob" in health_data:
                try:
                    self.dob_calendar.set_date(health_data["dob"])
                    self.calculate_age()
                except:
                    pass
            if "gender" in health_data:
                self.gender_var.set(health_data["gender"])
            if "weight_kg" in health_data:
                self.weight_kg_var.set(str(health_data["weight_kg"]))
            if "weight_g" in health_data:
                self.weight_g_var.set(str(health_data["weight_g"]))
            if "height_cm" in health_data:
                self.height_cm_var.set(str(health_data["height_cm"]))
            if "conditions" in health_data:
                self.conditions_text.delete("1.0", tk.END)
                self.conditions_text.insert("1.0", health_data["conditions"])
            if "sport_profile" in health_data:
                self.sport_profile_text.delete("1.0", tk.END)
                self.sport_profile_text.insert("1.0", health_data["sport_profile"])
            if "further_details" in health_data:
                self.further_details_text.delete("1.0", tk.END)
                self.further_details_text.insert("1.0", health_data["further_details"])

            if "bmi" in health_data:
                self.bmi_label.config(text=str(health_data["bmi"]))
            if "bmi_class" in health_data:
                self.bmi_class_label.config(text=str(health_data["bmi_class"]))

    def calculate_age(self, event=None):
        dob_str = self.dob_calendar.get_date()
        try:
            dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
            today = date.today()
            age_days = (today - dob).days
            years = age_days // 365
            days_remaining = age_days % 365
            self.age_label.config(text=f"{years} years and {days_remaining} days")
        except:
            self.age_label.config(text="N/A")

    def calculate_bmi(self):
        try:
            kg = int(self.weight_kg_var.get())
            g = int(self.weight_g_var.get())
            total_weight = kg + (g / 1000.0)
            cm = int(self.height_cm_var.get())
            meters = cm / 100.0
            bmi = total_weight / (meters ** 2)
            bmi = round(bmi, 1)
            self.bmi_label.config(text=str(bmi))

            # Classification
            if bmi <= 18.4:
                classification = "Underweight"
            elif 18.5 <= bmi <= 22.9:
                classification = "Healthy"
            elif 23 <= bmi <= 27.4:
                classification = "Overweight"
            else:
                classification = "Obese"
            self.bmi_class_label.config(text=classification)
        except:
            messagebox.showerror("Error", "Invalid weight/height for BMI calculation.")

    def save_health_data(self):
        name = self.member_name_var.get()
        if not name or name == "Select Member":
            messagebox.showerror("Error", "Please select a member.")
            return
        member = MemberManagement.search_member(name=name)
        if not member:
            messagebox.showerror("Error", "Member not found.")
            return
        member_id = member["member_id"]

        dob = self.dob_calendar.get_date()
        gender = self.gender_var.get()
        weight_kg = int(self.weight_kg_var.get())
        weight_g = int(self.weight_g_var.get())
        height_cm = int(self.height_cm_var.get())
        conditions = self.conditions_text.get("1.0", tk.END).strip()
        sport_profile = self.sport_profile_text.get("1.0", tk.END).strip()
        further_details = self.further_details_text.get("1.0", tk.END).strip()

        bmi_str = self.bmi_label.cget("text")
        bmi_class_str = self.bmi_class_label.cget("text")

        if bmi_str == "N/A":
            self.calculate_bmi()
            bmi_str = self.bmi_label.cget("text")
            bmi_class_str = self.bmi_class_label.cget("text")

        # Create health data dict
        health_info = {
            "dob": dob,
            "gender": gender,
            "weight_kg": weight_kg,
            "weight_g": weight_g,
            "height_cm": height_cm,
            "bmi": bmi_str,
            "bmi_class": bmi_class_str,
            "conditions": conditions,
            "sport_profile": sport_profile,
            "further_details": further_details
        }

        HealthConditionManager.update_member_health(member_id, health_info)
        messagebox.showinfo("Success", "Health information saved successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Payment Management System")
    root.geometry("1400x900")  # Increased size to accommodate more columns
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    app = HealthConditionFrame(root)
    app.grid(row=0, column=0, sticky='nsew')
    root.mainloop()