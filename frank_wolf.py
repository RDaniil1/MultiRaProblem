from pulp import LpMaximize, LpProblem, lpSum, LpVariable, PULP_CBC_CMD, LpMinimize
from sympy import symbols, solve, simplify
from math import fabs


n = 23
x1, x2 = symbols('x1, x2')
fx_concave = 0

fx_dst_coeff = [
    [1, 1],
    [-3, 1],
    [1, -3]
]

model_data = ['x1_model + x2_model >= 2 * n', 
              'x1_model - 2 *x2_model <= n', 
              '-3 * x1_model + 2 *x2_model <= 2 * n', 
              'x1_model <= 4 * n', 
              'x2_model <= 3 * n', 
              'x1_model >= 0', 
              'x2_model >= 0']

def ideal_dot_iter(iter_num: int):
    model = LpProblem(sense=LpMaximize)

    x1_model = LpVariable("x1")
    x2_model = LpVariable("x2")
    
    for data in model_data: 
        model += eval(data)
    
    fxn_dst = [fx_dst_coeff[iter_num][0] * x1_model, fx_dst_coeff[iter_num][1] * x2_model]
    model += lpSum(fxn_dst)

    model.solve(PULP_CBC_CMD(msg=False))
    
    return sum([model.variables()[i].value() * fx_dst_coeff[iter_num][i] for i in range(2)])

def frank_wolfs_iter(x1_n: float, x2_n: float) -> dict[float]:
    coeff_x1 = fx_concave.diff(x1).subs({x1 : x1_n, x2 : x2_n})
    coeff_x2 = fx_concave.diff(x2).subs({x1 : x1_n, x2 : x2_n})
    
    model = LpProblem(sense=LpMinimize)

    x1_model = LpVariable("x1")
    x2_model = LpVariable("x2")

    for data in model_data: 
        model += eval(data)

    model += lpSum([coeff_x1 * x1_model, coeff_x2 * x2_model])

    model.solve(PULP_CBC_CMD(msg=False))
    
    opt_coord = [var.value() for var in model.variables()]
    
    lambda_n = symbols('lambda_n')
    
    xn = [x1_n, x2_n]
    x1_new, x2_new = [simplify(xn[i] + lambda_n * (opt_coord[i] - xn[i])) for i in range(2)]
    
    subbed_fx = simplify(fx_concave.subs({x1 : x1_new, x2 : x2_new}))
    first_fx_deriv_on_lambda = subbed_fx.diff(lambda_n)
    
    lambda_val = solve(first_fx_deriv_on_lambda, lambda_n)[0] if first_fx_deriv_on_lambda != 0 else 0
    
    return {x1 : x1_new.subs(lambda_n, lambda_val),
            x2 : x2_new.subs(lambda_n, lambda_val)}

def get_dst_values(x1_opt: float, x2_opt: float):
    return { f'f{i + 1}' : fx_dst_coeff[i][0] * x1_opt + fx_dst_coeff[i][1] * x2_opt for i in range(3)}
    
for it in range(3):
    fx_concave += (ideal_dot_iter(it) - (fx_dst_coeff[it][0] * x1 + fx_dst_coeff[it][1] * x2)) ** 2

opt_ideal_dot_coord = solve([fx_concave.diff(x1), fx_concave.diff(x2)])
print(opt_ideal_dot_coord)
print(get_dst_values(opt_ideal_dot_coord[x1], opt_ideal_dot_coord[x2]))

X_n = {x1 : 3 * n, 
       x2 : 2 * n}
func_val = 0
func_val_new = float('inf')
eps = 0.01
while fabs(func_val_new - func_val) > eps:
    X_n = frank_wolfs_iter(X_n[x1], X_n[x2])
    func_val = func_val_new 
    func_val_new = fx_concave.subs({x1 : X_n[x1], x2 : X_n[x2]})

print(X_n)
print(get_dst_values(X_n[x1], X_n[x2]))
