#!/usr/bin/python
"""
python alistgeo.py data/alist-geog-filtered.xml data/batlasidmatchstuff.xml

options:

-h, --help = get usage message
-o path/to/file.txt, --outfile=path/to/file.txt = where to put results (otherwise
to stdout)
"""

import getopt
import sys
import rule
import match

from lxml import etree
import alistgeogmunger as agm

ALISTGEOFN = 'data/alist-geog-filtered.xml'
BATLASFN = 'data/batlas.xml'

def main(argv):
    """
    run the conversion
    """
    
    try:
        opts, args = getopt.getopt(argv, "ho:", ['help', 'outfile='])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)
        
    if len(args) != 0:
        print "incorrect number of arguments (%s)" % len(args)
        usage()
        sys.exit(2)
        
    outfile = None
    for o, a in opts:
        if o == '-h':
            print __doc__
            sys.exit()
        elif o in ('-o', '--outfile'):
            outfile = a
        else:
            assert False, "unhandled option (%s)" % o
            
    alistgeo = loadxml(ALISTGEOFN)
    alistgeo = agm.munge(alistgeo)
    # still need to do the following
    #batlas = loadxml(BATLASFN)
    # build a ruleset
    # use match.match() to loop through possible matches like for m in match.match(alistgeo, batlas, myruleset)
    # might have to make second or third passes with different rulesets for things that fail to match in earlier attempts
    result  = alistgeo
        
    if outfile:
        f = open(outfile, 'w')
        f.write(result)
        f.close()
    else:
        print result
        
def usage():
    print __doc__
        
def convert(these, those):
    pass    
    # build ruleset
    # run matches and report

def loadxml(fn):
    result = []
    d = etree.parse(fn)
    root = d.getroot()
    for r in root.xpath("//*[local-name()='record']"):
        t = []
        for k in r.getchildren():
            t.append(k.text)
        result.append(tuple(t))
    return result
        
if __name__ == "__main__":
    main(sys.argv[1:])
