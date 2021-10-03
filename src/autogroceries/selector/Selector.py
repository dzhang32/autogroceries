from bs4 import BeautifulSoup


class Selector:
    def __init__(self):
        self._source = None
        self._soup = None

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, value):
        self.source = value

    @property
    def soup(self):
        return self._soup

    @soup.setter
    def soup(self, value):
        self.soup = value

    def convert_to_soup(self):
        self.soup = BeautifulSoup(self.source, "html.parser")
