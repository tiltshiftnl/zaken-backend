import logging

import requests
from django.conf import settings
from tenacity import after_log, retry, stop_after_attempt

logger = logging.getLogger(__name__)


@retry(stop=stop_after_attempt(3), after=after_log(logger, logging.ERROR))
def generic_decos_request(url):
    try:
        headers = {"Accept": "application/itemdata"}
        username = settings.DECOS_JOIN_USERNAME
        password = settings.DECOS_JOIN_PASSWORD
        response = requests.get(
            url, headers=headers, timeout=8, auth=(username, password)
        )
        data = response.json()
        return data
    except Exception as e:
        print(e)

    return {}


def get_decos_join_permit():
    print("Starting Decos Join Request")
    url = (
        "https://decosdvl.acc.amsterdam.nl:443/decosweb/aspx/api/v1/items/90642DCCC2DB46469657C3D0DF0B1ED7/COBJECTS?filter=TEXT8"
        " eq 'Herengracht' and INITIALS eq '1'"
    )
    data = generic_decos_request(url)
    print("First request")
    print(data)
    items = data.get("links", [])
    items_urls = [item.get("href") for item in items]
    print("Nested items urls")
    print(items_urls)
    data_items = [generic_decos_request(url) for url in items_urls]
    print("All data items")
    print(data_items)
    return {"items": data_items}