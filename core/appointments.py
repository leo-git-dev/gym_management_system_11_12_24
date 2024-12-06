from utils.helpers import generate_unique_id
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

        return results
