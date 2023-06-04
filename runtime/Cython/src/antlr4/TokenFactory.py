from typing import TypeVar, Generic, Union
from misc.Pair import Pair
from .CharStream import CharStream
from .Token import Token
from .TokenSource import TokenSource

Symbol = TypeVar("Symbol", bound=Token)
SourceType = Pair[TokenSource, CharStream]

class TokenFactory(Generic[Symbol]):
    def _create1(self, source: SourceType, type: int, text: str, channel: int, start: int, stop: int, line: int, 
        charPositionInLine: int) -> Symbol:
        raise NotImplementedError()

    def _create2(self, type: int, text: str) -> Symbol:
        raise NotImplementedError()

    def create(self, sourceOrType: Union[SourceType, int], typeOrText: Union[int, str], text: str, channel: int, 
        start: int, stop: int, line: int, charPositionInLine: int) -> Symbol:
        if isinstance(sourceOrType, Pair) and isinstance(typeOrText, int):
            return self._create1(sourceOrType, typeOrText, text, channel, start, stop, line, charPositionInLine)
        elif isinstance(sourceOrType, int) and isinstance(typeOrText, str):
            return self._create2(sourceOrType, typeOrText)
        else:
            raise RuntimeError("TokenFactory.create() called with unrecognized types")