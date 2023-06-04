class IntStream:
    EOF: int = -1
    UNKNOWN_SOURCE_NAME: str = "<unknown>"

    def consume(self) -> None:
        raise NotImplementedError()

    def LA(self, i: int) -> int:
        raise NotImplementedError()

    def mark(self) -> int:
        raise NotImplementedError()

    def release(self, marker: int) -> None:
        raise NotImplementedError()

    def index(self) -> int:
        raise NotImplementedError()
    
    def seek(self, index: int) -> None:
        raise NotImplementedError()

    def size(self) -> int:
        raise NotImplementedError()

    def getSourceName(self) -> str:
        raise NotImplementedError()

    
    