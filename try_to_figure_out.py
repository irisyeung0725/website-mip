#!/usr/bin/python3

import sys
from gurobipy import *

# def add(param):
#     Cal = param + 2
#     return Cal

# def main():
#     return add(2)

# if __name__ == "__main__":
#     print(main())

input_file_path = "/Users/cassie/Dropbox/GA/Website/p0033.lp"
read_file = read(input_file_path)
read_file.optimize()

