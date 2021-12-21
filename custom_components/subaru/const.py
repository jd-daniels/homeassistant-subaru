"""Constants for the Subaru integration."""
from enum import Enum

from homeassistant.const import Platform

DOMAIN = "subaru_jd"
FETCH_INTERVAL = 300
UPDATE_INTERVAL = 7200
CONF_UPDATE_ENABLED = "update_enabled"
CONF_NOTIFICATION_OPTION = "notification_option"
CONF_COUNTRY = "country"


class NotificationOptions(Enum):
    """Lovelace levels of notification."""

    FAILURE = "Failure — Only notify on failure"
    PENDING = "Pending — Temporary notification of remote command in progress"
    SUCCESS = "Success — Persistent notification of completed remote command"

    @classmethod
    def list(cls):
        """List values of NotificationOptions."""
        return [item.value for item in NotificationOptions]

    @classmethod
    def get_by_value(cls, value):
        """Get enum instance by value."""
        for item in cls:
            if item.value == value:
                return item


# entry fields
ENTRY_CONTROLLER = "controller"
ENTRY_COORDINATOR = "coordinator"
ENTRY_VEHICLES = "vehicles"
ENTRY_LISTENER = "listener"

# update coordinator name
COORDINATOR_NAME = "subaru_data"

# info fields
VEHICLE_VIN = "vin"
VEHICLE_NAME = "display_name"
VEHICLE_HAS_EV = "is_ev"
VEHICLE_API_GEN = "api_gen"
VEHICLE_HAS_REMOTE_START = "has_res"
VEHICLE_HAS_REMOTE_SERVICE = "has_remote"
VEHICLE_HAS_SAFETY_SERVICE = "has_safety"
VEHICLE_LAST_UPDATE = "last_update"
VEHICLE_STATUS = "status"

API_GEN_1 = "g1"
API_GEN_2 = "g2"
MANUFACTURER = "Subaru Corp."

REMOTE_SERVICE_FETCH = "fetch_jd"
REMOTE_SERVICE_UPDATE = "update_jd"
REMOTE_SERVICE_LOCK = "lock_jd"
REMOTE_SERVICE_UNLOCK = "unlock_jd"
REMOTE_SERVICE_LIGHTS = "lights_jd"
REMOTE_SERVICE_LIGHTS_STOP = "lights_stop_jd"
REMOTE_SERVICE_HORN = "horn_jd"
REMOTE_SERVICE_HORN_STOP = "horn_stop_jd"
REMOTE_SERVICE_REMOTE_START = "remote_start_jd"
REMOTE_SERVICE_REMOTE_STOP = "remote_stop_jd"
REMOTE_SERVICE_CHARGE_START = "charge_start_jd"

SUPPORTED_PLATFORMS = [
    Platform.BINARY_SENSOR,
    Platform.DEVICE_TRACKER,
    Platform.LOCK,
    Platform.SENSOR,
]

ICONS = {
    "Avg Fuel Consumption": "mdi:leaf",
    "EV Range": "mdi:ev-station",
    "Odometer": "mdi:road-variant",
    "Range": "mdi:gas-station",
}
