# Copyright 2013 Allen Institute
# This file is part of dipde
# dipde is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# dipde is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with dipde.  If not, see <http://www.gnu.org/licenses/>.

import sympy.parsing.sympy_parser as symp
from sympy.utilities.lambdify import lambdify
from sympy.abc import t as sym_t


class ExternalPopulation(object):
    '''External (i.e. background) source for connections to Internal Populations
    
    This class provides a background drive to internal population.  It is used as the source argument to a connection, in order to provide background drive.

    Parameters
    ----------
    firing_rate : numeric, str
        Output firing rate of the population.  If numeric type, this defines a constant background generator; if str, it is interpreted as a SymPy function with independent variable 't'.
    record : bool (default=False)
        If True, a history of the output firing rate is recorded (firing_rate_record attribute).
    **kwargs
        Any additional keyword args are stored as metadata (metadata attribute)
        
    Attributes
    ----------
    self.firing_rate_string : str
        String representation of firing_rate input parameter
    self.closure : function
        A function returns the firing rate at a given time

    '''
    
    def __init__(self, firing_rate, record=False, **kwargs):
        
        self.firing_rate_string = str(firing_rate)
        self.closure = lambdify(sym_t,symp.parse_expr(self.firing_rate_string))
        
        self.record = record
        self.type = "external"
        
        # Additional metadata:
        self.metadata = kwargs
        
    def firing_rate(self, t):
        curr_firing_rate = self.closure(t)
        if curr_firing_rate < 0:
            raise RuntimeError("negative firing rate requested: %s, at t=%s" % (self.firing_rate_string, t)) # pragma: no cover
        
        return curr_firing_rate
    
    def initialize(self):
        if self.record == True: self.initialize_firing_rate_recorder()
        
    def update(self):
        if self.record == True: self.update_firing_rate_recorder()
    
    def initialize_firing_rate_recorder(self):
        
        # Set up firing rate recorder:
        self.firing_rate_record = [self.curr_firing_rate]
        self.t_record = [0]
    
    def update_firing_rate_recorder(self):
        self.firing_rate_record.append(self.curr_firing_rate)
        self.t_record.append(self.t_record[-1]+self.simulation.dt)
    
    @property
    def curr_firing_rate(self):
        return float(self.firing_rate(self.simulation.t))