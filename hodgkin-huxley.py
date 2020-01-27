import math
import numpy as np
import matplotlib.pyplot as plt

#### Parameter settings for resting potential of -65mV sourced from https://neurowiki.case.edu/wiki/HodgkinHuxleyModelParameters
C = 1.0 # Capacitance 
initial_Vm = -65.0 # initial potential

### Channel constants
## Leak (L)
g_max_L = 0.3 # Maximum conductance per area
E_L = -54.387 # Equilibrium potential

## Potassium (K)
g_max_K = 36.0 # Maximum conductance per area
E_K = -77.0 # Equilibrium potential

# alpha n
V1 = 100.0
V2 = -55.0
V3 = -10.0

# beta n
V4 = 0.125
V5 = -65.0
V6 = 80.0

## Sodium (Na)
g_max_Na = 120.0 # Maximum conductance per area
E_Na = 50.0 # Equilibrium potential

# alpha m
V7 = 10.0
V8 = -40.0
V9 = 10.0

# beta m 
V10 = 4.0
V11 = -65.0
V12 = 18.0

# alpha h
V13 = 0.07
V14 = -65.0
V15 = 20.0

# beta h
V16 = 1.0
V17 = -35.0
V18 = 10.0

#### Channels
class Channel:

    def __init__(self):
        self.I = 0

    def current(self, dt, Vm):
        return # used by actual channels

    def _delta(self, x, a_x, b_x):
        return (a_x * (1 - x)) - (b_x * x)

    def _toConducting(self, Vm, c1, c2, c3):
        return (-(Vm - c2)) / (c1 * (math.exp((-(Vm - c2)) / c3) - 1))

    def _toNonConducting(self, Vm, c1, c2, c3):
        return c1 * math.exp((-(Vm - c2)) / c3)

class LeakChannel (Channel) :

    def current(self, dt, Vm):
        self.I = g_max_L * (Vm - E_L)

class PotassiumChannel (Channel) :

    def __init__(self):
        super()
        self.n = 0.32 # TODO initial val?

        self.dn_dt_old = 0

    def a_n(self, Vm):
        return self._toConducting(Vm, V1, V2, V3)

    def b_n(self, Vm):
        return self._toNonConducting(Vm, V4, V5, V6)

    def current(self, dt, Vm):
        dn_dt =  self._delta(self.n, self.a_n(Vm), self.b_n(Vm))
        self.n += (self.dn_dt_old + dn_dt) * dt / 2
        self.dn_dt_old = dn_dt

        self.I = g_max_K * self.n**4 * (Vm - E_K)

class SodiumChannel (Channel) :

    def __init__(self):
        super()
        self.m = 0.05 # TODO initial val?
        self.h = 0.6 # TODO 

        self.dm_dt_old = 0
        self.dh_dt_old = 0

    def a_m(self, Vm):
        return self._toConducting(Vm, V7, V8, V9)

    def b_m(self, Vm):
        return self._toNonConducting(Vm, V10, V11, V12)

    def a_h(self, Vm):
        return self._toNonConducting(Vm, V13, V14, V15)

    def b_h(self, Vm):
       return  1.0 / (V16 * (math.exp((-(Vm - V17)) / V18) + 1))

    def current(self, dt, Vm):
        dm_dt = self._delta(self.m, self.a_m(Vm), self.b_m(Vm))
        self.m += (self.dm_dt_old + dm_dt) * dt / 2
        self.dm_dt_old = dm_dt

        dh_dt = self._delta(self.h, self.a_h(Vm), self.b_h(Vm))
        self.h += (self.dh_dt_old + dh_dt) * dt / 2
        self.dh_dt_old = dh_dt

        self.I = g_max_Na * self.m**3 * self.h * (Vm - E_Na)

#### Neuron
class HHCell:

    def __init__(self, init_potential=initial_Vm, capacitance=C):

        self.C = capacitance
        self.Vm = init_potential

        # ions channels of the cell
        self.l = LeakChannel()
        self.k = PotassiumChannel()
        self.na = SodiumChannel()

        self.dVm_dt_old = 0

    def update(self, dt, I_inj):
        '''
        dt - time since last update
        '''

        # Update channels
        self.l.current(dt, self.Vm) 
        self.k.current(dt, self.Vm)
        self.na.current(dt, self.Vm)
        
        dVm_dt = (I_inj - self.l.I - self.k.I - self.na.I) / C
        self.Vm += (self.dVm_dt_old + dVm_dt) * dt / 2
        self.dVm_dt_old = dVm_dt

def main():
    neuron = HHCell()

    Vms = [neuron.Vm]
    ts = [0]

    fig, ax = plt.subplots(1, 1)
    #

    dt = 0.01
    for i in range (10000):
        if i < 1000:
            I_inj = 0
        elif i < 5000:
            I_inj = 0
        elif i < 10000:
            I_inj = 0

        neuron.update(dt, I_inj)

        ts.append(ts[-1] + dt)
        Vms.append(neuron.Vm)
        print(neuron.Vm)

        #ax.clear()
    ax.plot(ts, Vms)
    plt.show()
        #plt.draw()
        #plt.pause(0.001)    

if __name__ == "__main__":
    main()