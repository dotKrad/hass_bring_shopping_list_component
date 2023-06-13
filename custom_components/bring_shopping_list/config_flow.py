"""Home Assistant bring shopping list integration Config Flow"""

from collections import OrderedDict

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers.selector import selector
from homeassistant.core import callback

from homeassistant.const import CONF_USERNAME, CONF_PASSWORD, CONF_NAME

from .const import DOMAIN
from .api import Bring


@callback
def configured_instances(hass):
    """Return a set of configured SimpliSafe instances."""
    entites = []
    for entry in hass.config_entries.async_entries(DOMAIN):
        entites.append(f"{entry.data.get(CONF_USERNAME)}")
    return set(entites)


class BSLFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Fpl Config Flow Handler"""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize."""
        self._errors = {}
        self.username = None
        self.password = None
        self.lists = []

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        self._errors = {}

        if user_input is not None:
            username = user_input[CONF_USERNAME]
            password = user_input[CONF_PASSWORD]

            if username not in configured_instances(self.hass):
                #session = async_create_clientsession(self.hass)
                self.username = username
                self.password = password
                api = Bring(username, password)

                await self.hass.async_add_executor_job(api.login)

                return await self._show_select_list_form(api=api)

            else:
                self._errors[CONF_NAME] = "name_exists"

            return await self._show_config_form(user_input)

        return await self._show_config_form(user_input)

    async def async_step_select_list(self, user_input=None):
        """ select list config flow """
        data = {}
        data["username"] = self.username
        data["password"] = self.password
        data["lists"] = []

        for item in self.lists:
            if item["name"] in user_input["lists"]:
                data["lists"].append(item["listUuid"])

        return self.async_create_entry(title=self.username, data=data)


    async def _show_select_list_form(self, api):

        lists = await self.hass.async_add_executor_job(api.loadLists)

        self.lists = lists["lists"]

        data_schema = OrderedDict()
        options = [node["name"] for node in lists["lists"]]

        data_schema["lists"] = selector({
            "select": {
                "options": options,
                "multiple" : True
                }
        })


        return self.async_show_form(
            step_id="select_list", data_schema=vol.Schema(data_schema), errors=self._errors
        )

    async def _show_config_form(self, user_input):
        """Show the configuration form to ask for credentials."""
        username = ""
        password = ""

        if user_input is not None:
            if CONF_USERNAME in user_input:
                username = user_input[CONF_USERNAME]
            if CONF_PASSWORD in user_input:
                password = user_input[CONF_PASSWORD]

        data_schema = OrderedDict()
        data_schema[vol.Required(CONF_USERNAME, default= username)] = str
        data_schema[vol.Required(CONF_PASSWORD, default= password)] = str

        return self.async_show_form(
            step_id="user", data_schema=vol.Schema(data_schema), errors=self._errors
        )

    async def async_step_import(self, user_input):  # pylint: disable=unused-argument
        """Import a config entry.
        Special type of import, we're not actually going to store any data.
        Instead, we're going to rely on the values that are in config file.
        """
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        return self.async_create_entry(title="configuration.yaml", data={})
