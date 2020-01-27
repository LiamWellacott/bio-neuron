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
        if self.v >= 30:
            self.v = self.c
            self.u += self.d

def I(t):
    if t > 100:
        return 10
    return 0

def main():
    neuron = INeuron(0.02, 0.2, -65, 8)

    Vms = [neuron.v]
    ts = range(1000)

    fig, ax = plt.subplots(1, 1)
    
    for t in ts[1:]:

        neuron.update(I(t))

        Vms.append(neuron.v)
        print(neuron.v)

        #ax.clear()
    ax.plot(ts, Vms)
    plt.show()
        #plt.draw()
        #plt.pause(0.001)    



if __name__ == "__main__":
    main()