from utils.helpers import generate_unique_id
from database.data_loader import DataLoader
from core.member_management import MemberManagement
# Removed the top-level import of GymManager to prevent circular import

class AppointmentManager:
    @staticmethod
    def schedule_appointment(member_id, trainer_id, date, time, cost, status):
        # Local import to prevent circular dependency
        from core.gym_management import GymManager

        appointments = DataLoader.get_data("appointments")
        new_appointment_id = generate_unique_id(appointments, "appointment_id")

        new_appointment = {
            "appointment_id": str(new_appointment_id),  # Numeric ID as string
            "member_id": member_id,
            "trainer_id": trainer_id,
            "date": date,
            "time": time,
            "cost": cost,
            "status": status
        }
        appointments.append(new_appointment)
        DataLoader.save_data("appointments", appointments)
        print(f"Appointment scheduled with ID: {new_appointment_id}")

    @staticmethod
    def view_all_appointments():
        appointments = DataLoader.get_data("appointments")
        for a in appointments:
            a.setdefault("appointment_id", "Unknown")
            a.setdefault("member_id", "Unknown")
            a.setdefault("trainer_id", "Unknown")
            a.setdefault("date", "Unknown")
            a.setdefault("time", "Unknown")
            a.setdefault("cost", 0.0)       # Default cost if missing
            a.setdefault("status", "Pending")  # Default status if missing
        return appointments

    @staticmethod
    def view_all_appointments_enriched():
        # Local import to prevent circular dependency
        from core.gym_management import GymManager

        # Enrich with: wellbeing_staff_name, specialty (activity), gym_user_name, gym_name, cost, status
        appointments = AppointmentManager.view_all_appointments()
        members = MemberManagement.view_all_members()
        gyms = GymManager.view_all_gyms()

        members_by_id = {m["member_id"]: m for m in members}
        gyms_by_id = {g["gym_id"]: g for g in gyms}

        enriched = []
        for appt in appointments:
            member = members_by_id.get(appt["member_id"], {})
            trainer = members_by_id.get(appt["trainer_id"], {})
            gym_data = gyms_by_id.get(trainer.get("gym_id", ""), {})

            enriched.append({
                "appointment_id": appt["appointment_id"],
                "wellbeing_staff_name": trainer.get("name", "Unknown"),
                "specialty": trainer.get("activity", "Unknown"),
                "gym_user_name": member.get("name", "Unknown"),
                "gym_name": gym_data.get("gym_name", "Unknown"),
                "date": appt["date"],
                "time": appt["time"],
                "cost": float(appt["cost"]),
                "status": appt["status"]
            })
        return enriched

    @staticmethod
    def delete_appointment(appointment_id):
        appointments = DataLoader.get_data("appointments")
        updated_appointments = [a for a in appointments if str(a["appointment_id"]) != str(appointment_id)]
        if len(updated_appointments) < len(appointments):
            DataLoader.save_data("appointments", updated_appointments)
            return True
        return False

    @staticmethod
    def update_appointment(appointment_id, new_date=None, new_time=None, new_trainer=None):
        appointments = DataLoader.get_data("appointments")
        for appointment in appointments:
            if str(appointment["appointment_id"]) == str(appointment_id):
                if new_date:
                    appointment["date"] = new_date
                if new_time:
                    appointment["time"] = new_time
                if new_trainer:
                    appointment["trainer_id"] = new_trainer
                DataLoader.save_data("appointments", appointments)
                return True
        return False

    @staticmethod
    def get_appointment_by_id(appointment_id):
        appointments = DataLoader.get_data("appointments")
        for a in appointments:
            if str(a["appointment_id"]) == str(appointment_id):
                return a
        return None

    @staticmethod
    def is_double_booked(trainer_id, date, time, exclude_id=None):
        appointments = DataLoader.get_data("appointments")
        for a in appointments:
            if a["trainer_id"] == trainer_id and a["date"] == date and a["time"] == time:
                if exclude_id and str(a["appointment_id"]) == str(exclude_id):
                    continue
                return True
        return False

    @staticmethod
    def search_appointments_by_wellbeing_name(wellbeing_name):
        # Local import to prevent circular dependency
        from core.gym_management import GymManager

        # Filter after enrichment
        all_appts = AppointmentManager.view_all_appointments_enriched()
        return [a for a in all_appts if a["wellbeing_staff_name"] == wellbeing_name]

'''from utils.helpers import generate_unique_id
from database.data_loader import DataLoader


class AppointmentManager:
    @staticmethod
    def schedule_appointment(member_id, trainer_id, date, time):
        appointments = DataLoader.get_data("appointments")
        new_appointment_id = generate_unique_id(appointments, "appointment_id")

        new_appointment = {
            "appointment_id": f"A{new_appointment_id}",
            "member_id": member_id,
            "trainer_id": trainer_id,
            "date": date,
            "time": time
        }
        appointments.append(new_appointment)
        DataLoader.save_data("appointments", appointments)
        print(f"Appointment scheduled successfully with ID: A{new_appointment_id}")

    @staticmethod
    def view_all_appointments():
        """
        Retrieve all appointments and ensure compatibility with updated structure.
        """
        appointments = DataLoader.get_data("appointments")
        for appointment in appointments:
            # Ensure backward compatibility for missing fields
            appointment.setdefault("appointment_id", "Unknown")
            appointment.setdefault("member_id", "Unknown")
            appointment.setdefault("trainer_id", "Unknown")
            appointment.setdefault("date", "Unknown")
            appointment.setdefault("time", "Unknown")
        return appointments

    @staticmethod
    def delete_appointment(appointment_id):
        appointments = DataLoader.get_data("appointments")
        updated_appointments = [a for a in appointments if a["appointment_id"] != appointment_id]
        if len(updated_appointments) < len(appointments):
            DataLoader.save_data("appointments", updated_appointments)
            return True
        return False

    @staticmethod
    def update_appointment(appointment_id, new_date=None, new_time=None, new_trainer=None):
        appointments = DataLoader.get_data("appointments")
        for appointment in appointments:
            if appointment["appointment_id"] == appointment_id:
                if new_date:
                    appointment["date"] = new_date
                if new_time:
                    appointment["time"] = new_time
                if new_trainer:
                    appointment["trainer_id"] = new_trainer
                DataLoader.save_data("appointments", appointments)
                return True
        return False

    @staticmethod
    def search_appointments(member_id=None, member_name=None, trainer_name=None, gym_name=None):
        appointments = DataLoader.get_data("appointments")
        members = DataLoader.get_data("members")
        trainers = DataLoader.get_data("trainers")
        gyms = DataLoader.get_data("gyms")

        results = []
        for appointment in appointments:
            member = next((m for m in members if m["member_id"] == appointment["member_id"]), None)
            trainer = next((t for t in trainers if t["trainer_id"] == appointment["trainer_id"]), None)
            gym = next((g for g in gyms if g["gym_id"] == trainer["gym_id"]), None) if trainer else None

            if (
                    (member_id and appointment["member_id"] == member_id) or
                    (member_name and member and member["name"] == member_name) or
                    (trainer_name and trainer and trainer["name"] == trainer_name) or
                    (gym_name and gym and gym["name"] == gym_name)
            ):
                results.append(appointment)

        return results'''
