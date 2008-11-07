"""
dset.py
Structured datasets for concordia.matchtool
"""

import os
import logging as l

import lxml.etree as etree

from config import Config

class DSet:

    def __init__(self, config=None):
        if not config:
            try:
                c = self.config
            except AttributeError:
                self.config = Config()
        else:
            self.config = config
    
        self.values = []
        
    def loadxml(self, filename):
    
        # read in and parse the xml file
        xroot = etree.parse(filename).getroot()

        # get rules for extracting values from config
        bname = os.path.basename(filename)
        froot, fext = os.path.splitext(bname)
        try:
            self.vxpcount = int(self.config.getVal(froot, 'vxpcount'))
        except TypeError:
            l.warning("failed to get vxpcount from config file; bname was '%s'; froot was '%s'; fext was '%s'" % (bname, froot, fext))
            raise
        
        self.vxpaths = []
        for i in range(self.vxpcount):
            self.vxpaths.append(self.config.getVal(froot, "vxpath%s" % i))
        
        # extract values from xml file
        for i in range(self.vxpcount):
            print "trying to get values from xml file (%s) with xpath = '%s'" % (bname, self.vxpaths[i])
            xvals = xroot.xpath(self.vxpaths[i])
            print "got %s values from xml file" % len(xvals)
            self.values.append([])
            for j in range(len(xvals)):
                t = self.getallxmltext(xvals[j])
                print "\tgot %s as a value from xml file" % t
                self.values[i].append(t)
                
                
                
                
    def getallxmltext(self, elem):
        text = elem.text or ""
        for e in elem:
            text = text + " " + getalltext(e)
        return text.strip()

        
        