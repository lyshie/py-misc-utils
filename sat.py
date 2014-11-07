#!/usr/bin/env python
# -*- coding: utf-8 -*-

#=========================================================================
#
#         FILE: sat.py
#
#        USAGE: ./sat.py
#
#  DESCRIPTION: Package dependency resolution using SAT solver
#
#      OPTIONS: ---
# REQUIREMENTS: ---
#         BUGS: ---
#        NOTES: ---
#       AUTHOR: SHIE, Li-Yi (lyshie), lyshie@mx.nthu.edu.tw
# ORGANIZATION:
#      VERSION: 1.0
#      CREATED: 2014-11-07 15:58:39
#     REVISION: ---
#=========================================================================

import pycosat


def interpret(sol=[]):
    installed = []
    not_installed = []

    for p in sol:
        if (p > 0):
            installed.append(str(abs(p)))
        else:
            not_installed.append(str(abs(p)))

    print("\tInstalled packages: {}".format(", ".join(installed)))
    print("\tNot installed packages: {}".format(", ".join(not_installed)))


def main():
    # A requires B
    r1 = [-1, 2]

    # A requires C
    r2 = [-1, 3]

    # B conflicts C
    r3 = [-2, -3]

    # A conflicts B
    r4 = [-1, -2]

    # (-A|B) & (-A|C) & (-B|-C)
    cnf1 = [r1, r2, r3]

    # (-A|B) & (-A|-B)
    cnf2 = [r1, r4]

    print("Case 1:")
    for sol in pycosat.itersolve(cnf1):
        interpret(sol)
        print("\t----")

    print("Case 2:")
    for sol in pycosat.itersolve(cnf2):
        interpret(sol)
        print("\t----")

if __name__ == '__main__':
    main()
