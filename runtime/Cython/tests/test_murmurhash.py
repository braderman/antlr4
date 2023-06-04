#!/usr/bin/env python3

import unittest
import capnp
import os
import sys
import MurmurHash_capnp

src_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src')
sys.path.insert(0,src_path)

import antlr4.misc.MurmurHash as MurmurHash


class MurmurHashTest(unittest.TestCase):
    def test_update(self):
        with open("resources/murmurhash.dat", "rb") as input:
            i = 0
            for func in MurmurHash_capnp.MurmurHashMethods.read_multiple_packed(input):
                which = func.which()
                if which == "updateInt":
                    updateInt = func.updateInt
                    #print(f"Case #{i} update: {updateInt.input.hash}, {updateInt.input.value}")
                    output = MurmurHash._update(updateInt.input.hash, updateInt.input.value)
                    self.assertEqual(updateInt.output, output)
                    i += 1
                elif which == "finish":
                    finish = func.finish
                    #print(f"Case #{i} finish: {finish.input.hash}, {finish.input.numberOfWords}")
                    output = MurmurHash.finish(finish.input.hash, finish.input.numberOfWords)
                    self.assertEqual(finish.output, output)
                    i += 1

                #if i == 100:
                #    break


if __name__ == "__main__":
    unittest.main()