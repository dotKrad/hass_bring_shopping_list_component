"""Data Update Coordinator"""
import logging
from datetime import timedelta

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.core import HomeAssistant

from .api import Bring
from .const import DOMAIN


SCAN_INTERVAL = timedelta(seconds=1200)

_LOGGER: logging.Logger = logging.getLogger(__package__)


class BSLDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    def __init__(self, hass: HomeAssistant, client: Bring) -> None:
        """Initialize."""
        self.api = client
        self.platforms = []

        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=SCAN_INTERVAL)

    async def _async_update_data(self):
        """Update data via library."""
        try:
            data = {}
            await self.hass.async_add_executor_job(self.api.login)
            lists = await self.hass.async_add_executor_job(self.api.loadLists)

            for l in lists["lists"]:
                uuid = l['listUuid']
                data[uuid] = l

                items = await self.hass.async_add_executor_job(self.api.getItems, l)
                data[uuid]["items"] = items

            return data
        except Exception as exception:
            raise UpdateFailed() from exception
