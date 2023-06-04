#!/usr/bin/env python3

import unittest
import os
import sys

src_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src')
sys.path.insert(0,src_path)

from antlr4.misc.Pair import Pair

class PairTest(unittest.TestCase):
    def test_intPair(self):
        pair1: Pair[int, int]
        pair1 = Pair(3, 4)
        self.assertEqual(3, pair1.a)
        self.assertEqual(4, pair1.b)
        self.assertEqual("(3, 4)", str(pair1))
        self.assertEqual(pair1, pair1)

        pair2: Pair[int, int]
        pair2 = Pair(3, 4)
        self.assertEqual(pair1, pair2)
        self.assertEqual(hash(pair2), hash(pair2))

        pair3: Pair[int, int]
        pair3 = Pair(5, 6)
        self.assertNotEqual(pair1, pair3)
        self.assertNotEqual(pair2, pair3)
        self.assertNotEqual(hash(pair1), hash(pair3))
        self.assertNotEqual(hash(pair2), hash(pair3))
        self.assertNotEqual(pair1, "pair1")
        self.assertNotEqual(pair1, None)

    def test_strPair(self):
        pair1: Pair[str, str]
        pair1 = Pair("a", "b")
        self.assertEqual("a", pair1.a)
        self.assertEqual("b", pair1.b)
        self.assertEqual("(a, b)", str(pair1))
        self.assertEqual(pair1, pair1)

        pair2: Pair[str, str]
        pair2 = Pair("a", "b")
        self.assertEqual(pair1, pair2)
        self.assertEqual(hash(pair2), hash(pair2))

        pair3: Pair[str, str]
        pair3 = Pair("c", "d")
        self.assertNotEqual(pair1, pair3)
        self.assertNotEqual(pair2, pair3)
        self.assertNotEqual(hash(pair1), hash(pair3))
        self.assertNotEqual(hash(pair2), hash(pair3))

        pair4: Pair[int, int]
        pair4 = Pair(1, 5)
        self.assertNotEqual(pair1, pair4)

        pair5: Pair[int, str]
        pair5 = Pair(2, "f")
        self.assertNotEqual(pair1, pair5)

if __name__ == "__main__":
    unittest.main()