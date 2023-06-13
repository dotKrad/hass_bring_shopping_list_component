class BSlSensor(Entity):

    def __init__(self, config):
        self._state = None
        self._purchase = []
        self._recently = []
        self._listId = config['id']
        self._name = config['id']

        if 'name' in config:
            self._name = config['name']

        self._locale = 'en-US'
        if 'locale' in config:
            self._locale = config['locale']

    @property
    def name(self):
        """Return the name of the sensor."""
        return SENSOR_PREFIX + self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        return ICON if len(self._purchase) > 0 else ICONEMPTY

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        attrs = {}
        attrs["Purchase"] = self._purchase
        attrs["Recently"] = self._recently
        attrs["List_Id"] = self._listId
        return attrs

    def getList(self, source=[], details=[], articles=[]):
        items = []
        for p in source:
            found = False
            for d in details:
                if p["name"] == d["itemId"]:
                    found = True
                    break

            item = {}
            item["image"] = p["name"]
            item["name"] = p["name"]
            item["specification"] = p["specification"]

            if found == True:
                item["image"] = d["userIconItemId"]

            item["key"] = item["image"]

            if(item["name"] in articles):
                item["name"] = articles[item["name"]]
            else:
                if(found == 0):
                    item["image"] = item["name"][0]

            item["image"] = self.purge(item["image"])
            # .lower().replace("é", "e").replace("ä", "ae").replace("-", "_").replace("ö", "oe").replace("ü", "ue").replace(" ", "_")

            # print("%s: %s => %s" % (item.key, item.name, item.specification))

            if "+" in item["specification"]:
                specs = item["specification"].split("+")

                for spec in specs:
                    temp = dict(item.items())
                    temp["specification"] = spec.strip()
                    items.append(temp)

            else:
                items.append(item)

        return items

    def update(self):
        self._items = []
        self._recently = []
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        # get articles US
        url = f"https://web.getbring.com/locale/articles.{self._locale}.json"
        articles = get(url=url).json()

        url = f"https://api.getbring.com/rest/bringlists/{self._listId}/details"
        details = get(url=url).json()

        url = f'https://api.getbring.com/rest/bringlists/{self._listId}'
        data = get(url=url).json()

        purchase = data["purchase"]
        recently = data["recently"]

        self._purchase = self.getList(purchase, details, articles)
        self._recently = self.getList(recently, details, articles)

        self._state = len(purchase)

    def purge(self, item):
        return item.lower()\
            .replace("é", "e")\
            .replace("ä", "ae")\
            .replace("-", "_")\
            .replace("ö", "oe")\
            .replace("ü", "ue")\
            .replace(" ", "_")