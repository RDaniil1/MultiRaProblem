from pulp import LpMaximize, LpProblem, lpSum, LpVariable, PULP_CBC_CMD
from pprint import pprint


n = 23
    
def get_additional_constraint(x1, x2, goal_x1, goal_x2, delta):
    return goal_x1 * x1 + goal_x2 * x2 - delta

def get_optimal_point(addit_constr: float=0, addit_constr2: float=0, iteration: int=0):
    model = LpProblem(sense=LpMaximize)

    x1 = LpVariable('x1')
    x2 = LpVariable('x2')

    model += (x1 + 2 * x2 <= 4 * 23)
    model += (2 * x1 + x2 >= n)
    model += (x1 <= 2 * n)
    model += (x2 <= 1.5 * n)
    model += (x1 >= 0)
    model += (x2 >= 0)
    
    match iteration:
        case 0:
            model += lpSum([x1, -3 * x2])
        case 1:
            model += (x1 + (-3) * x2 >= addit_constr)
            model += lpSum([-3 * x1, x2])
        case 2:
            model += (x1 + (-3) * x2 >= addit_constr)
            model += (-3 * x1 + x2 >= addit_constr2)
            model += lpSum([x1, x2])
            
    model.solve(PULP_CBC_CMD(msg=0))

    return [val.value() for val in model.variables()]

GOAL_FUNC = [[1, -3],
             [-3, 1],
             [1, 1]]

DELTA = [1, 3]

def get_res_from_goal_func(ind: int, P: list[float]):
    return GOAL_FUNC[ind][0] * P[0] + GOAL_FUNC[ind][1] * P[1]

points = []
points += [get_optimal_point()]
addit_constr = get_additional_constraint(*points[0], *GOAL_FUNC[0], DELTA[0])

points += [get_optimal_point(addit_constr, iteration=1)]
addit_constr2 = get_additional_constraint(*points[1], *GOAL_FUNC[1], DELTA[1])

points += [get_optimal_point(addit_constr, addit_constr2, 2)]

pprint(points)

goal_func_res = []
for i in range(3):
    goal_func_res += [get_res_from_goal_func(i, points[i])]

print(goal_func_res)