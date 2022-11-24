from requests import get

from bs4 import BeautifulSoup

"""
Parse onliner.by rent USE SELENIUM
"""

ROOM_1 = "?rent_type[]=1_room"
ROOM_2 = "?rent_type[]=2_rooms"
ROOM_3 = "?rent_type[]=3_rooms"
ROOM_4 = "?rent_type[]=4_rooms"
ROOM_5 = "?rent_type[]=5_rooms"
ROOM_6 = "?rent_type[]=6_rooms"


URL = f"https://r.onliner.by/ak/"


def extract_max_appart(url, room):
    """ Парсим сайт, максимум квартир по количеству комнат"""
    url = URL + ROOM_1
    onliner_req = get(url)
    pages = []

    soup_onliner = BeautifulSoup(onliner_req.text, "html.parser")

    paginator = soup_onliner.find_all("div", {"class": "pagination-dropdown"})

    with open("onliner.html", "w+") as f:
        f.write(str(paginator))

    import pdb

    pdb.set_trace()
    return soup_onliner


print(extract_max_appart(URL, ROOM_1))
