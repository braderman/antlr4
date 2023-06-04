from typing import List, Optional, cast

class Interval:
    INTERVAL_POOL_MAX_VALUE: int = 1000
    INVALID: "Interval"
    cache: "List[Optional[Interval]]" = [None for _ in range(INTERVAL_POOL_MAX_VALUE+1)]
    
    a: int
    b: int

    def __init__(self, a: int, b: int):
        self.a = a
        self.b = b

    @classmethod
    def of(cls, a: int, b: int) -> "Interval":
        if a != b or a < 0 or a > cls.INTERVAL_POOL_MAX_VALUE:
            return Interval(a, b)

        if cls.cache[a] is None:
            cls.cache[a] = Interval(a, a)
            
        return cast(Interval, cls.cache[a])

    def __len__(self) -> int:
        if self.b < self.a:
            return 0

        return self.b - self.a + 1

    def __eq__(self, o: object) -> bool:
        if o is None or not isinstance(o, Interval):
            return False

        return self.a == o.a and self.b == o.b

    def __hash__(self) -> int:
        hash = 23
        hash = hash * 31 + self.a
        hash = hash * 31 + self.b
        return hash

    def startsBeforeDisjoint(self, other: "Interval") -> bool:
        return self.a < other.a and self.b < other.a

    def startsBeforeNonDisjoint(self, other: "Interval") -> bool:
        return self.a <= other.a and self.b >= other.a

    def startsAfter(self, other: "Interval") -> bool:
        return self.a > other.a

    def startsAfterDisjoint(self, other: "Interval") -> bool:
        return self.a > other.b

    def startsAfterNonDisjoint(self, other: "Interval") -> bool:
        return self.a > other.a and self.a <= other.b

    def disjoint(self, other: "Interval") -> bool:
        return self.startsBeforeDisjoint(other) or self.startsAfterDisjoint(other)

    def adjacent(self, other: "Interval") -> bool:
        return self.a == other.b + 1 or self.b == other.a - 1

    def properlyContains(self, other: "Interval") -> bool:
        return other.a >= self.a and other .b <= self.b

    def union(self, other: "Interval") -> "Interval":
        return Interval.of(min(self.a, other.a), max(self.b, other.b))

    def intersection(self, other: "Interval"):
        return Interval.of(max(self.a, other.a), min(self.b, other.b))

    def differenceNotProperlyContained(self, other: "Interval") -> "Optional[Interval]":
        diff = None

        if other.startsBeforeNonDisjoint(self):
            diff = Interval.of(max(self.a, other.b + 1), self.b)
        elif other.startsAfterNonDisjoint(self):
            diff = Interval.of(self.a, other.a - 1)

        return diff

    def __str__(self):
        return f"{self.a}..{self.b}"


Interval.INVALID = Interval(-1, -2)