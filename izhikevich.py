import math
import random
import numpy as np
import matplotlib.pyplot as plt

initial_v = -65.0

class INeuron:

    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

        self.v = initial_v
        self.u = self.b * self.v

    def dv_dt(self, I):
        return (0.04 * self.v**2) + (5*self.v) + 140 - self.u + I

    def du_dt(self):
        return self.a * ((self.b * self.v) - self.u)

    def update(self, I_t):
        ''' fixed timestep of 1ms to simplify '''
        self.v += self.dv_dt(I_t)
        self.u += self.du_dt()
        if self.v >= 30: # Firing threshold
            self.v = self.c
            self.u += self.d
            return True
        return False

class RSNeuron (INeuron):

    def __init__(self):
        super().__init__(0.02, 0.2, -65.0, 8.0)

class IBNeuron (INeuron):

    def __init__(self):
        super().__init__(0.02, 0.2, -55.0, 4.0)

class CHNeuron (INeuron):

    def __init__(self):
        super().__init__(0.02, 0.2, -50.0, 2.0)

class FSNeuron (INeuron):

    def __init__(self):
        super().__init__(0.1, 0.2, -65.0, 2.0)

class TCNeuron (INeuron):

    def __init__(self):
        super().__init__(0.02, 0.25, -65.0, 0.05)

class RZNeuron (INeuron):

    def __init__(self):
        super().__init__(0.1, 0.25, -65.0, 2.0)

class LTSNeuron (INeuron):

    def __init__(self):
        super().__init__(0.02, 0.25, -65.0, 2.0)


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
    return random.normalvariate(0, 1) * (5.0 if i < Ne else 2.0)

def I(t):
    return 5

def AllNeuron():
    neurons = [RSNeuron(), IBNeuron(), CHNeuron(), FSNeuron(), TCNeuron(), RZNeuron(), LTSNeuron()] 

    Vms = []
    spikes = []
    for n in neurons:
        Vms.append([n.v])
        spikes.append([0])

    ts = range(250)

    fig, ax = plt.subplots(7, 2)
    
    for t in ts[1:]:
        for i, n in enumerate(neurons):
            spike = n.update(I(t))

            Vms[i].append(n.v)
            spikes[i].append(1 if spike else 0)

    for i in range(len(neurons)):  
        ax[i][0].plot(ts, Vms[i])
        ax[i][1].plot(ts, spikes[i])
    plt.show()

def oneNeuron():
    global initial_v

    initial_v = -65.0
    neuron = RZNeuron()
    Vms = [neuron.v]
    spikes = [0]

    fig, ax = plt.subplots(1, 2)
    ts = range(250)

    for t in ts[1:]:
        spike = neuron.update(steppingI(t))
        
        Vms.append(neuron.v)
        spikes.append(1 if spike else 0)
 
    ax[0].plot(ts, Vms)
    ax[1].plot(ts, spikes)
    plt.show()

def network():

    random.seed(1)

    Ne = 900
    Ni = 100
    total = Ne + Ni

    rx = [ random.random() for _ in range(total) ]
    neurons = []
    S = []
    for i, r in enumerate(rx):
        # create neuron
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

    ts = range(1000)
    
    fires = [0] * total
    spikes = [ fires ]
    for t in ts:

        fires_t = []
        for i, n in enumerate(neurons):

            I_t = thalamicI(t, i, Ne)
            for j in range(total):
                if fires[j]: # if fired last time
                    I_t += S[j][i]
   
            spike = n.update(I_t)
            fires_t.append(1 if spike else 0)

        spikes.append(fires_t)
        fires = fires_t
    
    plt.matshow(spikes)
    plt.show()


if __name__ == "__main__":
    #oneNeuron()
    #AllNeuron()
    network()