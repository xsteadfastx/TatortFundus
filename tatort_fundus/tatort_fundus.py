import re
import requests
from bs4 import BeautifulSoup


class Episode(object):
    def __init__(self, episoden_name):
        self.episoden_name = episoden_name
        self.episoden_name = self.episoden_name.decode('utf-8')
        self.URL = 'http://www.tatort-fundus.de/web/folgen/alpha.html'
        self.full_site = self._browse()
        self.soup = BeautifulSoup(self.full_site)

    def _get_link(self, name, URL):
        """ searches for a string and returns the right url for it """
        r = requests.get(URL)
        soup = BeautifulSoup(r.text)
        links = soup.findAll('div', 'folgen_suche')
        for i in links:
            if name in i.text:
                return i.a['href']
            else:
                pass

    def _browse(self):
        """ looks for the the first letter in episoden_name and gets the right
        page """
        start_letter_page = self._get_link(self.episoden_name[0], self.URL)
        letter_page = self._get_link(self.episoden_name, start_letter_page)
        r = requests.get(letter_page)
        return r.text

    def _table_soup(self, info_item):
        """ soups the info box """
        soup = self.soup
        inhalt = soup.findAll('div', {'class': 'inhalt_folgen'})
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

    def _content_soup(self):
        """ soups the rest of the page informations """
        soup = self.soup
        inhalt = soup.findAll('div', {'id': 'lauftext'})
        inhalt_extract = []

        for i in inhalt:
            inhalt_extract.append(i.text)

        return inhalt_extract

    def _actors_soup(self):
        """ extracts the actors and put it into a list """
        soup = self.soup
        inhalt = soup.findAll('div', {'id': 'lauftext'})
        inhalt_extract = []

        for i in inhalt:
            inhalt_extract.append(i)

        actors_list = []

        for i in inhalt_extract[1].findAll('b'):
            actors_list.append(i.text)

        return actors_list

    @property
    def episode_number(self):
        soup = BeautifulSoup(self.full_site)
        number = re.findall(r"^\d\d\d", soup.title.text)
        return number[0]

    @property
    def drehbuch(self):
        return self._table_soup('Drehbuch:')

    @property
    def idee(self):
        return self._table_soup('Idee:')

    @property
    def regie(self):
        return self._table_soup('Regie:')

    @property
    def sender(self):
        return self._table_soup('Produktions- sender:')

    @property
    def firma(self):
        return self._table_soup('Produktionsfirma:')

    @property
    def drehzeit(self):
        return self._table_soup('Drehzeit:')

    @property
    def drehort(self):
        return self._table_soup('Drehort:')

    @property
    def bildformat(self):
        return self._table_soup('Bildformat:')

    @property
    def redaktion(self):
        return self._table_soup('Redaktion:')

    @property
    def erstsendung(self):
        return self._table_soup('Erstsendung:')

    @property
    def quote(self):
        return self._table_soup('Quote bei Erstsendung:')

    @property
    def actors(self):
        """ returns list of actors """
        return self._actors_soup()

    @property
    def summary(self):
        return self._content_soup()[0]


class Ermittler(object):
    def __init__(self):
        self.URL = 'http://www.tatort-fundus.de/web/ermittler/alpha.html'

    def _get_link(self, name, URL):
        r = requests.get(URL)
        soup = BeautifulSoup(r.text)
        links = soup.findAll('a', 'internal-link')
        for i in links:
            if name in i.text:
                return 'http://www.tatort-fundus.de/web/%s' % i['href']
            else:
                pass

    def _ermittler_soup(self, ermittler):
        ermittler_url = self._get_link(ermittler, self.URL)
        r = requests.get(ermittler_url)
        return BeautifulSoup(r.text)

    def folgen(self, ermittler):
        """ extract content from table """
        ermittler = ermittler.decode('utf-8')
        extract_episodes = self._ermittler_soup(ermittler).findAll('td',
                                                                   'inhalt_folgen')

        """ extract text and fill a list """
        episodes_raw = []
        for i in extract_episodes:
            episodes_raw.append(i.text)

        """ create and fill list """
        episodes_raw = iter(episodes_raw)
        episodes_data = []
        for i in zip(episodes_raw, episodes_raw, episodes_raw, episodes_raw):
            episodes_data.append(i)

        """ returns list """
        return episodes_data


def ermittler_uebersicht():
    """ creates list of ermittler """
    URL = 'http://www.tatort-fundus.de/web/ermittler/alpha.html'
    r = requests.get(URL)
    soup = BeautifulSoup(r.text)
    links = soup.findAll('a', 'internal-link')
    ermittler = []
    for i in links[:-5]:
        ermittler.append(i.text.strip())

    """ makes ermittler a set, put into a list, get rid of doubles
    and sort it """
    return sorted(filter(None, list(set(ermittler))))


def naechste_erstsendungen():
    """creates list of next first aired episodes"""
    URL = 'http://www.tatort-fundus.de/web/folgen/die-naechsten-erstsendungen.html'
    r = requests.get(URL)
    soup = BeautifulSoup(r.text)

    """ get the table data and put just the text into a list"""
    table = soup.findAll('div', 'inhalt_folgen')
    raw_table_data = []
    for i in table:
        raw_table_data.append(i.text)

    """convert raw_table_data to iter and zip a list with 5 items in a row
    together"""
    raw_table_data = iter(raw_table_data)
    data = []
    for i in zip(raw_table_data, raw_table_data, raw_table_data,
                 raw_table_data, raw_table_data):
        data.append(i)

    """return list"""
    return data


def naechste_wiederholungen():
    """creates a list of next aired old episodes"""
    URL = 'http://www.tatort-fundus.de/web/folgen/wiederholungen.html'
    r = requests.get(URL)
    soup = BeautifulSoup(r.text)

    table = soup.findAll('td', 'wh_tabelle')
    raw_table_data = []
    for i in table:
        raw_table_data.append(i.text.strip('\n'))

    """convert raw_table_data to iter and zip a list with 5 items in a row
    together"""
    raw_table_data = iter(raw_table_data)
    data = []
    for i in zip(raw_table_data, raw_table_data, raw_table_data,
                 raw_table_data, raw_table_data):
        data.append(i)

    """delete first item in list"""
    del data[0]

    """return list"""
    return data
