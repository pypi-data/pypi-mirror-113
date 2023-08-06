from ._gap import gap

class Clash:
    def __init__(self, clash):
        self._gap = gap(clash)

    def gap(self):
        return self._gap

    def __repr__(self):
        return str(self._gap)

    def __str__(self):
        return str(self._gap)
