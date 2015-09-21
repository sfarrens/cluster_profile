import math
import numpy as np
from functions import cosmo

data = np.genfromtxt("h_ab", dtype="float", unpack = True)

z = data[0,:]
m70 = data[1,:]

H0_70 = 70.0
H0_100 = 100.0

m100 = m70 + 5 * np.log10(H0_70 / H0_100)

for i in range(len(z)):
    print z[i], m100[i]
