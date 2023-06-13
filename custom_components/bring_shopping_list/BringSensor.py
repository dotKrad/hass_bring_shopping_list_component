"""Sensor"""

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

ICON = "mdi:cart"
ICONEMPTY = "mdi:cart-outline"

class BringSensor(CoordinatorEntity, SensorEntity):
    """Sensor"""
    def __init__(self, coordinator, config_entry, l):
        super().__init__(coordinator)
        self.config_entry = config_entry
        self.list = l
        self.sensorName = l["name"]
        self.uuid = l["listUuid"]

    @property
    def native_value(self):
        lista = self.coordinator.data.get(self.uuid)

        if lista is not None:
            self._attr_native_value = len(lista["items"]["purchase"])

        return self._attr_native_value

    @property
    def unique_id(self):
        """Return the ID of this device."""
        sensorName = self.sensorName.lower().replace(" ", "")
        return f"{self.uuid}_{sensorName}"

    @property
    def name(self):
        sensorName = self.sensorName.lower().replace(" ", "")
        return f"{DOMAIN}_{sensorName}"

    #@property
    #def device_info(self):
    #    return {
    #        "identifiers": {(DOMAIN, self.uuid)},
    #        "name": f"Bring list {self.sensorName}",
    #        "model": "1",
    #        "manufacturer": "Bring",
    #    }

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        lista = self.coordinator.data.get(self.uuid)

        return ICON if len(lista["items"]["purchase"]) > 0 else ICONEMPTY

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        attributes = {
            "attribution": "Data provided by Bring Shopping List",
            "integration": "Bring Shopping List",
        }
        #attributes.update(self.customAttributes())
        lista = self.coordinator.data.get(self.uuid)

        attributes["Purchase"] = lista["items"]["purchase"]
        attributes["Recently"] = lista["items"]["recently"]
        attributes["List_Id"] = self.uuid

        return attributes
