print("\n=========INTERPOLARE LAGRANGE=========")
def lagrange(x_nodes, y_nodes, x):
    n = len(x_nodes)
    result = 0.0
    for i in range(n):
        Li = 1.0
        for j in range(n):
            if j != i:
                Li *= (x - x_nodes[j]) / (x_nodes[i] - x_nodes[j])
        result += y_nodes[i] * Li
    return result

## AFISARE ##
import math
n_nodes = 7
a, b = 0, 3
x_nodes = [a + i * (b - a) / (n_nodes - 1) for i in range(n_nodes)]
y_nodes = [math.exp(x) for x in x_nodes]
x_eval = [0.25, 0.75, 1.25, 1.75, 2.25, 2.75]
print(f"Noduri: {n_nodes} puncte pe [{a}, {b}]")
print(f"\n{'x':>8} {'P(x)':>14} {'f(x)':>14} {'Eroare':>12}")
max_err = 0.0
for x in x_eval:
    px = lagrange(x_nodes, y_nodes, x)
    fx = math.exp(x)
    err = abs(px - fx)
    if err > max_err:
        max_err = err
    print(f"{x:>8.2f} {px:>14.8f} {fx:>14.8f} {err:>12.2e}")
print(f"\nEroare maxima pe [{a},{b}]: {max_err:.6e}")


print("\n=========SPLINE CUBICE NATURALE=========")
import numpy as np
def cubic_spline(x_nodes, y_nodes):
    n = len(x_nodes) - 1
    h = np.diff(x_nodes)
    A = np.zeros((n+1, n+1)); b = np.zeros(n+1)
    A[0,0] = 1; A[n,n] = 1   # conditii naturale
    for i in range (1,n):
        A[i,i-1] = h[i-1]
        A[i,i] = 2*(h[i-1] + h[i])
        A[i,i+1] = h[i]
        b[i] = 6*((y_nodes[i+1]-y_nodes[i]) / h[i] - (y_nodes[i]-y_nodes[i-1])/h[i-1])
    M = np.linalg.solve(A, b)
    return M, h

## AFISARE ##
import math
n_nodes = 7
a, b = 0, 3
x_nodes = np.array([a + i * (b - a) / (n_nodes - 1) for i in range(n_nodes)])
y_nodes = np.array([math.exp(x) for x in x_nodes])
M, h = cubic_spline(x_nodes, y_nodes)
print(f"=== Spline cubic natural ===")
print(f"Noduri: {n_nodes} puncte pe [{a}, {b}]")
momente_str = ", ".join([f"{m:.4f}" for m in M])
print(f"\nMomente (M_i): [{momente_str}]")
def eval_spline(x_nodes, y_nodes, M, h, x):
    n = len(x_nodes) - 1
    for i in range(n):
        if x_nodes[i] <= x <= x_nodes[i+1]:
            hi = h[i]
            a_i = (x_nodes[i+1] - x) / hi
            b_i = (x - x_nodes[i]) / hi
            return (a_i * y_nodes[i] + b_i * y_nodes[i+1] +
                    ((a_i**3 - a_i) * M[i] + (b_i**3 - b_i) * M[i+1]) * hi**2 / 6)
    return None
x_eval = [0.25, 0.75, 1.25, 1.75, 2.25, 2.75]
print(f"\n{'x':>8} {'S(x)':>14} {'f(x)':>14} {'Eroare':>12}")
max_err = 0.0
for x in x_eval:
    sx = eval_spline(x_nodes, y_nodes, M, h, x)
    fx = math.exp(x)
    err = abs(sx - fx)
    if err > max_err:
        max_err = err
    print(f"{x:>8.2f} {sx:>14.8f} {fx:>14.8f} {err:>12.2e}")
print(f"\nEroare maxima spline: {max_err:.6e}")


### RECAPITULARE ###
# INTERPOLARE = aproximarea functiilor
# Interpolarea polinomiala = aproximarea cu o functie
# Eroarea de trunchiere in interpolarea Lagrange
# Eroarea de rontunjire in interpolarea Lagrange
# Interpolarea Lagrange = trece prin toate punctele, dar poate oscila
# Interpolare Newton cu diferente finite
#           - speta 1 - diferente progresive
#           - speta 2 - diferente regresive
# Metoda lui Aitken de interpolare
# Spilne cubice naturale = combina interpolare exacta cu netezime C^2
# Fenomenul Runge = grad mare -> oscilatii la capete (noduri echidistante)
# Regresia liniara = minimizeaza suma patratelor reziduurilor
#                  - nu trece prin puncte dar ofera o aproximare globala robusta

### CONCLUZII ###
# Lagrange       - Interpolare - O(n^2)      - Instabil de grad mare
# Newton         - Interpolare - O(n^2)      - Adaugare facila de noduri
# Spline cubic   - Interpolare - O(n) sistem - Fara Runge, C^2
# Regresie CMMMP - Aproximare  - O(nm^2)     - Robust la zgomot