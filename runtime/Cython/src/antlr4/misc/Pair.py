from typing import TypeVar, Generic, cast

A = TypeVar("A")
B = TypeVar("B")

class Pair(Generic[A, B]):
    a: A
    b: B

    def __init__(self, a: A, b: B):
        self.a = a
        self.b = b

    def __eq__(self, obj: object) -> bool:
        if obj is self:
            return True
        elif not isinstance(obj, Pair):
            return False

        objPair = cast(Pair[A, B], obj)

        if type(objPair.a) != type(self.a) or type(objPair.b) != type(self.b):
            return False

        return self.a == objPair.a and self.b == objPair.b

    def __hash__(self) -> int:
        return hash((self.a, self.b))

    def __str__(self):
        return f"({self.a}, {self.b})"