"""
match.py
Supports list-based matching, with optional rulesets
"""

# Part of concordia.matchtool
#
# Copyright (c) 2008, Institute for the Study of the Ancient World, New 
# York University
#
# concordia.matchtool is free software: you can redistribute it and/or modify
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

import logging as l
from errors import Error, ParameterError
            
def match(these, those, rules=None):
    """
    match the next item in 'these' against items in 'those' according to
    the ruleset defined in 'rules'
    
    parameters:
    
    - 'these' and 'those': sequences containing one or more sequences 
       on which the match is to be based (the individual sequences inside 
       'these' are assumed to be ordered series of values to be used in the
       matching operation defined in 'rules')
    
    - 'rules': a sequence of rule objects whose data and methods are 
       defined in concordia.matchtool.rule. If no rule(s) are defined, then
       'match' performs a simple filter on the sequence
       
    """

    for this in these:
        if not(rules):
            results = map(lambda x: (x==this, x), those)
        else:
            results = map(lambda x: (rules(this, x), x), those)
        yield results
    