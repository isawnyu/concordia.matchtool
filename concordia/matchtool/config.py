"""
config.py
Load and parse configuration files for use by other code.
"""

# Part of concordia.matchtool
#
# Copyright (c) 2008, Institute for the Study of the Ancient World, New 
# York University
#
# idp.contenttool is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import os

from ConfigParser import ConfigParser

class Config(ConfigParser):
    
    def __init__(self, cpath=None):
        ConfigParser.__init__(self)
        if not cpath:
            self.configpath = os.path.join(os.getcwd(), 'concordia', 'matchtool', 'data.cfg')
        else:
            self.configpath = os.path.abspath(cpath)
        self.read(self.configpath)
        
        
    def getVal(self, section, key):
        val = None
        s = section
        if s in self.sections():
            val = self.get(s, key)
            if '|' in val:
                s, key = val.split('|')
                val = self.getVal(s, key)
        return val

    def getVals(self, section, keys):
        vals = {}
        for k in keys:
            vals[k] = self.getVal(section, k)
        return vals
        
    def dump(self):
        print "Data Config"
        for s in self.datad.sections():
            print "section %s" % s
            print self.datad.items(s)
        