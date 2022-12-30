import matplotlib.pyplot as plt
from numpy import sqrt, linspace, full
from texttable import Texttable
from pandas import DataFrame
import warnings


warnings.filterwarnings("ignore")

n = 23

test_data = {
    'x' : [33, 28, 20, 31, 33, 29, 35, 22, 35, 29, 38, 32, 36, 33, 41, 43, 41, 37, 30, 32],
    'y' : [30, 35, 28, 39, 36, 34, 38, 30, 39, 27, 19, 21, 19, 23, 18, 25, 24, 18, 23, 17]
}

def get_non_effective_values(dots: dict[str, list[float]], inverse: bool = False):
    i = 0
    true_ind = []
    seek_on_x = []
    seek_on_y = []
    while i < len(dots['x']):
        seek_on_x = []
        seek_on_y = []
        
        if i in true_ind:
            i += 1
            continue
        
        for val in dots['x']:
            seek_on_x += [dots['x'][i] >= val] if not inverse else [dots['x'][i] <= val]
        seek_on_x[i] = False

        for val in dots['y']:
            seek_on_y += [dots['y'][i] >= val] if not inverse else [dots['y'][i] <= val]
        seek_on_y[i] = False
        
        seek_res = [True if seek_on_x[i] == seek_on_y[i] == True else False for i in range(len(seek_on_x))]
        
        if not true_ind:
            true_ind = [ind for ind in range(len(seek_res)) if seek_res[ind] == True]
        else: 
            true_ind = sorted(list(set(true_ind) | set([ind for ind in range(len(seek_res)) if seek_res[ind] == True])))
        
        i += 1

    non_effective = full(len(dots['x']), False)
    non_effective[[true_ind]] = True 
    
    return non_effective

def print_non_effective_table(dots: dict[str, list[float]], non_effective: list[float]):
    table = Texttable()
    table.header(['Dot', 'f1', 'f2', 'Non-effective'])

    for i in range(len(dots['x'])):
        table.add_row([f'a{i + 1}', dots['x'][i], dots['y'][i], non_effective[i]])

    print(table.draw())

def get_in_cone_dots(dots: dict[str, list[float]]):
    non_effective = []
    seek_on_x = []
    seek_on_y = []
    for i in range(len(dots['x'])):
        seek_on_x = [dots['x'][i] <= v for v in dots['x']] 
        seek_on_x[i] = False 
        seek_on_y = [dots['y'][i] <= v for v in dots['y']]
        seek_on_y[i] = False
        
        seek_res = [True if seek_on_x[i] == seek_on_y[i] == True else False for i in range(len(seek_on_x))]
        
        non_effective += [seek_res]

    return [is_dots_in_cone.count(True) for is_dots_in_cone in non_effective] 

def get_f_dots(in_cone_dots: list):
    return [1 / (1 + (bi / (20 - 1))) for bi in in_cone_dots]

def get_ki_dots(f_dots: list[float]):
    ki_dots = []
    center_between_k3_k2 = 0.75 + (0.85 - 0.75) / 2
    center_between_k2_k1 = 0.85 + (1 - 0.85) / 2
    for i in range(len(f_dots)):
        ki_range_dispatcher = {
            f_dots[i] < 0.75 : 3,
            0.75 <= f_dots[i] < center_between_k3_k2 : 3,
            center_between_k3_k2 <= f_dots[i] <= 0.85 : 2,
            0.85 <= f_dots[i] < center_between_k2_k1 : 2,
            center_between_k2_k1 <= f_dots[i] <= 1 : 1
        }
        ki_dots += [ki_range_dispatcher[True]]
    
    return ki_dots 

def print_klustered_dots_table(dots: dict[str, list[float]], in_cone_dots: list[float], f_dots: list[float], ki_dots: list[float]):
    table = Texttable()
    table.header(['Dot', 'F1', 'F2', 'bi', 'F', 'Ki'])

    for i in range(len(dots['x'])):
        table.add_row([f'a{i + 1}', dots['x'][i], dots['y'][i], in_cone_dots[i], f_dots[i], ki_dots[i]])

    print(table.draw())

def draw_plot(dots: dict[str, list[float]], ki_dots: list[float]):
    df = DataFrame({'f1' : dots['x'], 'f2' : dots['y'], 'Ki' : ki_dots})
    k3_df = df[df['Ki'] == 3]
    k2_df = df[df['Ki'] == 2]
    k1_df = df[df['Ki'] == 1]

    fig, (clusters_dots, in_area_dots) = plt.subplots(1, 2, figsize=(14, 7.5))

    in_area_dots.grid(True)

    in_area_dots.axhline(0, color='black')
    in_area_dots.axvline(0, color='black')

    in_area_dots.plot(linspace(-20, 80, 100), 2 * n - linspace(-20, 80, 100), label='-f1 + f2 <= 23')
    in_area_dots.plot(linspace(-20, 80, 100), n + linspace(-20, 80, 100), label='f1 + f2 >= 2 * 23')
    in_area_dots.plot(linspace(0, n * 2 + 1, 1500), -sqrt(n ** 2 - (linspace(0, n * 2 + 1, 1500) - n) ** 2) + n, color='blue')
    in_area_dots.plot(linspace(0, n * 2 + 1, 1500), sqrt(n ** 2 - (linspace(0, n * 2 + 1, 1500) - n) ** 2) + n, color='blue', label='(f1 - 23)^2 + (f2 - 23)^2 <= 23^2')

    in_area_dots.scatter(k3_df['f1'], k3_df['f2'], c='red')
    in_area_dots.scatter(k2_df['f1'], k2_df['f2'], c='red')
    in_area_dots.scatter(k1_df['f1'], k1_df['f2'], c='red')

    in_area_dots.annotate('F1', (10, 2))
    in_area_dots.annotate('F2', (2, 10))

    in_area_dots.legend()

    clusters_dots.grid(True)

    clusters_dots.axhline(0, color='black')
    clusters_dots.axvline(0, color='black')

    clusters_dots.scatter(k3_df['f1'], k3_df['f2'], c='green', label='K3')
    clusters_dots.scatter(k2_df['f1'], k2_df['f2'], c='orange', label='K2')
    clusters_dots.scatter(k1_df['f1'], k1_df['f2'], c='red', label='K1')

    clusters_dots.annotate('F1', (10, 1))
    clusters_dots.annotate('F2', (1, 10))

    clusters_dots.legend()

    plt.show()

if __name__ == '__main__':
    dots = test_data
    non_effective = get_non_effective_values(dots)
    print_non_effective_table(dots, non_effective)
    
    in_cone_dots = get_in_cone_dots(dots)
    f_dots = get_f_dots(in_cone_dots)
    ki_dots = get_ki_dots(f_dots)
    print_klustered_dots_table(dots, in_cone_dots, f_dots, ki_dots)
    
    draw_plot(dots, ki_dots)
