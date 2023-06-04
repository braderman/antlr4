#!/usr/bin/env python3

import unittest
import capnp
import os
import sys
import Interval_capnp

src_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src')
sys.path.insert(0,src_path)

from antlr4.misc.Interval import Interval


class IntervalTest(unittest.TestCase):
    def test_set(self):
        funcs = set()

        with open("resources/interval2.dat", "rb") as input:
            for func in Interval_capnp.IntervalMethods.read_multiple_packed(input):
                funcs.add(func.which())

        print(funcs)        

    def test1(self):
        with open("resources/interval.dat", "rb") as input:
            for func in Interval_capnp.IntervalMethods.read_multiple_packed(input):
                which = func.which()
                if which == "intervalOf":
                    f = func.intervalOf
                    output = Interval.of(f.input.a, f.input.b)
                    self.assertEqual(Interval.of(f.output.a, f.output.b), output)
                elif which == "adjacent":
                    f = func.adjacent
                    state = Interval(f.state.a, f.state.b)
                    input = Interval(f.input.a, f.input.b)
                    output = state.adjacent(input)
                    self.assertEqual(f.output, output)
                elif which == "startsBeforeDisjoint":
                    f = func.startsBeforeDisjoint
                    state = Interval(f.state.a, f.state.b)
                    input = Interval(f.input.a, f.input.b)
                    output = state.startsBeforeDisjoint(input)
                    self.assertEqual(f.output, output)
                elif which == "startsAfterDisjoint":
                    f = func.startsAfterDisjoint
                    state = Interval(f.state.a, f.state.b)
                    input = Interval(f.input.a, f.input.b)
                    output = state.startsAfterDisjoint(input)
                    self.assertEqual(f.output, output)
                elif which == "disjoint":
                    f = func.disjoint
                    state = Interval(f.state.a, f.state.b)
                    input = Interval(f.input.a, f.input.b)
                    output = state.disjoint(input)
                    self.assertEqual(f.output, output)
                elif which == "methUnion":
                    f = func.methUnion
                    state = Interval(f.state.a, f.state.b)
                    input = Interval(f.input.a, f.input.b)
                    output = state.union(input)
                    self.assertEqual(Interval(f.output.a, f.output.b), output)
    
    def test2(self):
        with open("resources/interval2.dat", "rb") as input:
            for func in Interval_capnp.IntervalMethods.read_multiple_packed(input):
                which = func.which()
                if which == "length":
                    f = func.length
                    output = len(Interval(f.state.a, f.state.b))
                    self.assertEqual(f.output, output)
                elif which == "startsAfterNonDisjoint":
                    f = func.startsAfterNonDisjoint
                    state = Interval(f.state.a, f.state.b)
                    input = Interval(f.input.a, f.input.b)
                    output = state.startsAfterNonDisjoint(input)
                    self.assertEqual(f.output, output)                
                elif which == "properlyContains":
                    f = func.properlyContains
                    state = Interval(f.state.a, f.state.b)
                    input = Interval(f.input.a, f.input.b)
                    output = state.properlyContains(input)
                    self.assertEqual(f.output, output)                
                elif which == "intersection":
                    f = func.intersection
                    state = Interval(f.state.a, f.state.b)
                    input = Interval(f.input.a, f.input.b)
                    output = state.intersection(input)
                    self.assertEqual(Interval(f.output.a, f.output.b), output)


if __name__ == "__main__":
    unittest.main()