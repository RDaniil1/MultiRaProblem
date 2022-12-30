from criteria_decision import voting_matrix, reshape, vald, savage, get_voting_matrix_result, pprint
from excluding_clasterisation import get_non_effective_values, plt
from numpy import column_stack

data = [
    [(7, 7), (8, 4), (10, 5), (9, 6)],
    [(5, 4), (6, 5), (7, 9), (14, 8)],
    [(11, 10), (7, 8), (6, 5), (12, 2)],
    [(10, 3), (11, 6), (9, 4), (4, 10)],
    [(1, 5), (2, 3), (1, 8), (2, 4)],
    [(2, 2), (1, 5), (2, 6), (4, 12)],
    [(3, 8), (3, 6), (2, 3), (2, 11)],
    [(4, 2), (1, 5), (3, 9), (3, 10)]
]

def get_effective_or_non_effective_coord(dots, effective, is_effective):
    dots_amount = range(len(dots[0]))
    coords = []
    for j in range(2):
        coords += [[dots[j][i] for i in dots_amount if effective[i] == is_effective]]

    return coords
    
def draw_projects(effective, non_effective, label):
    plt.figure(1, label=label)
    plt.grid(True)
    plt.gca().set_aspect('equal', adjustable='datalim')
    plt.axhline(0, c='black')
    plt.axvline(0, c='black')
    plt.xlabel("f1")
    plt.ylabel("f2")
    
    plt.scatter(*effective, c='green', label='Effective')
    plt.scatter(*non_effective, c='red', label='Non-effective')
    
    plt.legend()
    plt.show()
    
    
def get_fn_matrix(Q: list[list[tuple[int, int]]], n: int):
    if n not in [1, 2]:
        print('n must be only 1 or 2')
        return

    fn = []
    for row in Q:
        fn += [[F[n - 1] for F in row]]

    return fn

if __name__ == '__main__':
    Q = data

    f1 = get_fn_matrix(Q, 1)
    f2 = get_fn_matrix(Q, 2)
    
    pprint(f1)
    pprint(f2)

    task1_V = vald(f1, _return='matrix') + vald(f2, _return='matrix')
    task1_V = reshape(task1_V, (2, len(Q)))
    task1_res = ~get_non_effective_values({
        'x': task1_V[0],
        'y': task1_V[1]
    })
    
    effective = get_effective_or_non_effective_coord(task1_V, task1_res, True)
    non_effective = get_effective_or_non_effective_coord(task1_V, task1_res, False)
    
    draw_projects(effective, non_effective, 'Vect maximin')

    task2_V = savage(f1, _return='matrix') + savage(f2, _return='matrix')
    task2_V = reshape(task2_V, (2, len(Q)))
    task2_res = ~get_non_effective_values({
        'x': task2_V[0],
        'y': task2_V[1]
    }, True)

    effective = get_effective_or_non_effective_coord(task2_V, task2_res, True)
    non_effective = get_effective_or_non_effective_coord(task2_V, task2_res, False)
    
    draw_projects(effective, non_effective, 'Vect minimax')
    
    print(task1_res)
    print(task2_res)
    
    print('\nVoting matrix for f1:')
    vot_matr1 = voting_matrix(f1, ['vald', 'savage', 'hurwitz', 'laplas'])
    print('\nVoting matrix for f2:')
    vot_matr2 = voting_matrix(f2,  ['vald', 'savage', 'hurwitz', 'laplas'])
    
    final_vot_matr = column_stack((task1_res, task2_res, vot_matr1, vot_matr2))
    print('Final voting matrix:', final_vot_matr, sep='\n')
    print('Results:', *get_voting_matrix_result(final_vot_matr))
