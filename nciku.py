#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Get shit from nciku.
#

import sys
from optparse import OptionParser
import urllib.request
from urllib.parse import quote
import re
import os

# Play with the user-agent
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
urlopen = opener.open

CHARDIR = '/usr/local/share/hanzi'
STROKEURL = 'http://www.nciku.com/search/zh/searchorder/%s'

def charid(c):
    """Given a 汉字, retrieve the character ID on nciku.com. This
    allows you to easily retrieve other information (pinyin, stroke order
    diagram, etc.)"""
    page = urlopen('http://www.nciku.com/search/all/%s' % quote(c))
    cid = page.geturl().split('/')[-1]
    # If this is true, we weren't redirected. This happens when the term is
    # ambiguous. Find the _first_ link in the page and return its cid.
    if cid == quote(c):
        page = page.read()
        # Search the page for the url like: /charid/char, e.g., 1310230/妹
        return re.search(bytes('(\d+?)">%s' % c, 'utf-8'), page).group(1).decode('ascii')
    else:
        return cid

def strokeurl(c):
    cid = charid(c)
    page = urlopen(STROKEURL % cid).read()
    swfurl = re.search(b'http:\/\/.*?\.swf', page).group(0)
    return swfurl

def downloadstrokes(c, swfpath):
    """Given a 汉字, download its flash stroke order file."""
    swfurl = strokeurl(c)
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
            downloadstrokes(c, swfpath)

        os.system('open %s' % swfpath)

if __name__ == '__main__':
    sys.exit(main())
