import pprint
DOMAIN = 'bring_shopping_list'


async def async_setup(hass, config):
    def handle_swap_item(call):
        name = call.data.get('key')
        entity = call.data.get('entityId')
        print(f"handle event with key {name} from {entity}")
        pprint.pprint(hass.states.get(entity))

    bring = config[DOMAIN]
    hass.services.async_register(DOMAIN, 'swap_item', handle_swap_item)
    hass.helpers.discovery.load_platform('sensor', DOMAIN, bring, config)

    return True

    # print(config)
    #hass.states.async_set('bring.world', 'Earth')
    #hass.states.async_set('bring.purchase', 'Alufolie,Tampons')
    #hass.data[DOMAIN] = {'temperature': 23}

    #component = hass.data[DOMAIN] = EntityComponent(_LOGGER, DOMAIN, hass, SCAN_INTERVAL)
    # await component.async_setup(config)
