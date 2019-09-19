# hass_bring_shopping_list_component (work in progress)


```
bring_shopping_list:
  lists:
    - id: xxxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
      name: Home
      locale: en-US
    - id: xxxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
      name: Work
      locale: de-DE
```


# Main Config:

|NAME|TYPE|DEFAULT|DESCRIPTION|
|-|-|-|-|
|id|string|**REQUIRED**| The list id|
|name|string|optional|This is used to make sensor name friendly otherwise id will be used. Example <code>**sensor.bring_shopping_list_home**</code> |
|locale|string|en-US|Locale used to get the name of the items.|
