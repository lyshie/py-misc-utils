#!/usr/bin/env python
# -*- coding: utf-8 -*-

#=========================================================================
#
#         FILE: mysql_backup_rotate.py
#
#        USAGE: ./mysql_backup_rotate.py --help
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
import argparse
import pipes
import logging
import logging.handlers


def list_files(path, pattern, sorted=True):
    files = [f for f in os.listdir(
        path) if os.path.isfile(os.path.join(path, f))]

    # filter out 'mysqldump_12345678_123456.lzo'
    if pattern:
        files = [os.path.join(path, f) for f in files if pattern.match(f)]

    # order by 'mtime' desc
    if sorted:
        files.sort(key=lambda x: os.stat(x).st_mtime, reverse=True)

    return files


def rotate(path, pattern, number=0):
    unlinked_files = []

    files = list_files(path, pattern, sorted=True)
    if number > 0:
        for i, f in enumerate(files):
            if i < number:
                pass
            else:
                unlinked_files.append(f)
                os.unlink(f)

    return unlinked_files


def backup_mysql(path, filename, table, compress=True, timeout=0):
    abs_filename = os.path.join(path, filename)

    arg = "--all-databases"
    if table != "ALL":
        arg = "--database %s" % (pipes.quote(table))

    if compress:
        cmd = "/usr/bin/mysqldump %s | lzop --best | pv > %s" % (
            arg, pipes.quote(abs_filename))
    else:
        cmd = "/usr/bin/mysqldump %s | pv > %s" % (
            arg, pipes.quote(abs_filename))

    if subprocess.call(cmd, shell=True) == 0:
        return abs_filename
    else:
        return None


def main():
    # logging
    logger = logging.getLogger(os.path.basename(__file__))
    logger.setLevel(logging.DEBUG)

    handler = logging.handlers.SysLogHandler(address="/dev/log")
    formatter = logging.Formatter(
        '%(name)s[%(process)d]: [%(levelname)s] %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    # parse argument
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--type", type=str, default="hourly")
    parser.add_argument("-n", "--number", type=int, default=0)
    parser.add_argument("--table", type=str, default="ALL")
    args = parser.parse_args()

    # filename => /tmp/mysqldump_20150129_211037.lzo'
    path = "/tmp"
    suffix = time.strftime("%Y%m%d_%H%M%S")
    filename = "%s_%s_mysqldump_%s.lzo" % (args.type, args.table, suffix)
    pattern = re.compile(
        r"%s_%s_mysqldump_\d{8}_\d{6}\.lzo" % (re.escape(args.type), re.escape(args.table)))

    # rotate only when successfully backup
    ret_file = backup_mysql(path, filename, table=args.table)
    if ret_file:
        logger.info("Backup file: %s" % (ret_file))

        unlinked_files = rotate(path, pattern, number=args.number)
        for f in unlinked_files:
            logger.info("Unlink file: %s" % (f))

if __name__ == '__main__':
    main()
