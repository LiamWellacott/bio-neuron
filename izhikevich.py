import math
import random
import numpy as np
import matplotlib.pyplot as plt

class INeuron:
    '''
    Implementation of Izhikevich model of a Neuron as per: https://www.izhikevich.org/publications/spikes.htm
    '''

    def __init__(self, a, b, c, d, initial_v=-65.0):
        '''
        Input
        -----
            - a: How quickly the neuron recovers (u) from firing, larger values lead to faster recovery.
            - b: Sensitivity of recovery (u) to sub action potential membrane potential (v).
            - c: Post spike reset value of membrane potential (v)
            - d: Post spike offset to recovery (u)
        '''
        self.a = a
        self.b = b
        self.c = c
        self.d = d

        self.v = initial_v
        self.u = self.b * self.v

        self.name = "INeuron" # for plotting nicely
        self.fired = False # record if an update leads to a spike (erased by next update)

    def dv_dt(self, I):
        ''' Update of membrane potential (v) as per Izhikevich defintiion '''
        return (0.04 * self.v**2) + (5*self.v) + 140 - self.u + I

    def du_dt(self):
        ''' Updae of recovery variabe (u) as per Izhikevich defintiion '''
        return self.a * ((self.b * self.v) - self.u)

    def update(self, I_t):
        ''' 
        Calculate and apply differential update equations, then check if threshold condition (spike) occurs.

        Input
        -----
            - I_t: total input current at time t
        
        Note: fixed timestep of 1ms assumed to simplify update
        '''
        # Update neuron status
        self.v += 0.5*self.dv_dt(I_t)
        self.v += 0.5*self.dv_dt(I_t)
        self.u += self.du_dt()

        # Check if Firing threshold reached
        self.fired = self.v >= 30.0
        if self.fired: 
            self.v = self.c
            self.u += self.d

### Neuron types as outlined in original work
class RSNeuron (INeuron):
    ''' Regular Spiking (RS)'''
    def __init__(self):
        super().__init__(0.02, 0.2, -65.0, 8.0)
        self.name = "Regular Spiking (RS)"

class IBNeuron (INeuron):
    ''' Intrinsically Bursting (IB)'''
    def __init__(self):
        super().__init__(0.02, 0.2, -55.0, 4.0)
        self.name = "Intrinsically Bursting (IB)"

class CHNeuron (INeuron):
    ''' Chattering (CH)'''
    def __init__(self):
        super().__init__(0.02, 0.2, -50.0, 2.0)
        self.name = "Chattering (CH)"

class FSNeuron (INeuron):
    ''' Fast Spiking (FS)'''
    def __init__(self):
        super().__init__(0.1, 0.2, -65.0, 2.0)
        self.name = "Fast Spiking (FS)"

class TCNeuron (INeuron):
    ''' Thalamo-Cortical (TC)'''
    def __init__(self, initial_v=-65.0):
        super().__init__(0.02, 0.25, -65.0, 0.05, initial_v=initial_v)
        self.name = "Thalamo-Cortical (TC)"

class RZNeuron (INeuron):
    ''' Resonator (RZ)'''
    def __init__(self):
        super().__init__(0.1, 0.25, -65.0, 2.0)
        self.name = "Resonator (RZ)"

class LTSNeuron (INeuron):
    ''' Low Threshold Spiking (LTS)'''
    def __init__(self):
        super().__init__(0.02, 0.25, -65.0, 2.0)
        self.name = "Low Threshold Spiking (LTS)"

### Some alternative "background current" functions for experimentation
def constantI(t):
    return 5

def steppingI(t):
    if t < 50:
        return 0
    if t < 150:
        return 1
    if t < 160:
        return 8
    return 3

def thalamicI(t, i, Ne):
    ''' 
    As per Izhikevich description of thalamic input current, excitatory neurons have a greater background current (5 vs 2)
    '''
    return random.normalvariate(0, 1) * (5.0 if i < Ne else 2.0)

### Modes of running model
def oneNeuron(neuron, sim_length, current_func):

    # record initial state
    Vms = [neuron.v]
    spikes = [0]

    # run for 
    ts = range(sim_length)
    for t in ts[1:]:
        neuron.update(current_func(t))
        
        if neuron.fired:
            Vms.append(30) # to normalise graph
            spikes.append(1)
        else:
            Vms.append(neuron.v)
            spikes.append(0)
 
    fig, (v_ax, spike_ax) = plt.subplots(1, 2)
    v_ax.plot(ts, Vms)
    v_ax.set_xlabel("time (ms)")
    v_ax.set_ylabel("membrane potential (v)")
    
    spike_ax.plot(ts, spikes)
    spike_ax.set_xlabel("time (ms)")
    spike_ax.set_ylabel("Spike occurrence")

    fig.suptitle(neuron.name)
    plt.show()

def allNeuron(sim_length):
    neurons = [RSNeuron(), IBNeuron(), CHNeuron(), FSNeuron(), TCNeuron(initial_v=-63.0), TCNeuron(initial_v=-87.0), RZNeuron(), LTSNeuron()] 
    for n in neurons:
        oneNeuron(n, sim_length, constantI)

def network(Ne, Ni, sim_length):

    random.seed(1) # for repeatability

    total = Ne + Ni
    rx = [ random.random() for _ in range(total) ]

    ## Create network
    neurons = [] 
    S = [] # synaptic connection strengths
    for i, r in enumerate(rx):

        # create neuron as per ranges defined in Izhikevich
        if i < Ne: # is excitatory
            neurons.append(INeuron(0.02, 0.2, -65.0 + (15.0 * (r**2)), 8.0 - (6.0 * (r**2))))
        else:
            neurons.append(INeuron(0.02 + (0.08*r), 0.25 - (0.05*r), -65.0, 2.0))

        # create connections
        ws = [ random.random() for _ in range(total)]
        for j in range(total):
            if i < Ne: # is excitatory
                ws[j] = ws[j] * 0.5 # weaker
            else:
                ws[j] = ws[j] * -1 # inhibit
        S.append(ws)

    ## Run network
    ts = range(sim_length)
    
    fires_last = [0] * total 
    spikes = [ fires_last ]
    for t in ts:

        fires_now = []
        for i, n in enumerate(neurons):

            # calculate current input current
            I_t = thalamicI(t, i, Ne)
            for j in range(total):
                if fires_last[j]:
                    I_t += S[j][i] # each fire injects some current (scaled by connection weight)

            # update neuron and record spikes
            n.update(I_t)
            fires_now.append(1 if n.fired else 0)

        spikes.append(fires_now)
        fires_last = fires_now
    
    plt.matshow(spikes)
    plt.show()


if __name__ == "__main__":
    # delete/add below as required

    #oneNeuron(RSNeuron(), 250, constantI)
    #allNeuron(250)
    network(800, 200, 500)