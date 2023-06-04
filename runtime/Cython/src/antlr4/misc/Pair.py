from typing import TypeVar, Generic
from . import MurmurHash

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

        elif type(obj.a) != type(self.a) or type(obj.b) != type(self.b):
            return False

        return self.a == obj.a and self.b == obj.b

    def __hash__(self) -> int:
        hash_val = MurmurHash.initialize()
        hash_val = MurmurHash.update(hash_val, self.a)
        hash_val = MurmurHash.update(hash_val, self.b)
        return MurmurHash.finish(hash_val, 2)

    def __str__(self):
        return f"({self.a}, {self.b})"