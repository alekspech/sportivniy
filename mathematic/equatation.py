from mathematic.draw_tools import make_axes
import numpy as np
import matplotlib.pyplot as plt

'''
2x + 3 = 11 дано 
2x + 3 = 0 проверим при каком х левая часть имеет у равный 0
2x = -3
x = -1.5

x = 4     чтд
y = 2x + 3
при x = 0
y = 3
при x = 1
y = 5
'''
xs = np.linspace(-2, 8, 20)
y1 = 2*xs + 3
y2 = np.full_like(xs, 11) 
y3 = -2 * xs - 1 
print(y2)
print(y1)
fig, ax = make_axes(xlim=(-15, 15), ylim=(-15, 15))
ax.plot(xs, y1, label = 'y = 2x + 3')
ax.plot(xs, y2, label = 'y = 11')
ax.plot(xs, y3, label='y = -2x - 1')
ax.legend(loc='upper left')
plt.show()