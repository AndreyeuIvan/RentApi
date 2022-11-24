from re import finditer, MULTILINE, findall
from requests import get
from math import ceil
from bs4 import BeautifulSoup

from models import Appartments

ROOM_1 = "1k"
ROOM_2 = "2k"
ROOM_3 = "3k"
ROOM_4 = "4k"

URL = f"https://realt.by/rent/flat-for-long/"


def get_number_req(text):
    """Забираем количество объялений из выражения. Получаем число. Часто в выражении может появлятся количество отображений на странице, что удаляется 2 запросом"""
    regex_ad = r"\d+\s\bобъявлений\b"
    matches = finditer(regex_ad, text, MULTILINE)
    result = ""
    for match in matches:
        result = match.group()
    regex_digit = r"\d+"
    matches_digit = finditer(regex_digit, result, MULTILINE)
    for match in matches_digit:
        result = int(match.group())
    return result


def get_html(name, html):
    with open(f"{name}.csv", "w+") as f:
        f.write(str(html))


def get_last_page(url, room):
    """Находим максимум квартир по новому url"""
    url_ = url + room
    realt_req = get(url_)
    soup_realt = BeautifulSoup(realt_req.text, "html.parser")
    paginator = soup_realt.find_all("div", {"class": "mt-sm"})
    number_of_appa = paginator[1].get_text()
    ad_value = get_number_req(number_of_appa)
    last_page = ceil(ad_value / 20)  # only for realt.by
    return last_page, url_


def exctract_realt_apparts(html):
    """Достаем из html нужную инфу и возвращаем дикт"""
    link = html.find("a", {"class": "image mb-0"}).get("href")
    address = html.find("div", {"class": "color-graydark"}).text[2:-1]
    floor = html.find("div", {"class": "info-large"}).text[19:28]
    try:
        price = [
            int(i)
            for i in findall(
                "\d+", html.find("div", {"class": "col-auto"}).text, MULTILINE
            )
        ][
            0
        ]  # regular experess
    except AttributeError:
        price = "discuss"
    id_realt = int(
        html.find("span", {"class": "flex-grow-1 justify-content-md-end"}).text[3:]
    )
    date_publ = "".join(
        findall(
            r"\d{2}\.\d{2}\.\d{4}",
            html.find("div", {"class": "info-mini color-graydark"}).text,
            MULTILINE,
        )
    )  # re
    phone = html.find("span", {"class": "color-black"}).text
    square_meters = html.find("div", {"class": "info-large"}).text[11:15]
    return {
        "address": address,
        "floor": floor,
        "price": price,
        "id": id_realt,
        "phone": phone,
        "link": link,
        "date": date_publ,
        "meters": square_meters,
    }


def extract_appart(last_page, url):
    """Собираем в цикле все объявления"""
    apparts = []
    for page in range(1, last_page):
        res = get(f"{url}?pages={page}")
        soup = BeautifulSoup(res.text, "html.parser")
        results = soup.find_all("div", {"data-mode": "2"})
        for result in results:
            appart = exctract_realt_apparts(result)
            # save to DB
            Appartments(
                address=appart.get("address"),
                floor=appart.get("floor"),
                price=appart.get("price"),
                id_r=appart.get("id"),
                phone=appart.get("phone"),
                link=appart.get("link"),
                date=appart.get("date"),
                meters=appart.get("meters"),
            )
            # add sqlalchemy save!
            apparts.append(appart)
    return apparts


def main():
    last_page, url = get_last_page(URL, ROOM_1)
    quarters = extract_appart(last_page, url)
    return quarters


get_html("realt.txt", main())
