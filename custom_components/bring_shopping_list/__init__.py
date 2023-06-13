"""Bring Shopping List Component"""
import logging
import pprint



from .dataUpdateCoordinator import BSLDataUpdateCoordinator
from .const import DOMAIN
from .api import Bring


_LOGGER = logging.getLogger(__package__)

async def async_setup(hass, config):
    def handle_swap_item(call):
        name = call.data.get('key')
        entity = call.data.get('entityId')
        print(f"handle event with key {name} from {entity}")
        pprint.pprint(hass.states.get(entity))

    #bring = config[DOMAIN]
    #hass.services.async_register(DOMAIN, 'swap_item', handle_swap_item)
    #hass.helpers.discovery.load_platform('sensor', DOMAIN, bring, config)

    return True

    # print(config)
    #hass.states.async_set('bring.world', 'Earth')
    #hass.states.async_set('bring.purchase', 'Alufolie,Tampons')
    #hass.data[DOMAIN] = {'temperature': 23}

    #component = hass.data[DOMAIN] = EntityComponent(_LOGGER, DOMAIN, hass, SCAN_INTERVAL)
    # await component.async_setup(config)

async def async_setup_entry(hass, entry):
    """Set up this integration using UI."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})

    # Get "global" configuration.
    username = entry.data.get("username")
    password = entry.data.get("password")

    client = Bring(username, password)

    coordinator = BSLDataUpdateCoordinator(hass, client=client)
    await coordinator.async_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    hass.async_add_job(hass.config_entries.async_forward_entry_setup(entry, "sensor"))

    return True
