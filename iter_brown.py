from texttable import Texttable
from numpy import transpose, array, zeros, where,set_printoptions
from collections import Counter
import matplotlib.pyplot as plt
from geometry import solve_task
from sys import exit
from pandas import DataFrame


set_printoptions(2)

A = array([[7, 5, 4, 2],
           [1, 2, 5, 6]])

transp_A = transpose(A)
n = 200

def saddle_point_exist(matrix: list[list[float]]) -> bool:
    alpha = max([min(column) for column in matrix])
    beta = min([max(row) for row in transpose(matrix)]) 
    return alpha == beta

def create_table_header():
    second_strategies = [f'C{i + 1}' for i in range(len(A[0]))]
    first_strategies = [f'M{j + 1}' for j in range(len(A))]
    return ['K', 'i', *second_strategies, 'alpha_k', 'j', *first_strategies, 'beta_k', 'v']
    
def print_game_states(game_states):
    headers = create_table_header()
    table = Texttable()
    table.header(headers)
    table.add_rows(game_states, header=False)
    print(table.draw())

def export_table_to_excel(table):
    headers = create_table_header()
    df = DataFrame(table, columns=headers)
    df.to_excel('iter_brown.xlsx', engine='xlsxwriter')

def nullify_strategies(strategy, amount):
    if len(strategy) != amount:
        for i in range(1, amount + 1):
            if i not in strategy.keys():
                strategy[i] = 0
    return strategy

def print_strategies(name, strategy):
    for i, amount in strategy.items():
        print(f'{name}{i} = {amount}', f'{name}{i}* = {amount / n}')
    print()

if __name__ == '__main__':
    if saddle_point_exist(A):
        print('This matrix has a saddle point')
        exit(0)

    game_states = []
    row = array(A[0])
    column = zeros(len(A), dtype=float)
    i = 0
    max_j = []
    min_i = []
    v = 0 
    _pi = []
    _is = [i]
    for k in range(1, n + 1):
        j = where(row == min(row))[0][0]
        column += transp_A[j]
        alpha_k = min(row) / k
        beta_k = max(column) / k
        v = (alpha_k + beta_k) / 2
        _pi += [v]
        max_j += [j + 1]
        min_i += [i + 1]

        game_states += [ [k, i + 1, *row, alpha_k, j + 1, *column, beta_k, v] ]
        
        if k != n:
            i = where(column == max(column))[0][0]
            row += A[i]
        _is += [i]
        
    p = dict(Counter(min_i).most_common(len(A)))
    q = dict(Counter(max_j).most_common(len(A[0])))

    p = nullify_strategies(p, len(A))
    q = nullify_strategies(q, len(A[0]))

    print_game_states(game_states)
    export_table_to_excel(game_states)

    print_strategies('p', p)
    print_strategies('q', q)

    print(f'v = {v}')

    p_mixed_strat = solve_task(A)
    
    plt.figure(1, label='p', figsize=(5, 5.5))
    plt.plot(range(n), abs(array(_pi) - p_mixed_strat), color='blue')
    plt.xlabel('k')
    plt.ylabel('|p(k) - p|')
    plt.axhline(color='black')
    plt.axvline(color='black')
    plt.grid(True)
    plt.show()

