class Selector:
    def __init__(self):
        self._items = None

    @property
    def items(self):
        return self._webelements

    @items.setter
    def items(self, value):
        self._items = value
