#!/usr/bin/env bash

python3 setup.py build_ext --inplace
cp MurmurHash.cpython-310-x86_64-linux-gnu.so ..