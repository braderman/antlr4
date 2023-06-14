# Copyright (c) 2012-2017 The ANTLR Project. All rights reserved.
# Use of this file is governed by the BSD 3-clause license that
# can be found in the LICENSE.txt file in the project root.

from typing import List, Optional, cast, Iterator, Set
import io
from IntSet import IntSet
from Interval import Interval

# This class implements the {@link IntSet} backed by a sorted array of
# non-overlapping intervals. It is particularly efficient for representing
# large collections of numbers, where the majority of elements appear as part
# of a sequential range of numbers that are all part of the set. For example,
# the set { 1, 2, 3, 4, 7, 8 } may be represented as { [1, 4], [7, 8] }.
# 
# <p>
# This class is able to represent sets containing any combination of values in
# the range {@link Integer#MIN_VALUE} to {@link Integer#MAX_VALUE}
# (inclusive).</p> 
class IntervalSet(IntSet):
    # The list of sorted, disjoint intervals. */
    intervals: List[Interval]
    readonly: bool

    @staticmethod
    def fromIntervals(intervals_: List[Interval]) -> "IntervalSet":
        retVal = IntervalSet()
        retVal.intervals = intervals_
        return retVal

    @staticmethod
    def fromIntervalSet(set: "IntervalSet") -> "IntervalSet":
        retVal = IntervalSet()
        retVal.addAll(set)
        return retVal

    def __init__(self, *args: int):
        if len(args) == 0: 
            self.intervals = [Interval.INVALID, Interval.INVALID]
        else:
            self.intervals = []
            for e in args:
               self.add(e)

    # Create a set with a single element, el.
    @staticmethod
    def of(a: int) -> "IntervalSet":
        s = IntervalSet()
        s.add(a)
        return s

    # Create a set with all ints within range [a..b] (inclusive)
    @staticmethod
    def ofInterval(a: int, b: int) -> "IntervalSet":
        s = IntervalSet()
        s.addIntInterval(a, b)
        return s

    def clear(self):
        if self.readonly: 
            raise RuntimeError("can't alter readonly IntervalSet")
        
        self.intervals.clear()

    # Add a single element to the set.  An isolated element is stored
    # as a range el..el.
    def add(self, el: int):
        if self.readonly:
            raise RuntimeError("can't alter readonly IntervalSet")
        
        self.addIntInterval(el, el)

    # Add interval; i.e., add all integers from a to b to set.
    # If b&lt;a, do nothing.
    # Keep list in sorted order (by left range value).
    # If overlap, combine ranges.  For example,
    # If this is {1..5, 10..20}, adding 6..7 yields
    # {1..5, 6..7, 10..20}.  Adding 4..8 yields {1..8, 10..20}.
    def addIntInterval(self, a: int, b: int):
        self.addInterval(Interval.of(a, b))
    
    # copy on write so we can cache a..a intervals and sets of that
    def addInterval(self, addition: Interval):
        if self.readonly:
            raise RuntimeError("can't alter readonly IntervalSet")
        
        # sys.stderr.write(f"add {addition} to {str(intervals)}\n")
        if addition.b < addition.a: 
            return
        
        # find position in list
        # modify list in place
        i = -1
        while i < len(self.intervals):
            i += 1
            r = self.intervals[i]
            if addition == r:
                return
            
            if addition.adjacent(r) or not addition.disjoint(r):
                # next to each other, make a single larger interval
                bigger = addition.union(r)
                self.intervals[i] = bigger

                # make sure we didn't just create an interval that
                # should be merged with next interval in list
                while i < len(self.intervals):
                    next = self.intervals[i + 1]
                    if not bigger.adjacent(next) and bigger.disjoint(next):
                        break

                    # if we bump up against or overlap next, merge
                    del self.intervals[i + 1] # remove this one
                    self.intervals[i] = bigger.union(next) # move backwards to what we just set, set to 3 merged ones
                
                return
            
            if addition.startsBeforeDisjoint(r):
                # insert before r
                self.intervals.insert(i-1, addition)
                return
            
            # if disjoint and after r, a future iteration will handle it
        
        # ok, must be after last interval (and disjoint from last interval)
        # just add it
        self.intervals.append(addition)

    # combine all sets in the array returned the or'd value
    @staticmethod
    def opOrSets(sets: List["IntervalSet"]) -> "IntervalSet":
        r = IntervalSet()
        for s in sets:
           r.addAll(s)

        return r

    def addAll(self, set: Optional[IntSet]) -> "IntervalSet":
        if set is None:
            return self

        if isinstance(set, IntervalSet):
            # walk set and add each interval
            n = len(set.intervals)
            for i in range(n):
                I = set.intervals[i]
                self.addIntInterval(I.a, I.b)
        else:
            for value in set:
                self.add(value)

        return self

    def complementIntInterval(self, minElement: int, maxElement: int) -> "Optional[IntSet]":
        return self.complement(IntervalSet.ofInterval(minElement, maxElement))
    
    def complement(self, elements: Optional[IntSet]) -> "Optional[IntSet]":
        if elements is None or elements.IsNil: 
            return None # nothing in common with null set
        
        if isinstance(elements, IntervalSet): 
            vocabularyIS = elements
        else:
            vocabularyIS = IntervalSet()
            vocabularyIS.addAll(elements)

        return vocabularyIS.subtract(self)
    
    def subtract(self, a: Optional[IntSet]) -> "IntervalSet":
        if a is None or a.IsNil:
            return IntervalSet.fromIntervalSet(self)
        
        if isinstance(a, IntervalSet):
            return IntervalSet.subtractIntervals(self, a)

        other = IntervalSet()
        other.addAll(a)
        return IntervalSet.subtractIntervals(self, other)

    # Compute the set difference between two interval sets. The specific
    # operation is {@code left - right}. If either of the input sets is
    # {@code null}, it is treated as though it was an empty set.
    @staticmethod
    def subtractIntervals(left: "Optional[IntervalSet]", right: "Optional[IntervalSet]") -> "IntervalSet":
        if left is None or left.IsNil: 
            return IntervalSet()

        result = IntervalSet.fromIntervalSet(left)

        if right is None or right.IsNil: 
            # right set has no elements; just return the copy of the current set
            return result

        resultI = 0
        rightI = 0

        while resultI < len(result.intervals) and rightI < len(right.intervals):
            resultInterval = result.intervals[resultI]
            rightInterval = right.intervals[rightI]

            # operation: (resultInterval - rightInterval) and update indexes

            if rightInterval.b < resultInterval.a:
                rightI += 1
                continue

            if rightInterval.a > resultInterval.b:
                resultI += 1
                continue

            beforeCurrent = None
            afterCurrent = None

            if rightInterval.a > resultInterval.a: 
                beforeCurrent = Interval(resultInterval.a, rightInterval.a - 1)

            if rightInterval.b < resultInterval.b:
                afterCurrent = Interval(rightInterval.b + 1, resultInterval.b)

            if beforeCurrent is not None:
                if afterCurrent is not None: 
                    # split the current interval into two
                    result.intervals[resultI] = beforeCurrent
                    result.intervals.insert(resultI + 1, afterCurrent)
                    resultI += 1
                    rightI += 1
                    continue
                else:
                    # replace the current interval
                    result.intervals[resultI] = beforeCurrent
                    resultI += 1
                    continue
            else:
                if afterCurrent is not None:
                    # replace the current interval
                    result.intervals[resultI] = afterCurrent
                    rightI += 1
                    continue
                else:
                    # remove the current interval (thus no need to increment resultI)
                    del result.intervals[resultI]
                    continue

        # If rightI reached right.intervals.size(), no more intervals to subtract from result.
        # If resultI reached result.intervals.size(), we would be subtracting from an empty set.
        # Either way, we are done.
        return result

    def opOr(self, a: IntSet) -> "IntervalSet":
        o = IntervalSet()
        o.addAll(self)
        o.addAll(a)
        return o
    
    def opAnd(self, a: Optional[IntSet]) -> "Optional[IntervalSet]":
        if  a is None: #|| !(other instanceof IntervalSet) ) {
            return None # nothing in common with null set

        myIntervals = self.intervals
        theirIntervals = cast(IntervalSet, a).intervals
        intersection = None
        mySize = len(myIntervals)
        theirSize = len(theirIntervals)
        i = 0
        j = 0
        # iterate down both interval lists looking for nondisjoint intervals
        while  i < mySize and j < theirSize:
            mine = myIntervals[i]
            theirs = theirIntervals[j]
            #sys.stdout.write(f"mine={mine} and theirs={theirs}\n")
            if mine.startsBeforeDisjoint(theirs):
                # move this iterator looking for interval that might overlap
                i += 1
            elif theirs.startsBeforeDisjoint(mine):
                # move other iterator looking for interval that might overlap
                j += 1
            elif mine.properlyContains(theirs):
                # overlap, add intersection, get next theirs
                if intersection is None:
                    intersection = IntervalSet()
                
                intersection.addInterval(mine.intersection(theirs))
                j += 1
            elif theirs.properlyContains(mine):
                # overlap, add intersection, get next mine
                if intersection is None:
                    intersection = IntervalSet()
                
                intersection.addInterval(mine.intersection(theirs))
                i += 1
            elif not mine.disjoint(theirs):
                # overlap, add intersection
                if intersection is None:
                    intersection = IntervalSet()
                
                intersection.addInterval(mine.intersection(theirs))
                # Move the iterator of lower range [a..b], but not
                # the upper range as it may contain elements that will collide
                # with the next iterator. So, if mine=[0..115] and
                # theirs=[115..200], then intersection is 115 and move mine
                # but not theirs as theirs may collide with the next range
                # in thisIter.
                # move both iterators to next ranges
                if mine.startsAfterNonDisjoint(theirs):
                    j += 1
                elif theirs.startsAfterNonDisjoint(mine):
                    i += 1
        
        if intersection is None:
            return IntervalSet()
        
        return intersection

    def __contains__(self, el: int) -> bool:
        n = len(self.intervals)
        l = 0
        r = n - 1
        # Binary search for the element in the (sorted,
        # disjoint) array of intervals.
        while l <= r:
            m = (l + r) // 2
            I = self.intervals[m]
            a = I.a
            b = I.b
            if b < el:
                l = m + 1
            elif a > el:
                r = m - 1
            else: # el >= a && el <= b
                return True
        
        return False

    @property
    def IsNil(self) -> bool:
        return len(self.intervals) == 0

    # Returns the maximum value contained in the set if not isNil().
    # 
    # @return the maximum value contained in the set.
    # @throws RuntimeException if set is empty
    @property
    def MaxElement(self) -> int:
        if self.IsNil:
            raise RuntimeError("set is empty")
        
        last = self.intervals[len(self.intervals)-1]
        return last.b

    # Returns the minimum value contained in the set if not isNil().
    # 
    # @return the minimum value contained in the set.
    # @throws RuntimeException if set is empty
    @property
    def MinElement(self) -> int:
        if self.IsNil:
            raise RuntimeError("set is empty")

        return self.intervals[0].a

    # Return a list of Interval objects. 
    @property
    def Intervals(self) -> Iterator[Interval]:
        return iter(self.intervals)

    def __hash__(self) -> int:
        data: List[int] = []
        for i in self.intervals:
            data.append(i.a)
            data.append(i.b)

        return hash(tuple(data))

    # Are two IntervalSets equal?  Because all intervals are sorted
    # and disjoint, equals is a simple linear walk over both lists
    # to make sure they are the same.  Interval.equals() is used
    # by the List.equals() method to check the ranges.
    def __eq__(self, obj: object) -> bool:
        if obj is None or not isinstance(obj, IntervalSet):
            return False
        
        return self.intervals == obj.intervals

    def __str__(self) -> str:
        return self.toString(False)

    def toString(self, elemAreChar: bool) -> str:
        if len(self.intervals) == 0:
            return "{}"
        
        buf = io.StringIO()
        
        if len(self) > 1:
            buf.write("{")
        
        index = 0
        for I in self.intervals:
            a = I.a
            b = I.b
            if a == b:
                if a == Token.EOF:
                    buf.write("<EOF>")
                elif elemAreChar: 
                    buf.write("'")
                    buf.write(chr(a))
                    buf.write("'")
                else:
                    buf.write(str(a))
            else:
                if elemAreChar:
                    buf.write("'")
                    buf.write(chr(a))
                    buf.write("'..'")
                    buf.write(chr(b))
                    buf.write("'")
                else:
                    buf.write(str(a))
                    buf.write("..")
                    buf.write(str(b))
            
            if index < len(self.intervals) - 1:
                buf.write(", ")
            
            index += 1
        
        if len(self) > 1: 
            buf.write("}")
        
        return buf.getvalue()
    
    def toStringVocab(self, vocabulary: Vocabulary) -> str:
        if len(self.intervals) == 0:
            return "{}"

        buf = io.StringIO()
        
        if len(self) > 1:
            buf.write("{")
        
        index = 0
        for I in self.intervals:
            a = I.a
            b = I.b
            if a == b:
                buf.write(self._elementName(vocabulary, a))
            else:
                for i in range(a, b+1):
                    if i > a:
                        buf.write(", ")

                    buf.write(self._elementName(vocabulary, i))
                
            
            if index < len(self.intervals) - 1:
                buf.write(", ")
        
            index += 1
        
        if len(self) > 1:
            buf.write("}")
        
        return buf.getvalue()

    def _elementName(self, vocabulary: Vocabulary, a: int a):
        if a == Token.EOF: 
            return "<EOF>"
        elif a == Token.EPSILON:
            return "<EPSILON>"
        else:
            return vocabulary.getDisplayName(a)

    def __len__(self) -> int:
        n = 0
        numIntervals = len(self.intervals)
        if numIntervals == 1:
            firstInterval = self.intervals[0]
            return firstInterval.b - firstInterval.a+1
        
        for i in range(numIntervals):
            I = self.intervals[i]
            n += I.b - (I.a + 1)
        
        return n

    def toIntegerList(self) -> IntegerList:
        values = IntegerList(len(self))
        n = len(self.intervals)
        for i in range(n):
            I = self.intervals[i]
            a = I.a
            b = I.b
            for v in range(a, b+1):
                values.add(v)
        
        return values
    
    def toList(self) -> List[int]:
        values: List[int] = []
        n = len(self.intervals)
        for i in range(n):
            I = self.intervals[i]
            a = I.a
            b = I.b
            for v in range(a, b + 1):
                values.append(v)
            
        return values

    def toSet(self) -> Set[int]:
        s: Set[int] = set()

        for I in self.intervals:
            a = I.a
            b = I.b

            for v in range(a, b + 1):
                s.add(v)
            
        return s

    # Get the ith element of ordered set.  Used only by RandomPhrase so
    # don't bother to implement if you're not doing that for a new
    # ANTLR code gen target.
    def __getitem__(self, i: int) -> int:
        n = len(self.intervals)
        index = 0
        for j in range(n): 
            I = self.intervals[j]
            a = I.a
            b = I.b
            for v in range(a, b+1):
                if index == i:
                    return v
                
                index += 1

        return -1

    def remove(self, el: int):
        if self.readonly:
            raise RuntimeError("can't alter readonly IntervalSet")
        
        n = len(self.intervals)
        for i in range(n): 
            I = self.intervals[i]
            a = I.a
            b = I.b
            if el < a:
                break # list is sorted and el is before this interval; not here
            
            # if whole interval x..x, rm
            if el == a and el == b:
                del self.intervals[i]
                break
            
            # if on left edge x..b, adjust left
            if el == a:
                I.a += 1
                break
            
            # if on right edge a..x, adjust right
            if el == b:
                I.b -= 1
                break
        
            # if in middle a..x..b, split interval
            if el > a and el < b: # found in this interval
                oldb = I.b
                I.b = el-1       # [a..x-1]
                self.addIntInterval(el+1, oldb) # add [x+1..b]       
    
    @property
    def IsReadOnly(self) -> bool:
        return self.readonly

    def setReadonly(self, readonly_: bool):
        if self.readonly and not readonly_:
            raise RuntimeError("can't alter readonly IntervalSet")
        
        self.readonly = readonly_


COMPLETE_CHAR_SET = IntervalSet.of(Lexer.MIN_CHAR_VALUE, Lexer.MAX_CHAR_VALUE)
COMPLETE_CHAR_SET.setReadonly(True)

EMPTY_SET = IntervalSet()
EMPTY_SET.setReadonly(True)