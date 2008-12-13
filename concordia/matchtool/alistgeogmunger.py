"""
alistgeogmunger.py
"""

import re
import logging as l

BAREGEX = 'Barrington Atlas (\d\d) ([A-Z]\d)'
GNAMELOC = '(\w+) (in|of) ([\w\s]*)'
GNAMEPOST = '(\w+)[\.:,;] ([\w\s]*)'

fieldnames = ['id', 'geogname', 'mapnum', 'gridsquare', 'modname', 'locdesc',  'type', 'extra']

def munge(alistgeo):
    result = []
    reba = re.compile(BAREGEX)
    regnloc = re.compile(GNAMELOC)
    regnpost = re.compile(GNAMEPOST)
    
    for a,b,c in alistgeo:
        
        # determine barrington atlas map and grid, if any
        map = None
        grid = None
        if c:
            m = reba.search(c)
            if m:
                map, grid = m.groups()
            else:
                print "munger did not find barrington atlas citation in alistgeo info:"
                print (a,b,c)
        else:
            print "munger did not find barrington atlas citation in alistgeo content:"
            print (a,b,c)

        # clean up geographic name and trap for locational and other annotations
        gname = None
        loc = None
        extra = None
        if b:
            m = regnloc.match(b)
            if m:
                gname = m.groups()[0]
                loc = ' '.join(m.groups()[1:])
            else:            
                m = regnpost.match(b)
                if m:
                    gname, extra = m.groups()
                else:
                    gname = b
        else:
            print "did not find geographic name for:"
            print (a,b,c)

        # trap for rivers and act accordingly
        river = None
        if c:
            if 'river' in c:
                river = 'river'

        # trap for modern and act accordingly
        modern = False
        if c:
            if 'modern' in c:
                modern = True
            elif extra:
                if 'modern' in extra:
                    modern = True
                
        t = (a, gname, map, grid, modern, loc, river, extra)
        result.append(t)
    return result
    