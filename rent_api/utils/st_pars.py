from re import finditer, MULTILINE, findall
from requests import get
from bs4 import BeautifulSoup

from models import Appartments


class TvoiaSt:
    """Класс с сайта твоя столица"""

    ROOM_1 = "1"
    ROOM_2 = "2"
    ROOM_3 = "3"
    ROOM_4 = "4"

    URL = f"https://www.t-s.by/buy/flats/filter/rooms-is-"

    def get_number_re(self, text):
        regex_ad = r"^\d+"
        matches = finditer(regex_ad, text, MULTILINE)
        result = ""
        # import pdb;pdb.set_trace()
        for match in matches:
            result = match.group()
        return result

    def get_available_appart(self):
        """Достаем количество объявлений для каждой квартиры.
        1 Создаем новый урл.
        2 Достаем через реквес гет
        """
        url_1_ap = self.URL + self.ROOM_1 + "/"
        st_req = get(url_1_ap)
        soup_st = BeautifulSoup(st_req.text, "html.parser")
        max_appart_str = soup_st.find_all("div", {"class": "page__header--result"})[
            0
        ].get_text()
        max_appart_str = max_appart_str.replace(" ", "")
        max_appart = self.get_number_re(max_appart_str)
        return int(max_appart), url_1_ap

    def get_html(self, name, html):
        with open(f"{name}.csv", "w+") as f:
            f.write(str(html))

    def exctract_st_apparts(self, html):
        """Достаем из html нужную инфу и возвращаем дикт"""
        link = "https://www.t-s.by" + html.find("a", {"class": "card-item__link"}).get(
            "href"
        )
        address = html.find(
            "div", {"class": "card-item__header"}
        ).next.next.next.replace(" ", "")
        floor = html.find("li", {"class": "card-item__params--item"}).find("span").text
        try:
            price = "".join(
                findall(
                    "\d+",
                    html.find("div", {"class": "card-item__usd-price"}).next,
                    MULTILINE,
                )
            )  # regular experess
        except AttributeError:
            price = "discuss"
        square_meters = html.find(
            "ul", {"class": "card-item__params card-item__params--flats"}
        ).next.next.next.replace(" ", "")
        return {
            "address": address,
            "floor": floor,
            "price": price,
            "link": link,
            "meters": square_meters,
        }

    def extract_appart(self, number_appart, url):
        apparts = []
        res = get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        results = soup.find_all(
            "div",
            {
                "class": "card-item card-item-new js-maphover js-addfavorblock paginator-item"
            },
        )
        # import pdb; pdb.set_trace()
        for result in results:
            appart = self.exctract_st_apparts(result)
            apparts.append(appart)
        return apparts

    def main(self):
        last_page, url = self.get_available_appart()
        quarters = self.extract_appart(last_page, url)
        self.get_html("st", quarters)
        return quarters


t = TvoiaSt()
print(t.main())
