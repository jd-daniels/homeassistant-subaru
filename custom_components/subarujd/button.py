"""Support for Subaru buttons."""
import logging

from homeassistant.components.button import DOMAIN as BUTTON_DOMAIN, ButtonEntity

from . import DOMAIN as SUBARU_DOMAIN
from .const import (
    CONF_NOTIFICATION_OPTION,
    ENTRY_CONTROLLER,
    ENTRY_COORDINATOR,
    ENTRY_VEHICLES,
    ICONS,
    REMOTE_SERVICE_CHARGE_START,
    REMOTE_SERVICE_FETCH,
    REMOTE_SERVICE_HORN,
    REMOTE_SERVICE_HORN_STOP,
    REMOTE_SERVICE_LIGHTS,
    REMOTE_SERVICE_LIGHTS_STOP,
    REMOTE_SERVICE_REMOTE_START,
    REMOTE_SERVICE_REMOTE_STOP,
    REMOTE_SERVICE_UPDATE,
    VEHICLE_CLIMATE_SELECTED_PRESET,
    VEHICLE_HAS_EV,
    VEHICLE_HAS_REMOTE_SERVICE,
    VEHICLE_HAS_REMOTE_START,
)
from .entity import SubaruEntity
from .remote_service import async_call_remote_service

_LOGGER = logging.getLogger(__name__)

BUTTON_TYPE = "type"
BUTTON_SERVICE = "service"

G1_REMOTE_BUTTONS = [
    {BUTTON_TYPE: "Horn Start", BUTTON_SERVICE: REMOTE_SERVICE_HORN},
    {BUTTON_TYPE: "Horn Stop", BUTTON_SERVICE: REMOTE_SERVICE_HORN_STOP},
    {BUTTON_TYPE: "Lights Start", BUTTON_SERVICE: REMOTE_SERVICE_LIGHTS},
    {BUTTON_TYPE: "Lights Stop", BUTTON_SERVICE: REMOTE_SERVICE_LIGHTS_STOP},
    {BUTTON_TYPE: "Locate", BUTTON_SERVICE: REMOTE_SERVICE_UPDATE},
    {BUTTON_TYPE: "Refresh", BUTTON_SERVICE: REMOTE_SERVICE_FETCH},
]

RES_REMOTE_BUTTONS = [
    {BUTTON_TYPE: "Remote Start", BUTTON_SERVICE: REMOTE_SERVICE_REMOTE_START},
    {BUTTON_TYPE: "Remote Stop", BUTTON_SERVICE: REMOTE_SERVICE_REMOTE_STOP},
]

EV_REMOTE_BUTTONS = [
    {BUTTON_TYPE: "Charge EV", BUTTON_SERVICE: REMOTE_SERVICE_CHARGE_START}
]


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Subaru button by config_entry."""
    coordinator = hass.data[SUBARU_DOMAIN][config_entry.entry_id][ENTRY_COORDINATOR]
    vehicle_info = hass.data[SUBARU_DOMAIN][config_entry.entry_id][ENTRY_VEHICLES]
    entities = []
    for vin in vehicle_info:
        entities.extend(
            create_vehicle_buttons(vehicle_info[vin], coordinator, config_entry)
        )
    async_add_entities(entities, True)


def create_vehicle_buttons(vehicle_info, coordinator, config_entry):
    """Instantiate all available buttons for the vehicle."""
    buttons_to_add = []
    if vehicle_info[VEHICLE_HAS_REMOTE_SERVICE]:
        buttons_to_add.extend(G1_REMOTE_BUTTONS)

        if vehicle_info[VEHICLE_HAS_REMOTE_START] or vehicle_info[VEHICLE_HAS_EV]:
            buttons_to_add.extend(RES_REMOTE_BUTTONS)

        if vehicle_info[VEHICLE_HAS_EV]:
            buttons_to_add.extend(EV_REMOTE_BUTTONS)

    return [
        SubaruButton(
            vehicle_info, coordinator, config_entry, b[BUTTON_TYPE], b[BUTTON_SERVICE],
        )
        for b in buttons_to_add
    ]


class SubaruButton(SubaruEntity, ButtonEntity):
    """Representation of a Subaru button."""

    def __init__(self, vehicle_info, coordinator, config_entry, entity_type, service):
        """Initialize the button for the vehicle."""
        super().__init__(vehicle_info, coordinator)
        self.entity_type = entity_type
        self.hass_type = BUTTON_DOMAIN
        self.config_entry = config_entry
        self.service = service
        self.arg = None

    @property
    def icon(self):
        """Return the icon of the sensor."""
        if not self.device_class:
            return ICONS.get(self.entity_type)

    async def async_press(self):
        """Press the button."""
        _LOGGER.debug("%s button pressed for %s", self.entity_type, self.car_name)
        arg = None
        if self.service == REMOTE_SERVICE_REMOTE_START:
            arg = self.coordinator.data.get(self.vin).get(
                VEHICLE_CLIMATE_SELECTED_PRESET
            )
        controller = self.hass.data[SUBARU_DOMAIN][self.config_entry.entry_id][
            ENTRY_CONTROLLER
        ]
        await async_call_remote_service(
            self.hass,
            controller,
            self.service,
            self.vehicle_info,
            arg,
            self.config_entry.options.get(CONF_NOTIFICATION_OPTION),
        )
        await self.coordinator.async_refresh()
