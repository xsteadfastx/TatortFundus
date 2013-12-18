import re
from mechanize import Browser
from bs4 import BeautifulSoup


class Episode(object):
    def __init__(self, episoden_name):
        self.episoden_name = episoden_name
        self.full_site = self.browse()

    def browse(self):
        br = Browser()
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686;\
            en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9\
            Firefox/3.0.1')]
        br.set_handle_robots(False)
        br.open("http://www.tatort-fundus.de/web/folgen/alpha.html")
        episoden_name = self.episoden_name

        br.find_link(text=episoden_name[0])
        br.follow_link(text=episoden_name[0])

        br.find_link(text=episoden_name)
        response = br.follow_link(text=episoden_name)
        return response.read()

    def table_soup(self, info_item):
        soup = BeautifulSoup(self.full_site)
        inhalt = soup.findAll("div", {"class": "inhalt_folgen"})
        inhalt_extract = []

        try:
            for i in inhalt:
                inhalt_extract.append(i.text)

            for i in inhalt_extract:
                if i.startswith(info_item):
                    item_position = inhalt_extract.index(i)
                else:
                    pass

            return inhalt_extract[item_position+1]

        except Exception:
            return 'Keine Angaben'

    def content_soup(self):
        soup = BeautifulSoup(self.full_site)
        inhalt = soup.findAll("div", {"id": "lauftext"})
        inhalt_extract = []

        for i in inhalt:
            inhalt_extract.append(i.text)

        return inhalt_extract

    @property
    def episode_number(self):
        soup = BeautifulSoup(self.full_site)
        number = re.findall(r"^\d\d\d", soup.title.text)
        return number[0]

    @property
    def drehbuch(self):
        return self.table_soup('Drehbuch:')

    @property
    def idee(self):
        return self.table_soup('Idee:')

    @property
    def regie(self):
        return self.table_soup('Regie:')

    @property
    def sender(self):
        return self.table_soup('Produktions- sender:')

    @property
    def firma(self):
        return self.table_soup('Produktionsfirma:')

    @property
    def drehzeit(self):
        return self.table_soup('Drehzeit:')

    @property
    def drehort(self):
        return self.table_soup('Drehort:')

    @property
    def bildformat(self):
        return self.table_soup('Bildformat:')

    @property
    def redaktion(self):
        return self.table_soup('Redaktion:')

    @property
    def erstsendung(self):
        return self.table_soup('Erstsendung:')

    @property
    def quote(self):
        return self.table_soup('Quote bei Erstsendung:')

    @property
    def actors(self):
        return self.content_soup()[1]

    @property
    def summary(self):
        return self.content_soup()[0]
