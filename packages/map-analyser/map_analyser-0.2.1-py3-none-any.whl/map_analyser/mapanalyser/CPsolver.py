import cvxpy as cp
import numpy as np
from scipy.optimize import minimize

TOLERANCE = 0.01


def get_point(a, b, x):
    px = a[0] + x * (b[0] - a[0])
    py = a[1] + x * (b[1] - a[1])
    return px, py


def loss_function(x, common_edges, start, end, speeds):
    points = [get_point(a, b, x) for (a, b), x in zip(common_edges, x)]
    dist = speeds[0] * (np.sqrt((start[0] - points[0][0]) ** 2 + (start[1] - points[0][1]) ** 2))

    for i in range(len(points) - 1):
        dist += speeds[i + 1] * (
            np.sqrt((points[i][0] - points[i + 1][0]) ** 2 + (points[i][1] - points[i + 1][1]) ** 2))

    dist += speeds[-1] * (np.sqrt((points[-1][0] - end[0]) ** 2 + (points[-1][1] - end[1]) ** 2))
    return dist


def get_objective_function(lamb, Ax, Ay, Bx, By, speeds, sx, sy, ex, ey):
    xs = Ax + cp.multiply(lamb, (Bx - Ax))
    ys = Ay + cp.multiply(lamb, (By - Ay))

    xs1 = cp.hstack((sx, xs))
    xs2 = cp.hstack((xs, ex))
    ys1 = cp.hstack((sy, ys))
    ys2 = cp.hstack((ys, ey))

    diff = cp.vstack((xs1 - xs2, ys1 - ys2))

    distances = cp.norm(diff, 2, axis=0)

    return cp.sum(cp.multiply(speeds, distances))


def solve(start, end, speeds, common_edges):
    lamb = cp.Variable(len(common_edges))

    Ax = np.asarray([p[0][0] for p in common_edges])
    Ay = np.asarray([p[0][1] for p in common_edges])
    Bx = np.asarray([p[1][0] for p in common_edges])
    By = np.asarray([p[1][1] for p in common_edges])
    sx = np.asarray([start[0]])
    sy = np.asarray([start[1]])
    ex = np.asarray([end[0]])
    ey = np.asarray([end[1]])

    obj = cp.Minimize(get_objective_function(lamb, Ax, Ay, Bx, By, speeds, sx, sy, ex, ey))

    constraints = [0 <= lamb, lamb <= 1]
    problem = cp.Problem(obj, constraints)

    problem.solve(solver='ECOS', verbose=False, abstol=TOLERANCE)

    return problem.value, lamb.value


def solve_all(start, end, speeds, common_edges):
    n = len(common_edges)
    naive_initial = [0.6] * n
    bounds = [(0, 1)] * n

    import time
    for method in ['L-BFGS-B']:
        t = time.time()
        ret = minimize(lambda x: loss_function(x, common_edges, start, end, speeds),
                       naive_initial,
                       method=method,
                       bounds=bounds)
        print(str(time.time() - t) + '\t' + method + '\t' + str(ret.fun) + '\t' + str(ret.x))

    lamb = cp.Variable(n)

    Ax = np.asarray([p[0][0] for p in common_edges])
    Ay = np.asarray([p[0][1] for p in common_edges])
    Bx = np.asarray([p[1][0] for p in common_edges])
    By = np.asarray([p[1][1] for p in common_edges])
    sx = np.asarray([start[0]])
    sy = np.asarray([start[1]])
    ex = np.asarray([end[0]])
    ey = np.asarray([end[1]])

    obj = cp.Minimize(get_objective_function(lamb, Ax, Ay, Bx, By, speeds, sx, sy, ex, ey))

    constraints = [0 <= lamb, lamb <= 1]
    problem = cp.Problem(obj, constraints)

    for solver in cp.installed_solvers():
        t = time.time()
        try:
            problem.solve(solver=solver, verbose=False)
            print(str(time.time() - t) + '\t' + solver + '\t' + str(problem.value) + '\t' + str(lamb.value))
        except Exception as ex:
            pass
            # print(ex)

    return problem.value, lamb.value
