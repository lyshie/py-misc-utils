#!/usr/bin/env python
# -*- coding: utf-8 -*-

#=========================================================================
#
#         FILE: mysql_backup_rotate.py
#
#        USAGE: ./mysql_backup_rotate.py
#
#  DESCRIPTION: MySQL backup and rotate tool
#
#      OPTIONS: ---
# REQUIREMENTS: ---
#         BUGS: ---
#        NOTES: ---
#       AUTHOR: SHIE, Li-Yi (lyshie), lyshie@mail.nsysu.edu.tw
# ORGANIZATION:
#      VERSION: 1.0
#      CREATED: 2015-01-29 21:17:33
#     REVISION: ---
#=========================================================================

import os
import subprocess
import re
import time


def main():
    # filename => /tmp/mysqldump_20150129_211037.lzo'
    path = "/tmp"
    suffix = time.strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(path, "mysqldump_%s.lzo" % (suffix))

    # mysqldump
    subprocess.call(
        "/usr/bin/mysqldump --all-databases | lzop --best | pv > '%s'" % (filename), shell=True)

    # list files in '/tmp'
    files = [f for f in os.listdir(
        path) if os.path.isfile(os.path.join(path, f))]

    # filter out 'mysqldump_12345678_123456.lzo'
    pattern = re.compile(r"mysqldump_\d+_\d+\.lzo")
    files = [os.path.join(path, f) for f in files if pattern.match(f)]

    # order by 'mtime' desc
    files.sort(key=lambda x: os.stat(x).st_mtime, reverse=True)

    # unlink old files
    keep = 3
    for i, f in enumerate(files):
        if i < keep:
            pass
        else:
            os.unlink(f)
            print("Removed old file '%s'" % (f))

if __name__ == '__main__':
    main()
