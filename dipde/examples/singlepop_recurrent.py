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

import matplotlib.pyplot as plt
from dipde.internals.internalpopulation import InternalPopulation
from dipde.internals.externalpopulation import ExternalPopulation
from dipde.internals.simulation import Simulation
from dipde.internals.connection import Connection as Connection

def get_simulation(dt=.001, dv=.001, tf=.2, verbose=False, update_method='exact', approx_order=None, tol=1e-8):

    # Create simulation:
    b1 = ExternalPopulation('100')
    i1 = InternalPopulation(v_min=0, v_max=.02, dv=dv, update_method=update_method, approx_order=approx_order, tol=tol)
    b1_i1 = Connection(b1, i1, 1, weights=[.005], probs=[1.], delay=0.0)
    i1_i1 = Connection(i1, i1, 1, weights=[.005], probs=[1.], delay=0.0)
    simulation = Simulation([b1, i1], [b1_i1, i1_i1], dt=dt, tf=tf, verbose=verbose)

    return simulation


def example(show=True):

    # Settings:
    dt = .0001
    dv = .0001
    tf = .2
    verbose = False
    
    update_method = 'approx'
    approx_order = None
    tol = 1e-14
    simulation = get_simulation(dt=dt, tf=tf, dv=dv, verbose=verbose, update_method=update_method, approx_order=approx_order, tol=tol)
    simulation.run()
    i1 = simulation.population_list[1]
    plt.plot(i1.t_record, i1.firing_rate_record)

    if show == True: plt.show()
    return i1.t_record, i1.firing_rate_record
    
if __name__ == "__main__": example()        # pragma: no cover
