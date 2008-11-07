"""
errors.py
Handlers for custom exceptions
"""


# Part of idp.contentool
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


class Error(Exception):
    """Base class for exceptions in this module."""
    
    def __init__(self, reason):
        self.reason  = reason
        
    def __str__(self):
        return rep(self.reason)

class ParameterError(Error):
    """Exception raised for errors in parameters.
    
    Attributes:
        - pname: the name of the parameter
        - pval: the erroneous value of the parameter
        - reason: an explanation of why it was rejected
    """

    def __init__(self, pname, pval, reason):
        self.pname = pname
        self.pval = pval
        self.reason = reason
        
    def __str__(self):
        valstr = "'%s' is an invalid value for parameter '%s': %s" % (self.pval, self.pname, self.reason)
        return repr(valstr)

