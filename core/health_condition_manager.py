# health_condition_manager.py
import json
import os
from cryptography.fernet import Fernet

HEALTH_DATA_FILE = "health_data.json"
# In a real environment, store this key securely and do not hard-code
ENCRYPTION_KEY = Fernet.generate_key()
fernet = Fernet(ENCRYPTION_KEY)

class HealthConditionManager:
    @staticmethod
    def load_data():
        if not os.path.exists(HEALTH_DATA_FILE):
            return {}
        with open(HEALTH_DATA_FILE, "rb") as f:
            encrypted_data = f.read()
            if not encrypted_data:
                return {}
        try:
            decrypted_data = fernet.decrypt(encrypted_data)
            return json.loads(decrypted_data.decode())
        except Exception:
            # If decryption fails or file is empty
            return {}

    @staticmethod
    def save_data(data):
        encoded = json.dumps(data).encode()
        encrypted_data = fernet.encrypt(encoded)
        with open(HEALTH_DATA_FILE, "wb") as f:
            f.write(encrypted_data)

    @staticmethod
    def get_member_health(member_id):
        data = HealthConditionManager.load_data()
        return data.get(member_id, {})

    @staticmethod
    def update_member_health(member_id, health_info):
        data = HealthConditionManager.load_data()
        data[member_id] = health_info
        HealthConditionManager.save_data(data)
