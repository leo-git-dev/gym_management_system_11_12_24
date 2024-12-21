class WorkoutZone:
    def __init__(self, name, equipment=None, schedule=None):
        self.name = name
        self.equipment = equipment if equipment else []
        self.schedule = schedule if schedule else {}

    def add_equipment(self, equipment_name):
        if equipment_name not in self.equipment:
            self.equipment.append(equipment_name)
        else:
            raise ValueError(f"{equipment_name} is already in the equipment list.")

    def update_schedule(self, day, time_slot):
        self.schedule[day] = time_slot

