from .IntStream import IntStream
from .CharStream import CharStream
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .TokenSource import TokenSource

class Token:
    INVALID_TYPE: int = 0
    EPSILON: int = -2
    MIN_USER_TOKEN_TYPE: int = 1
    EOF: int = IntStream.EOF
    DEFAULT_CHANNEL: int = 0
    HIDDEN_CHANNEL: int = 1
    MIN_USER_CHANNEL_VALUE: int = 2

    def getText(self) -> str:
        raise NotImplementedError()

    def getType(self) -> int:
        raise NotImplementedError()

    def getLine(self) -> int:
        raise NotImplementedError()

    def getCharPositionInLine(self) -> int:
        raise NotImplementedError()

    def getChannel(self) -> int:
        raise NotImplementedError()

    def getTokenIndex(self) -> int:
        raise NotImplementedError()

    def getStartIndex(self) -> int:
        raise NotImplementedError()

    def getStopIndex(self) -> int:
        raise NotImplementedError()

    def getTokenSource(self) -> TokenSource:
        raise NotImplementedError()

    def getInputStream(self) -> CharStream:
        raise NotImplementedError()

    