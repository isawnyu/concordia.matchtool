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
from difflib import SequenceMatcher
        
RULETYPEEXACT = 1
RULETYPECASELESS = 2
RULETYPEAPPROX = 3

ruletypedict = {
    'exact' : RULETYPEEXACT,
    'caseless' : RULETYPECASELESS,
    'approximate' : RULETYPEAPPROX,
    'approx' : RULETYPEAPPROX, 
}

RULECONFNONE = 0.0
RULECONFLOW = 0.3
RULECONFHIGH = 0.7
RULECONFCERT = 1.0

ruleconfdict = {
    'none' : RULECONFNONE,
    'low' : RULECONFLOW,
    'high' : RULECONFHIGH,
    'ruleconfcert' : RULECONFCERT
}

RULECONFDFLT = RULECONFCERT

class Rule():
    """
    ancestor class to hold data and methods for match rules
    
    has two methods: init and match
    
    this version of the class, when called, only returns True
    """
    
    def __init__(self):
        """
        initialize a rule object
        """
        pass
        
    def __call__(self):
        """
        evaluate the function
        """
        return True
        
        
class RuleExact(Rule):
    """
    This rule compares two values (passed to __call__()) and returns the boolean
    result of an exact comparison
    """
        
    def __call__(self, this, that):
        """
        evaluate this rule by exactly comparing a value in each of the two records
        (index indicated by self.                
        """
        
        return this == that
        

class RuleCaseless(Rule):
    """
    This rule compares two values (assumed to be strings and passed to __call__())
    converts both of them to lowercase and returns the result of an exact comparison
    between these lowercase versions
    """

    def __call__(self, this, that):
        x = this.lower()
        y = that.lower()
        return x == y
        
        
class RuleApprox(Rule):
    """
    This rule compares two values using difflib.Sequencematcher. __init__ takes an
    optional parameter called "ratio", which is used by __call__() to judge the 
    "goodness" of the match between the two values. If it is not supplied, 0.6 is
    taken as the default. If Sequencematcher returns a ratio greater than the 
    ratio value passed to RuleApprox._init_() then __call__() returns True, otherwise
    False.
    """

    def __init__(self, ratio=0.6):
        self.goodratio = ratio
        self.realratio = -1
        
    def __call__(self, this, that):
        result = False
        sm = SequenceMatcher(None, this, that)
        self.realratio = sm.real_quick_ratio()
        if self.realratio >= self.goodratio:
            self.realratio = sm.ratio()
            if self.realratio >= self.goodratio:
                result = True
        return result
        
    
        
        
class RuleSet():
    """
    This class defines an ordered collection of rule objects and a confidence
    value to return if they all evaluate to True. 
    
    The list of rule objects is defined by a script that is passed to __init__(): 
    a list of tuples in which each tuple has three parts: a rule type string 
    (matching a key in ruletypedict), and then two indexes. The first index
    indicates which value in the "this" parameter later passed to __call__()
    should be used in the comparison. The second index indicates which
    value in the "that" parameter should be used in the comparison. This
    permits a single ruleset to contain rules that operate on different
    parts of the data records passed to the ruleset. See tests/rule.txt
    for some example usages.
    """
    
    def __init__(self, rscript, confidence):
    
        
        self.confidence = confidence
        self.rules = []
        
        for rs in rscript:
            rstr = None
            i = None
            j = None
            param = None
            try:
                rtstr, i, j, param = rs
            except:
                rtstr, i, j = rs
            try:
                rt = ruletypedict[rtstr]
            except KeyError:
                raise ParameterError('rt', rt, "must be one of: %s" % ' | '.join(ruletypedict.keys()))
            if rt == RULETYPEEXACT:
                r = RuleExact()
            elif rt == RULETYPECASELESS:
                r = RuleCaseless()
            elif rt == RULETYPEAPPROX:
                r = RuleApprox(param)
            else:
                raise ParameterError('rt', rt, "must be one of: %s" % ' | '.join(ruletypedict.keys())) 
            self.rules.append((r, i, j))
            
    def __call__(self, this, that):
        for eval, i, j in self.rules:
            if eval(this[i], that[j]):
                pass
            else:
                return RULECONFNONE
        return self.confidence
            
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
