#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Get shit from nciku.
#

from __future__ import with_statement
import sys
from optparse import OptionParser
import urllib2, urllib
from urllib import quote
import re
import os
from io import open

# Play with the user-agent
opener = urllib2.build_opener()
opener.addheaders = [(u'User-agent', u'Mozilla/5.0')]
urlopen = opener.open

CHARDIR = u'/usr/local/share/hanzi'
STROKEURL = u'http://www.nciku.com/search/zh/searchorder/%s'

def charid(c):
    u"""Given a 汉字, retrieve the character ID on nciku.com. This
    allows you to easily retrieve other information (pinyin, stroke order
    diagram, etc.)"""
    page = urlopen('http://www.nciku.com/search/all/%s' % quote(c.encode('utf8')))
    cid = page.geturl().split(u'/')[-1]
    # If this is true, we weren't redirected. This happens when the term is
    # ambiguous. Find the _first_ link in the page and return its cid.
    if cid == quote(c.encode('utf8')):
        page = page.read()
        # Search the page for the url like: /charid/char, e.g., 1310230/妹
        return re.search(('(\d+?)">%s' % c).encode('utf-8'), page).group(1)
    else:
        return cid

def strokeurl(c):
    cid = charid(c)
    page = urlopen(STROKEURL % cid).read()
    swfurl = re.search('http:\/\/.*?\.swf', page).group(0)
    return swfurl.decode(u'ascii')

def downloadstrokes(c, swfpath):
    u"""Given a 汉字, download its flash stroke order file."""
    swfurl = strokeurl(c)
    swf = urlopen(swfurl).read()
    with open(swfpath, u'wb') as out:
        out.write(swf)

def main():
    u"""main function for standalone usage"""
    usage = u"usage: %prog [options] charstring"
    parser = OptionParser(usage=usage)

    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.print_help()
        return 2

    # do stuff
    for c in args[0].decode('utf8'):
        print(c)
        swfpath = os.path.join(CHARDIR, u'%s.swf' % c)
        # Download if we don't already have it
        if not os.path.isfile(swfpath):
            downloadstrokes(c, swfpath)

        tmp = 'open %s' % swfpath
        os.system(tmp.encode('utf8'))

if __name__ == u'__main__':
    sys.exit(main())
