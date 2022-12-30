from numpy import array, transpose, row_stack, \
     where, vectorize, float64, any, eye, \
          around, dot
from random import choice
from texttable import Texttable


A = array([[7, 5, 4, 2],
          [1, 2, 5, 6]])
b = array([1, 1, 1, 1])
fx = [1, 1]

def print_table(A):
    table = Texttable()
    table.add_rows(A, False)
    print(table.draw())
    
def get_basis_ind_from_arr(headers: list[str]):
     str_indexes = [st.replace('x', '') for st in headers]
     return [int(num) - 1 for num in str_indexes]

def get_index_for_searching_max(max_len: int, indexes: list[int]):
     return list(set(range(max_len)) - set(indexes))

def get_results(arr, c, headers):
     c_len = len(c)
     basis_ind = get_basis_ind_from_arr(headers)
     c += [0 for _ in range(len(arr))]
     temp = [ 0 for _ in range(len(arr)) ]
     arr = transpose(arr)
     for ind, i in enumerate(basis_ind):
          temp[ind] = 1 if c[i] == 1 else 0
     c = array(temp)
     res = []
     for row in arr:
          res += [dot(row, c)]
     return res

max_set_ind_x = len(A)
max_added_x_ind = len(A[0])
max_ind_x = max_set_ind_x + max_added_x_ind
headers_row = [f'x{i + 1}' for i in range(max_ind_x)]
headers_column = [f'x{i + 1}' for i in range(max_set_ind_x, max_ind_x)]
#If goal function -> min
#Rotate functions to concatenate
simplex = transpose(row_stack((*A, eye(len(A[0])) * -1, b)) * -1)
simplex = vectorize(float64)(simplex)
simplex = around(simplex, decimals=2)

print(simplex)
print(headers_column)

b_ind = len(A) + len(A[0])
#Calculate until all b elements is bigger or equal 0
while any(simplex[:,b_ind] < 0):
     # To find max abs element
     simplex_abs = around(vectorize(abs)(simplex), decimals=2)
     #Set random max, if multiple values are the same 
     multiple_max_row_ind = [i for i, x in enumerate(simplex_abs[:,b_ind]) if x == max(simplex_abs[:,b_ind])]
     max_row = choice(multiple_max_row_ind)
     search_ind = get_index_for_searching_max(max_ind_x, get_basis_ind_from_arr(headers_column))
     max_on_selected_row = max(simplex_abs[max_row, search_ind])
     max_column = where(simplex_abs[max_row] == max_on_selected_row)[0][0]
     #Max element on cross
     choosed_elem = simplex[max_row,max_column]
     simplex[max_row] /= choosed_elem
     columns_subs = [i for i in range(len(A[0])) if i != max_row]
     #Substitute from non-max rows
     for other_ind in columns_subs:
          mult_num_on_basis_column = simplex[other_ind, max_column]
          multiplied_max_row = simplex[max_row] * mult_num_on_basis_column
          other_row = simplex[other_ind, :]
          simplex[other_ind, :] -= multiplied_max_row
     print_table(simplex) 
     headers_column[max_row] = headers_row[max_column]
     print(headers_column)

v = get_results(simplex, fx, headers_column)
print(get_results(simplex, fx, headers_column))