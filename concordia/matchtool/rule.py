"""
rule.py
Define a class for expressing and evaluating match rules
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

import logging as l
from errors import Error, ParameterError
        
RULETYPESTRING = 1
RULETYPECASELESS = 2
RULETYPEAPPROX = 3
RULETYPENUMBER = 4
RULETYPEREGEX = 5

RULETYPEDFLT = RULETYPESTRING

ruletypes = [
    RULETYPESTRING,
    RULETYPECASELESS,
    RULETYPEAPPROX,
    RULETYPENUMBER,
    RULETYPEREGEX
    ]

ruletypedict = {
    'string' : RULETYPESTRING,
    'caseless' : RULETYPECASELESS,
    'approximate' : RULETYPEAPPROX,
    'approx' : RULETYPEAPPROX, 
    'number' : RULETYPENUMBER,
    'regex' : RULETYPEREGEX,
    're' : RULETYPEREGEX
}

RULECONFNONE = 0
RULECONFLOW = 1
RULECONFHIGH = 2
RULECONFCERT = 3

RULECONFDFLT = RULECONFCERT

class Rule():
    """
    data and methods for match rules
    """
    
    def __init__(self, indexes, type=RULETYPEDFLT, confidence=RULECONFDFLT):
        """
        initialize a rule object
        parameters:
            indexes = pair of list indexes (tuple) to use in performing match (order
                in which passed is significant, and must be observed when indexes
                are passed to self.eval())
            type = type of evaulation to perform on values (using eval() method)
            confidence = confidence value to return from eval() method when
                match is successful
        """
        
        self.idx = indexes
        if type not in ruletypes:
            raise ParameterError('type', type, 'not a valid rule type value')
        self.type = type
        self.confidence=confidence
    
    
    def eval(self, valuelists):
        """
        evaluate values at self.indexes in valuelists (order is important) according
        to this rule
        """
        
        if self.type == RULETYPESTRING:
            return self.evalstring(valuelists)
        elif self.type == RULETYPECASELESS:
            return self.evalcaseless(valuelists)
        elif self.type == RULETYPEAPPROX:
            return self.evalapprox(valuelists)
        elif self.type == RULETYPENUMBER:
            return self.evalnumber(valuelists)
        elif self.type == RULETYPEREGEX:
            return self.evalregex(valuelists)


    def evalstring(self, valuelists):
        if valuelists[0][self.idx[0]] == valuelists[1][self.idx[1]]:
            return self.confidence
        else:
            return RULECONFNONE
    
    def evalcaseless(self, valuelists):
        v1 = valuelists[0][self.idx[0]].lower()
        v2 = valuelists[1][self.idx[1]].lower()
        if v1 == v2:
            return self.confidence
        else:
            return RULECONFNONE
    
    def evalapprox(self, valuelists):
        l.warning ("rule.Rule.evalapprox() is not implemented and returns nothing")
    
    def evalnumber(self, valuelists):
        if valuelists[0][self.idx[0]] == valuelists[1][self.idx[1]]:
            return self.confidence
        else:
            return RULECONFNONE
    
    def evalregex(self, valuelists):
        l.warning("rule.Rule.evalregex() is not implemented and returns nothing")

   
class RuleError(Error):
    """Exception raised for errors in rule initialization or evaluation.
    
    Attributes:
        - pname: the name of the parameter
        - pval: the erroneous value of the parameter
        - reason: an explanation of why it was rejected
    """
    
    def __init__(self, pname, reason):
        self.pname = pname
        self.reason = reason
        
    def __str__(self):
        valstr = "'%s' is an invalid value for parameter '%s': %s" % (self.pval, self.pname, self.reason)
        return repr(valstr)
