from sympy import symbols, simplify, solve
from itertools import combinations
import matplotlib.pyplot as plt


p1, p2, q1, q2, q3, q4, v = symbols('p1 p2 q1 q2 q3 q4 v')

def fp(A, i):
    return simplify(A[0][i] * p1 + A[1][i] * (1 - p1))

def fq(A, q1_1, q1_2, qi = q1, first_row: bool = True):
    A_i_row = (A[0][q1_1], A[0][q1_2]) if first_row else (A[1][q1_1], A[1][q1_2])
    return simplify(A_i_row[0] * qi + A_i_row[1] * (1 - qi)) 

def count_p1_coords_and_draw_fp_plot(A):
    v_limits = [0, 1]
    colors = ['blue', 'purple', 'green', 'orange']
    for i in range(len(A[0])):
        p1_res = []
        fp_i = fp(A, i)
        p1_res += [ fp_i.subs(p1, v_limits[0]) ]
        p1_res += [ fp_i.subs(p1, v_limits[1]) ]
        plt.plot(v_limits, p1_res, label=f'{fp_i}', color=colors[i])

def draw_plot_pattern(xlabel: str, ylabel: str):  
    plt.grid(True)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.axhline(0, color='black')
    plt.axvline(0, color='black')
    plt.legend()

def solve_task(matrix: list[list[int]]):
    p1_coords = []
    v_coords = []
    combs = list(combinations(range(len(matrix[0])), len(matrix)))
    for i, j in combs:
        if fp(matrix, i) - v !=  fp(matrix, j) - v:
            res = solve((fp(matrix, i) - v, fp(matrix, j) - v), p1, v)
        else: 
            res = solve((fp(matrix, i), fp(matrix, j)), p1, v)
            res[v] = 0
        p1_coords += [res[p1]]
        v_coords += [res[v]]
        
    plt.figure(1, label='fp', figsize=(6, 6.5))

    plt.scatter(p1_coords, v_coords, color='red')
    for i in range(len(p1_coords)):
        plt.annotate(f'{i + 1}', (p1_coords[i], v_coords[i]))

    count_p1_coords_and_draw_fp_plot(matrix)
    draw_plot_pattern('p1', 'f(p1, j)')

    plt.show()

    opt_project_ind = int(input('Find and type optimum dot num: ')) - 1
    opt_columns = combs[opt_project_ind]

    i, j = opt_columns
    p1_res = solve((fp(matrix, i) - v, fp(matrix, j) - v), p1, v)
    p1_res[p2] = 1 - p1_res[p1] 

    qi_opt1 = eval(f'q{opt_columns[0] + 1}')
    qi_opt2 = eval(f'q{opt_columns[1] + 1}')

    qi_res = solve((fq(matrix, i, j, qi_opt1) - v, fq(matrix, i, j, qi_opt1, False) - v), qi_opt1, v)
    
    qi_null = set(range(len(matrix[0]))) - set(opt_columns)

    qi_res[qi_opt2] = 1 - qi_res[qi_opt1]
    for i in qi_null:
        qi_res[f'q{i + 1}'] = 0

    print(p1_res, qi_res, sep='\n')

    return qi_res[v]

# A = [[5, 4, 3, 2],
#      [1, 4, 4, 7]]

# solve_task(A)