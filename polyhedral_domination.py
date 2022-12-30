import matplotlib.pyplot as plt
from texttable import Texttable
from numpy import full, array
from numpy.random import seed, uniform
from math import atan2, cos, sin, pi, sqrt
from pandas import DataFrame


seed(7)

mu1_min = 0.3
mu1_max = 0.7
mu2_min = 0.3
mu2_max = 0.6

class Point:
    def __init__(self, x, y, eff):
        self.x=x
        self.y=y
        self.eff=eff

def perpendicular(x, y):
    length = sqrt(x**2 + y**2)
    angle = atan2(y, x)
    
    return length*cos(angle+pi/2), length*sin(angle+pi/2)

b_coord = array([[-mu2_max + 1, mu2_max], [-mu2_min + 1, mu2_min]])

omega1_x, omega1_y = perpendicular(*b_coord[0])
omega2_x, omega2_y = perpendicular(*b_coord[1])

N = 100

U1 = uniform(0, 79, N)
U2 = uniform(0, 79, N)

Jn = lambda a, b, j: 0.2 * (U1[j] - a)**2 + 0.8 * (U2[j] - b)**2
    
J1 = [Jn(70, 20, j) for j in range(N)]
J2 = [Jn(10, 70, j) for j in range(N)]

dots = [Point(J1[i], J2[i], True) for i in range(N)]

non_eff_straight = full(N, False)

df = DataFrame()

def plot_polyhedral_cone():
    plt.figure(1)
    plt.gca().set_aspect('equal', adjustable='datalim')
    plt.xlim((-1.5, 1.5))
    plt.ylim((-1.5, 1.5))
    plt.axhline(0, c='black')
    plt.axvline(0, c='black')
    plt.xlabel("J1")
    plt.ylabel("J2")

    plt.plot([0, mu1_max], [mu2_min, mu2_min], '--', c='#9e9595')
    plt.annotate('mu2min', (0, mu2_min - 0.1))
    plt.plot([0, mu1_max], [mu2_max, mu2_max], '--', c='#9e9595')
    plt.annotate('mu2max', (0, mu2_max - 0.1))
    plt.plot([mu1_min, mu1_min], [mu2_max, 0], '--', c='#9e9595')
    plt.annotate('mu1min', (mu1_min - 0.1, 0))
    plt.plot([mu1_max, mu1_max], [mu2_max, 0], '--', c='#9e9595')
    plt.annotate('mu1max', (mu1_max - 0.1, 0))

    plt.plot([0, 1], [1, 0], c='orange', label='y = 1 - x')

    plt.quiver([0, 0], [0, 0], b_coord[:, 0], b_coord[:, 1], angles='xy', scale_units='xy', scale=1, color='blue', label='B')

    plt.quiver(*[0, 0], *[(omega1_x / omega1_y) * mu2_min , mu2_min ],  angles='xy', scale_units='xy', scale=1, color='red')
    plt.quiver(*[0, 0], *[mu1_min, -(-omega2_y / omega2_x) * mu1_min],  angles='xy', scale_units='xy', scale=1, color='red', label='Omega')

    plt.legend()
    plt.grid(True)

def scatter_straight():
    plt.figure(2)
    plt.gca().set_aspect('equal', adjustable='datalim')
    plt.axhline(0, c='black')
    plt.axvline(0, c='black')
    plt.grid(True)

    plt.xlabel("J1")
    plt.ylabel("J2")

    i = 0
    true_ind = []
    while i < N:
        seek_on_J1 = []
        seek_on_J2 = []
        
        if i in true_ind:
            i += 1
            continue
        
        for val in J1:
            seek_on_J1 += [J1[i] < val]
        seek_on_J1[i] = False

        for val in J2:
            seek_on_J2 += [J2[i] < val]
        seek_on_J2[i] = False
        
        seek_res = [True if seek_on_J1[i] == seek_on_J2[i] == True else False for i in range(len(seek_on_J1))]
        
        if not true_ind:
            true_ind = [ind for ind in range(len(seek_res)) if seek_res[ind] == True]
        else: 
            true_ind = sorted(list(set(true_ind) | set([ind for ind in range(len(seek_res)) if seek_res[ind] == True])))
        
        i += 1

    non_eff_straight[[true_ind]] = True 

    df = DataFrame({'J1' : J1, 'J2' : J2, 'Non-effective' : non_eff_straight})
    true_df = df[df['Non-effective'] == False]
    false_df = df[df['Non-effective'] == True]

    plt.scatter(false_df['J1'], false_df['J2'], c='red', label='Non-effective')
    plt.scatter(true_df['J1'], true_df['J2'], c='green', label='Effective')

    plt.legend()

def scatter_polyhedral():
    plt.figure(3)

    plt.gca().set_aspect('equal', adjustable='datalim')

    plt.axhline(0, c='black')
    plt.axvline(0, c='black')

    plt.xlabel("J1")
    plt.ylabel("J2")

    plt.grid(True)

    for i in range(N):
        for j in range(N):
            r = b_coord.dot([J1[i] - J1[j], J2[i] - J2[j]])
            if r[0] <= 0 and r[1] and r[0] != r[1]:
                dots[j].eff=False
    
    get_dots_by_state = lambda state: [[dots[i].x for i in range(N) if dots[i].eff == state],
                                        [dots[i].y for i in range(N) if dots[i].eff == state]]
        
    plt.scatter(*get_dots_by_state(False), c='red', label='Non-effective') 
    plt.scatter(*get_dots_by_state(True), c='green', label='Effective') 
        
    plt.legend()

def print_table_for_cone(non_eff: list[bool]):   
    table = Texttable()
    table.header(['№', 'X', 'Y', 'Non-effective'])

    for i in range(len(dots)):
        table.add_row([i + 1, dots[i].x, dots[i].y, non_eff[i]])

    print(table.draw())

plot_polyhedral_cone()
scatter_straight()
scatter_polyhedral()

non_eff_polyhedral = [not dots[i].eff for i in range(N)]

print_table_for_cone(non_eff_straight)
print_table_for_cone(non_eff_polyhedral)

plt.show()
