from .Token import Token
from .CharStream import CharStream
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .TokenFactory import TokenFactory

class TokenSource:
    def nextToken(self) -> Token:
        raise NotImplementedError()

    def getLine(self) -> int:
        raise NotImplementedError()

    def getCharPositionInLine(self) -> int:
        raise NotImplementedError()

    def getInputStream(self) -> CharStream:
        raise NotImplementedError()

    def getSourceName(self) -> str:
        raise NotImplementedError()

    def setTokenFactory(self, factory: TokenFactory[Any]) -> None:
        raise NotImplementedError()

    def getTokenFactory(self) -> TokenFactory[Any]:
        raise NotImplementedError()

