import numpy as np
from matplotlib import pyplot as plt


def Parabola(x, p0, p1, p2):
    y = p0+p1*x+p2*x**2
    return y

def main():
    x = np.linspace(0, 300, 5000)
    plt.figure()
    plt.plot(x, Parabola(x, 21.18, 2.34e-1, 9.75e-5), label='Real Data')
    plt.plot(x, Parabola(x, 22.38, 2.05e-1, 1.95e-4), label=r'2$\times$ p2')
    plt.plot(x, Parabola(x, 24.77, 1.48e-1, 3.90e-4), label=r'4$\times$ p2')
    plt.plot(x, Parabola(x, 29.54, 3.27e-2, 7.80e-4), label=r'8$\times$ p2')
    plt.legend(loc='best')
    #plt.show()
    plt.savefig('Parabolae.pdf')

main()
