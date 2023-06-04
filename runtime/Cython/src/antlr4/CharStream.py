from .IntStream import IntStream
from misc.Interval import Interval

class CharStream(IntStream):
    def getText(self, interval: Interval) -> str:
        raise NotImplementedError()