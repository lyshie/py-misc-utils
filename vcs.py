#!/usr/bin/env python
# -*- coding: utf-8 -*-

#=========================================================================
#
#         FILE: vcs.py
#
#        USAGE: ./vcs.py
#
#  DESCRIPTION: Version Control System (VCS) update utility
#
#      OPTIONS: ---
# REQUIREMENTS: ---
#         BUGS: ---
#        NOTES: ---
#       AUTHOR: SHIE, Li-Yi (lyshie), lyshie@mx.nthu.edu.tw
# ORGANIZATION:
#      VERSION: 1.0
#      CREATED: 2014-11-08 22:30:00
#     REVISION: ---
#=========================================================================

import os
import subprocess
import argparse
import logging


class VCS(object):

    def __init__(self, path):
        super(VCS, self).__init__()
        self.path = path

    def verbose(self):
        self.show_stdout = True

    def quiet(self):
        self.show_stdout = False

    def get_desc(self):
        pass

    def update(self):
        pass

    def clean(self):
        pass

    def call_process(self, cmd=None, cwd=None, show_stdout=None):
        '''idea from pip util'''
        if (show_stdout is None):
            if (hasattr(self, "show_stdout")):
                show_stdout = self.show_stdout
            else:
                show_stdout = False

        proc = subprocess.Popen(
            cmd, cwd=self.path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        out, err = proc.communicate()
        proc.wait()

        if (show_stdout and out):
            debug(out)


class GIT(VCS):

    def __init__(self, path):
        parent, git = os.path.split(path)
        if (".git" == git):
            self.path = parent
        else:
            self.path = path

    def update(self):
        self.call_process(["git", "pull"])

    def clean(self):
        self.call_process(["git", "gc"])


class SVN(VCS):

    def __init__(self, path):
        parent, svn = os.path.split(path)
        if (".svn" == svn):
            self.path = parent
        else:
            self.path = path

    def update(self):
        self.call_process(["svn", "upgrade"])
        self.call_process(["svn", "update"])


class CVS(VCS):

    def __init__(self, path):
        parent, cvs = os.path.split(path)
        if ("CVS" == cvs):
            self.path = parent
        else:
            self.path = path

    def update(self):
        self.call_process(["cvs", "update"])


def debug(msg, *args, **kwargs):
    logger = logging.getLogger(__name__)
    logger.debug(msg, *args, **kwargs)


def main():
    logging.basicConfig(level=logging.DEBUG)

    # using argument parser to get path name
    base_path = os.path.dirname(os.path.abspath(__file__))

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", default=base_path)
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    base_path = os.path.abspath(args.path)

    # filter out only dirs
    items = [os.path.join(base_path, d) for d in os.listdir(base_path)]
    dirs = filter(os.path.isdir, items)

    for d in dirs:
        git_path = os.path.join(base_path, d, ".git")
        svn_path = os.path.join(base_path, d, ".svn")
        cvs_path = os.path.join(base_path, d, "CVS")
        cur_path = os.path.join(base_path, d)

        vcs = None

        if (os.path.isdir(git_path)):
            debug("[GIT] %s" % git_path)
            vcs = GIT(git_path)
        elif (os.path.isdir(svn_path)):
            debug("[SVN] %s" % svn_path)
            vcs = SVN(svn_path)
        elif (os.path.isdir(cvs_path)):
            debug("[CVS] %s" % cvs_path)
            vcs = CVS(cvs_path)
        else:
            debug("[---] %s" % cur_path)

        if (isinstance(vcs, VCS)):
            if (args.verbose):
                vcs.verbose()
            vcs.update()
            vcs.clean()

if __name__ == '__main__':
    main()
