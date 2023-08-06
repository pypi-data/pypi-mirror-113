
import matplotlib.pyplot as plt

plt.plot([0.001, 0.005, 0.01, 0.1], [14.8, 11.4, 10.2, 4.8], 'x-')
plt.xlabel('k')
plt.ylabel('t')
plt.semilogx()
plt.grid()
plt.show()


