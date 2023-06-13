import os.path
import logging
import json
import requests
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from datetime import datetime
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_PORT, CONF_SSL
from homeassistant.helpers.entity import Entity
from requests import get

from .const import DOMAIN
from .BringSensor import BringSensor

#import pprint

__version__ = '0.0.1'

ICON = "mdi:cart"
ICONEMPTY = "mdi:cart-outline"
CONF_LISTS = 'lists'
CONF_LOCALE = 'locale'
SENSOR_PREFIX = 'bring_shopping_list_'

LOGGER = logging.getLogger(__name__)


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({

    # vol.Optional(CONF_SSL, default=False): cv.boolean,
    # vol.Optional(CONF_SSL_CERT, default=False): cv.boolean,
    # vol.Required(CONF_TOKEN): cv.string,
    # vol.Optional(CONF_MAX, default=5): cv.string,
    # vol.Optional(CONF_SERVER): cv.string,
    # vol.Optional(CONF_DL_IMAGES, default=True): cv.boolean,
    # vol.Optional(CONF_HOST, default='localhost'): cv.string,
    # vol.Optional(CONF_PORT, default=32400): cv.port,
    vol.Required(CONF_LISTS): vol.All(cv.ensure_list, [cv.string]),
    vol.Optional(CONF_LOCALE, default='en-US'): cv.string,
    # vol.Optional(CONF_IMG_CACHE, default='/custom-lovelace/upcoming-media-card/images/plex/'): cv.string
})


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""

    lists = entry.data.get("lists")

    coordinator = hass.data[DOMAIN][entry.entry_id]

    bsl_lists = []

    for uuid in lists:
        l = coordinator.data.get(uuid)
        bsl_lists.append(BringSensor(coordinator, entry, l))

    async_add_devices(bsl_lists)



