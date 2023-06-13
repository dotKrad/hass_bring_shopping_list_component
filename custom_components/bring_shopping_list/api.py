"""Bring Shopping List api client"""

import traceback
import requests


class Bring:
    """
    Bring API client.
    """

    def __init__(self, mail, password, headers = None):
        self.mail = mail
        self.password = password
        self.url = 'https://api.getbring.com/rest/v2/'
        self.uuid = ''
        self.name = ''
        self.bearerToken = ''
        self.refreshToken = ''

        if headers:
            self.headers = headers
        else:
            self.headers = {
                'Authorization': '',
                'X-BRING-API-KEY': 'cof4Nc6D8saplXjE3h3HXqHH8m7VU2i1Gs0g85Sp',
                'X-BRING-CLIENT-SOURCE': 'webApp',
                'X-BRING-CLIENT': 'webApp',
                'X-BRING-COUNTRY': 'US',
                'X-BRING-USER-UUID': ''
            }
        self.putHeaders = {
            'Authorization': '',
            'X-BRING-API-KEY': '',
            'X-BRING-CLIENT-SOURCE': '',
            'X-BRING-CLIENT': '',
            'X-BRING-COUNTRY': '',
            'X-BRING-USER-UUID': '',
            'Content-Type': ''
        }


    def login(self):
        """
        Try to login.

        Returns
        -------
        Response
            The server response object."""
        try:
            r = requests.post(f'{self.url}bringauth', data=f'email={self.mail}&password={self.password}', timeout=5)
        except:
            print('Exception: Cannot login:')
            traceback.print_exc()
            raise

        data = r.json()
        self.name = data['name']
        self.uuid = data['uuid']
        self.bearerToken = data['access_token']
        self.refreshToken = data['refresh_token']

        self.headers['X-BRING-USER-UUID'] = self.uuid
        self.headers['Authorization'] = f'Bearer {self.bearerToken}'
        self.putHeaders = {
            'Authorization': self.headers['Authorization'],
            'X-BRING-API-KEY': self.headers['X-BRING-API-KEY'],
            'X-BRING-CLIENT-SOURCE': self.headers['X-BRING-CLIENT-SOURCE'],
            'X-BRING-CLIENT': self.headers['X-BRING-CLIENT'],
            'X-BRING-COUNTRY': self.headers['X-BRING-COUNTRY'],
            'X-BRING-USER-UUID': self.headers['X-BRING-USER-UUID'],
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        return r

    def loadLists(self):
        """Load all shopping lists.

        Returns
        -------
        dict
            The JSON response as a dict."""
        try:
            r = requests.get(f'{self.url}bringusers/{self.uuid}/lists', headers=self.headers, timeout= 5).json()

            #https://api.getbring.com/rest/v2/bringusersettings/f450665a-97e4-416e-bf17-87d31c45d2eb
            us = requests.get(f'{self.url}bringusersettings/{self.uuid}', headers=self.headers, timeout= 5).json()

            uls = us["userlistsettings"]

            for l in r["lists"]:
                userSettings = next((obj for obj in uls if obj["listUuid"] == l['listUuid']),None)["usersettings"]
                locale = next((obj for obj in userSettings if obj["key"] == "listArticleLanguage"),None)["value"]
                l["listArticleLanguage"] = locale

            return r
        except:
            print('Exception: Cannot get lists: ')
            traceback.print_exc()
            raise


    def getItems(self, _list):
        """
        Get all items from a shopping list.

        Parameters
        ----------
        _list : object
            A list returned by loadLists()

        Returns
        -------
        dict
            The JSON response as a dict.
        """

        try:
            #get items
            listUuid = _list['listUuid']
            items = requests.get(f'{self.url}bringlists/{listUuid}', headers = self.headers, timeout= 5).json()

            #get articles
            #https://web.getbring.com/locale/articles.en-US.json
            locale = _list["listArticleLanguage"]
            articles = requests.get(f'https://web.getbring.com/locale/articles.{locale}.json', headers = self.headers, timeout= 5).json()

            for item in items["purchase"]:
                itemId = item["name"]
                #item["id"] = item["name"]
                if itemId in articles.keys():
                    item["name"] = articles[itemId]
                item["image"] = self.sanitize(itemId)

            return items
        except:
            print(f'Exception: Cannot get items for list {listUuid}:')
            traceback.print_exc()
            raise

    def getAllItemDetails(self, listUuid):
        """
        Get all details from a shopping list.

        Parameters
        ----------
        listUuid : str
            A list uuid returned by loadLists()

        Returns
        -------
        list
            The JSON response as a list.
        """
        try:
            r = requests.get(f'{self.url}bringlists/{listUuid}/details', headers = self.headers, timeout=5)
            return r.json()
        except:
            print(f'Exception: Cannot get item details for list {listUuid}:')
            traceback.print_exc()
            raise


    def saveItem(self, listUuid, itemName, specification=''):
        """
        Save an item to a shopping list.

        Parameters
        ----------
        listUuid : str
            A list uuid returned by loadLists()
        itemName : str
            The name of the item you want to save.
        specification : str, optional
            The details you want to add to the item.

        Returns
        -------
        Response
            The server response object.
        """
        try:
            data = f'&purchase={itemName}&recently=&specification={specification}&remove=&sender=null'
            r = requests.put(f'{self.url}bringlists/{listUuid}', headers=self.putHeaders, data=data, timeout=5)
            return r
        except:
            print(f'Exception: Cannot save item {itemName} ({specification}) to {listUuid}:')
            traceback.print_exc()
            raise

    def removeItem(self, listUuid, itemName):
        """
        Remove an item from a shopping list.

        Parameters
        ----------
        listUuid : str
            A list uuid returned by loadLists()
        itemName : str
            The name of the item you want to remove.

        Returns
        -------
        Response
            The server response object.
        """
        try:
            data=f'&purchase=&recently=&specification=&remove={itemName}&sender=null'
            r = requests.put(f'{self.url}bringlists/{listUuid}', headers=self.putHeaders, data=data, timeout=5)
            return r
        except:
            print(f'Exception: Cannot remove item {itemName} from {listUuid}:')
            traceback.print_exc()
            raise

    def sanitize(self, item):
        "purge id for http call"
        return item.lower()\
            .replace("é", "e")\
            .replace("ä", "ae")\
            .replace("-", "_")\
            .replace("ö", "oe")\
            .replace("ü", "ue")\
            .replace(" ", "_")
