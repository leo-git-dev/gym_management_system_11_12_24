from database.data_loader import DataLoader


class ScalabilityManager:
    @staticmethod
    def add_location(location_id, city, zones=None):
        locations = DataLoader.get_data("locations")
        if any(loc["location_id"] == location_id for loc in locations):
            raise ValueError("Location ID already exists.")

        new_location = {
            "location_id": location_id,
            "city": city,
            "zones": zones if zones else []
        }
        locations.append(new_location)
        DataLoader.save_data("locations", locations)
        return new_location

    @staticmethod
    def add_zone_to_location(location_id, zone_name):
        locations = DataLoader.get_data("locations")
        for location in locations:
            if location["location_id"] == location_id:
                if zone_name in location["zones"]:
                    raise ValueError("Zone already exists in this location.")
                location["zones"].append(zone_name)
                DataLoader.save_data("locations", locations)
                return location
        raise ValueError("Location ID not found.")
