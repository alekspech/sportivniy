import matplotlib.pyplot as plt 
import numpy as np

xs = np.linspace(start=-10,
                 stop=10,
                   num=10000)
# ys = 3*xs**2
ys = -(xs**5+25*xs) 
ys2 = xs**5+25*xs 
plt.plot(xs, ys, '--')
plt.plot(xs, ys2, 'r')
plt.grid()
plt.show()
print(xs)
