#!/usr/bin/env python3.1
# -*- coding: utf-8 -*-
#
# Get shit from nciku.
#

import sys
from optparse import OptionParser
from urllib.request import urlopen
from urllib.parse import quote
import re
import os

CHARDIR = '/usr/local/share/hanzi'
STROKEURL = 'http://www.nciku.com/search/zh/searchorder/%s'

def charid(c):
    """Given a 汉字 character, retrieve the character ID on nciku.com. This
    allows you to easily retrieve other information (pinyin, stroke order
    diagram, etc.)"""
    return urlopen('http://www.nciku.com/search/all/%s' %
            quote(c)).geturl().split('/')[-1]

def downloadgif(c, swfpath):
    """Given a 汉字 character, download its flash stroke order file."""
    cid = charid(c)
    page = urlopen(STROKEURL % cid).read()
    swfurl = re.search(b'http:\/\/.*?\.swf', page).group(0)
    swf = urlopen(swfurl.decode('ascii')).read()
    with open(swfpath, 'wb') as out:
        out.write(swf)

def main():
    """main function for standalone usage"""
    usage = "usage: %prog [options] charstring"
    parser = OptionParser(usage=usage)

    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.print_help()
        return 2

    # do stuff
    for c in args[0]:
        swfpath = os.path.join(CHARDIR, '%s.swf' % c)
        # Download if we don't already have it
        if not os.path.isfile(swfpath):
            downloadgif(c, swfpath)

        os.system('open %s' % swfpath)

if __name__ == '__main__':
    sys.exit(main())
