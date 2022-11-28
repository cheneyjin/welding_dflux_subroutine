import matplotlib.pyplot as plt
import numpy as np
# Input pulse parameters here:
#############################
Qmax = 2000.
Qmin = 100.
f = 20.
alpha = 0.7
#############################
t=np.arange(0,2./f,0.001)
ft = 0.
w = 2*np.pi*f
plt.ion()
for n in range(1,30,1):
    ft+=np.sin(alpha*n*np.pi)*np.cos(n*w*t)/n
    Qt = alpha*(Qmax-Qmin)+2*(Qmax-Qmin)*ft/np.pi+Qmin
    plt.clf()
    plt.plot(t,Qt)
    plt.pause(0.000000000000001)
    plt.ioff()
plt.show()
