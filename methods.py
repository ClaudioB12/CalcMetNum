import matplotlib
matplotlib.use('Agg')  # 👈 Esta línea evita errores de tkinter

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq


def bisection(f, a, b, tol=1e-6, max_iter=100):
    iteraciones = []
    for i in range(max_iter):
        c = (a + b) / 2
        fc = f(c)
        iteraciones.append((i, c, fc))
        if abs(fc) < tol or abs(b - a) < tol:
            break
        if f(a) * fc < 0:
            b = c
        else:
            a = c
    return c, iteraciones

def false_position(f, a, b, tol=1e-6, max_iter=100):
    iteraciones = []
    for i in range(max_iter):
        fa, fb = f(a), f(b)
        c = b - fb * (b - a) / (fb - fa)
        fc = f(c)
        iteraciones.append((i, c, fc))
        if abs(fc) < tol:
            break
        if fa * fc < 0:
            b = c
        else:
            a = c
    return c, iteraciones

def newton_raphson(f, df, x0, tol=1e-6, max_iter=100):
    iteraciones = []
    x = x0
    for i in range(max_iter):
        fx, dfx = f(x), df(x)
        if dfx == 0:
            break
        x_new = x - fx / dfx
        iteraciones.append((i, x_new, f(x_new)))
        if abs(f(x_new)) < tol:
            break
        x = x_new
    return x, iteraciones

def secant(f, x0, x1, tol=1e-6, max_iter=100):
    iteraciones = []
    for i in range(max_iter):
        if f(x1) - f(x0) == 0:
            break
        x2 = x1 - f(x1) * (x1 - x0) / (f(x1) - f(x0))
        iteraciones.append((i, x2, f(x2)))
        if abs(f(x2)) < tol:
            break
        x0, x1 = x1, x2
    return x2, iteraciones

def brent_method(f, a, b, tol=1e-6):
    root = brentq(f, a, b, xtol=tol)
    return root, []  # Brent no da iteraciones detalladas

def plot_function(f, a, b, iteraciones, method_name):
    x = np.linspace(a, b, 400)
    y = f(x)
    plt.figure()
    plt.plot(x, y, label='f(x)')
    if iteraciones:
        x_vals = [it[1] for it in iteraciones]
        y_vals = [it[2] for it in iteraciones]
        plt.plot(x_vals, y_vals, 'ro-', label='Iteraciones')
    plt.axhline(0, color='black', linestyle='--')
    plt.title(f'Gráfico del método {method_name}')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.legend()
    plt.grid(True)
    plt.savefig('static/graph.png')
    plt.close()
