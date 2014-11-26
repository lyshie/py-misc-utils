#!/usr/bin/env python
# -*- coding: utf-8 -*-

#=========================================================================
#
#         FILE: bookmark.py
#
#        USAGE: ./bookmark.py -f [places.sqlite]
#
#  DESCRIPTION: Dump the bookmarks from Firefox database (SQLite, ORM)
#
#      OPTIONS: ---
# REQUIREMENTS: ---
#         BUGS: ---
#        NOTES: ---
#       AUTHOR: SHIE, Li-Yi (lyshie), lyshie@mx.nthu.edu.tw
# ORGANIZATION:
#      VERSION: 1.0
#      CREATED: 2014-11-26 11:50:00
#     REVISION: ---
#=========================================================================

from __future__ import print_function
import os
import argparse

from sqlalchemy import Column, String, Integer, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Place(Base):
    __tablename__ = "moz_places"

    id = Column(Integer, primary_key=True)
    url = Column(String)
    title = Column(String)


class Bookmark(Base):
    __tablename__ = "moz_bookmarks"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    parent = Column(Integer)

    # relationship
    fk = Column(Integer, ForeignKey(Place.id))
    place = relationship(Place)


def get_db_file(location):
    db_file = ""

    if (location):
        basename = os.path.basename(location)
        if basename == "places.sqlite":
            db_file = os.path.abspath(location)
        else:
            db_file = os.path.abspath(os.path.join(location, "places.sqlite"))
    else:
        parent = os.path.expanduser("~/.mozilla/firefox")
        for d in os.listdir(parent):
            f = os.path.join(parent, d, "places.sqlite")
            if (os.path.isfile(f)):
                db_file = f
                break

    return db_file


def main():
    # set file location
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help="file or path")
    args = parser.parse_args()
    db_file = get_db_file(args.file)

    # database init
    engine = create_engine("sqlite:///{}".format(db_file))
    session = sessionmaker()
    session.configure(bind=engine)

    # query
    s = session()
    for b in s.query(Bookmark).filter(Bookmark.fk != None).all():
        title = u"{}".format(b.title)
        url = u"{}".format(b.place.url)

        title = title.replace("\x0b", "")

        # output UTF-8
        print(u"{}".format(title).encode("UTF-8"))
        print(u"    => {}".format(url).encode("UTF-8"))

if __name__ == '__main__':
    main()
