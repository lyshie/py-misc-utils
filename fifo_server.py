#!/usr/bin/env python
# -*- coding: utf-8 -*-

#=========================================================================
#
#         FILE: fifo_server.py
#
#        USAGE: ./fifo_server.py
#
#  DESCRIPTION: Use 'yield' to continuously read data from FIFO (a named pipe)
#
#      OPTIONS: ---
# REQUIREMENTS: ---
#         BUGS: ---
#        NOTES: ---
#       AUTHOR: SHIE, Li-Yi (lyshie), lyshie@mx.nthu.edu.tw
# ORGANIZATION:
#      VERSION: 1.0
#      CREATED: 2014-11-18 16:20:00
#     REVISION: ---
#=========================================================================

import os


def read_fifo(filename):
    while True:
        with open(filename, "r") as f:
            line = f.readline()
            if line:
                yield line


def main():
    fifo_name = "/tmp/server"

    if (os.path.exists(fifo_name)):
        os.remove(fifo_name)

    os.mkfifo(fifo_name)

    for line in read_fifo(fifo_name):
        line = line.rstrip("\n\r")
        if (line.lower() == "quit"):
            print("Quit!")
            break
        else:
            print("[{}]".format(line))

if __name__ == '__main__':
    main()
