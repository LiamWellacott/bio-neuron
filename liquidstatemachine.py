import nu

import izhikevich

class ReservoirNeuron():

    def __init__(self, pos):

    def D(self, other):
        '''
        Calculate the euclidean distance between this neuron and the other
        '''
        

class LiquidStateMachine:

    def __init__(self, n_inputs, n_outputs, n_reservoir=200, reservoir_n_type=izhikevich.RSNeuron, sparsity=0.2, inhibit=0.2, column_dim=(15.0, 3.0, 3.0)):

        w_input = []
        w_reservoir = []

        w_output = []

#         Regarding connectivity structure, the probability of a synaptic connection from neuron a to neuron b (as well as that of a synaptic connection from
# neuron b to neuron a) was defined as C ·e−(D(a,b)/λ)2
# , where λ is a parameter
# that controls both the average number of connections and the average distance between neurons that are synaptically connected. We assumed that
# the 135 neurons were located on the integer points of a 15 × 3 × 3 column
# in space, where D(a, b) is the Euclidean distance between neurons a and
# b. Depending on whether a and b were excitatory (E) or inhibitory (I), the
# value of C was 0.3 (EE), 0.2 (EI), 0.4 (IE), 0.1 (II).

        for i in range(n_reservoir):



        # The input to the neural circuit was via one or several input spike trains, which diverged to inject current into 30% randomly chosen
        # “liquid neurons”. The amplitudes of the input synapses were chosen from
        # a gaussian distribution, so that each neuron in the liquid circuit received a
        # slightly different input (a form of topographic injection).

#         Mathematically,
# this liquid state xM(t) can be defined as the vector of output values at time t
# of linear filters with exponential decay (time constant 30 ms) applied to the
# spike trains emitted by the liquid neurons.


#         The current
# firing activity p(t) of the population P, that is, the fraction of neurons in P
# firing during a time bin of 20 ms, was interpreted as the analog output of
# f M at time t (one often refers to such representation of analog values by the
# current firing activity in a pool of neurons as space rate coding).

def main():
    None

if __name__ == "__main__":
    main()