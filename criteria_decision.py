from numpy import transpose, dot, reshape, where
from pprint import pprint
from collections import defaultdict


test_data = [
     [7, 8, 10, 9,
      5, 6, 7, 14,
      11, 7, 6, 12,
      10, 11, 9, 4], 
     [1, 2, 1, 2,
      2, 1, 2, 4,
      3, 3, 2, 2,
      4, 1, 3, 3]]

def get_result_dispatcher(variants: list[str], a: list, is_max: bool = True):
	result_dispatcher = defaultdict()
	result_dispatcher[variants[0]] = get_min_max_indexes(a, is_max)
	result_dispatcher[variants[1]] = a
 
	return result_dispatcher

def get_min_max_indexes(arr, is_max: bool = True):
    min_max_arr = max(arr) if is_max else min(arr)
    is_min_max = lambda x: x == min_max_arr
    
    return [1 if is_min_max(num) else 0 for num in arr]
    
def vald(Q, _return: str='voting goal'):
	a = [min(xi) for xi in Q]
 
	print('Vald criteria: ')
	pprint(a)
	return get_result_dispatcher(['voting goal', 'matrix'], a)[_return]

def savage(Q, _return: str='voting goal'):
	Q_transp = transpose(Q)
	
	R = []
	print('Max elements on column and R:', [max(column) for column in Q_transp], sep='\n')
	for i in range(len(Q_transp)):
		temp = []
		for j in range(len(Q_transp[i])):
			temp += [max(Q_transp[i]) - Q_transp[i][j]]
		R += [temp]
	
	print('Savage criteria: ')
	pprint(transpose(R))
	a = [max(xi) for xi in transpose(R)]
	
	pprint(a)
	return get_result_dispatcher(['voting goal', 'matrix'], a, is_max=False)[_return]

def hurwitz(Q, gamma: float):
	min_nums = [min(row) for row in Q]
	max_nums = [max(row) for row in Q]
 
	print('Hurwitz criteria: ')
	print(min_nums)
	print(max_nums)
	
	Gi = lambda i, gamma: gamma * min_nums[i] + (1 - gamma) * max_nums[i]
 
	G = [Gi(i, gamma) for i in range(len(Q))]
	
	print(G)
	return get_min_max_indexes(G)

def baies(Q, p):
    d = [dot(p, q) for q in Q]
    
    print('Baies criteria: ')
    print(d)
    return get_min_max_indexes(d)

def laplas(Q, n): 
    f = [ 1 / n * sum(q) for q in Q]
    
    print('Laplas criteria: ')
    print(f)
    return get_min_max_indexes(f)

def voting_matrix(Q, enabled_criteria: list[str] = ['vald', 'savage', 'hurwitz', 'baies', 'laplas']):
	rows = len(Q)
	columns = len(Q[0])
 
	vot_matr = []
 
	criteria_dispatcher = {
    'vald' : 'vald(Q)',
	'savage' : 'savage(Q)',
	'hurwitz' : 'hurwitz(Q, 0.6)',
	'baies' : 'baies(Q, [0.1, 0.4, 0.4, 0.1])',
	'laplas' : 'laplas(Q, columns)'
 }
	
	for criteria in enabled_criteria:
		vot_matr += eval(criteria_dispatcher[criteria])
  
	vot_matr = reshape(vot_matr, (len(vot_matr) // rows, rows)).T
	
	print('Voting matrix: ')
	print(vot_matr)
	return vot_matr

def get_voting_matrix_result(vot_matr):
    vot_matr = [sum(xi) for xi in vot_matr]
    return where(get_min_max_indexes(vot_matr))[0] + 1
	
if __name__ == '__main__':
    Q = reshape(test_data, (8, 4))
    vot_matr = voting_matrix(Q)
    print(get_voting_matrix_result(vot_matr))