from .Gap import gap

class Clash:
    def __init__(self, clash):
        self._gap = gap(clash)

    def gap(self):
        return self._gap

    def __repr__(self):
        return str(self._gap)

