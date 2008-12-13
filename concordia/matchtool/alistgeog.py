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
import logging as l
from lxml import etree

import rule
import match

import alistgeogmunger as agm
import batlasidmunger as bam

ALISTGEOFN = 'data/alist-geog-filtered.xml'
BATLASFN = 'data/batlasidsformatching.xml'

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
    # we have to use a custom loader for the batlas data, because of the multiple varying number of geognames per record
    batlas = bam.loadxml(BATLASFN)
    # still need to do the following
    #
    # best rule is match map number and grid square and geogname
    rscripts = [
        [
            ('exact', agm.fieldnames.index('mapnum'),bam.fieldnames.index('mapnum')), 
            ('exact', agm.fieldnames.index('gridsquare'),bam.fieldnames.index('gridsquare')), 
            ('exact', agm.fieldnames.index('geogname'),bam.fieldnames.index('geogname'))
        ], 
    ]
    rscript = rscripts[0]
    rs = rule.RuleSet(rscript, rule.RULECONFCERT)
    g = match.match(alistgeo, batlas, rs)
    fails = []
    successes = []
    for i, q in enumerate(g):
        h = [z for z in q if z[0] == 1.0]
        if len(h) > 0:
            successes.append((alistgeo[i], h))
        else:
            fails.append(alistgeo[i])

    outxml('data/results.xml', successes)
    result = successes

    
        
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

def outxml(fn, results):

    d = etree.Element('matches')
    for a,b in results:
        rx = etree.SubElement(d, 'match')
        tx = etree.SubElement(rx, 'alistgeoitem')
        for i, c in enumerate(a):
            cx = etree.SubElement(tx, agm.fieldnames[i])
            print c
            cx.text = str(c)
        tx = etree.SubElement(rx, 'batlasmatches')
        for q in b:
            ttx = etree.SubElement(tx, 'batlasitem')
            cx = etree.SubElement(ttx, 'confidence')
            cx.text = str(q[0])
            for i, c in enumerate(q[1]):
                cx = etree.SubElement(ttx, bam.fieldnames[i])
                cx.text = unicode(c)
    f = open(fn, 'w')
    f.write(etree.tostring(d))
    f.close()
    
def loadxml(fn):
    result = []
    d = etree.parse(fn)
    root = d.getroot()
    for r in root.xpath("//*[local-name()='record']"):
        t = []
        for k in r.getchildren():
            kk = k.getchildren()
            if len(kk) == 0:
                t.append(k.text)
            else:
                s = etree.tostring(r)
                l.error("unexpected second-generation field levels found by alistgeog.loadxml() in the following record in %s; you will need to use a custom xml loader :\n\n%s" % (fn, s))
                sys.exit(2)
        result.append(tuple(t))
    return result
        
if __name__ == "__main__":
    main(sys.argv[1:])
