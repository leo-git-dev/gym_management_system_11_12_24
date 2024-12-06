from enum import Enum

class MembershipType(Enum):
    REGULAR = "Regular"
    PREMIUM = "Premium"
    TRIAL = "Trial"

class PaymentStatus(Enum):
    COMPLETED = "Completed"
    PENDING = "Pending"

class ZoneType(Enum):
    CARDIO = "Cardio"
    STRENGTH = "Strength"
    YOGA = "Yoga"
