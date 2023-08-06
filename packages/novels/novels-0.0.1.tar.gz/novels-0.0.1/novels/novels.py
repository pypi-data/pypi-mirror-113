import sys
import argparse
import os
import json
import yaml
import xmltodict
import re
import traceback
import time
import random
import string
from functools import partial
from collections import (deque,defaultdict)

def novels_main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--infile", dest="infile", help="input file")
    parser.add_argument("-t", "--title", dest="title", default=None, help="novel title")
    parser.add_argument("-n", "--number", dest="number", type=int, default=50, help="how many chapters to retrieve")
    parser.add_argument("-p", "--page", dest="page", default=None, help="Novel index page",)
    parser.add_argument("-X", "--debug", dest="debug", action="count", default=False, help="debug mode",)
    xargs = parser.parse_args()
    print("novel!!")



if __name__ == "__main__" :
    novels_main()
