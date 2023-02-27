import matplotlib.pyplot as plt
import numpy as np

x = np.array(range(10))
y = x**2

negative_y = y < 0
positive_y = y >= 0

plt.plot(x, y, 'bo', where=~negative_y, color='red')
plt.plot(x, y, 'bo', where=~positive_y, color='blue')

plt.show()