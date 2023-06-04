#!/usr/bin/env python3

import sys
import capnp
import Interval_capnp

def main():
    with open(sys.argv[1], "rb") as input:
        for func in Interval_capnp.IntervalMethods.read_multiple_packed(input):
            print(func)

if __name__ == "__main__":
    main()