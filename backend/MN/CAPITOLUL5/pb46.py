import numpy as np

# ============================================================
# PROBLEMA 46 – Metoda Broyden (quasi-Newton pentru sisteme neliniare)
# Scop: rezolvăm F(x,y)=0 fără a recalcula Jacobianul la fiecare pas
# Curs: Cap. "Metode quasi-Newton – Broyden"
# CERINTA: Rezolvați F1 = x2 + y2 − 4 = 0, F2 = ex + y − 1 = 0 prin metoda Broyden, start (1.0, 1.5).
#
# Ideea: pornim cu un Jacobian B0 (aproximație), și la fiecare pas
#        actualizăm B cu formula rang-1 (Broyden update):
#        B_nou = B + (Δf - B·Δx) · ΔxᵀI / ||Δx||²
#        unde Δx = x_nou - x_vechi, Δf = F(x_nou) - F(x_vechi)
# ============================================================

def F(v):
    """Sistemul de rezolvat:
    F1 = x² + y² - 4 = 0
    F2 = e^x + y - 1 = 0
    """
    x, y = v
    return np.array([x**2 + y**2 - 4,
                     np.exp(x) + y - 1])

# --- Parametri ---
x0 = np.array([1.0, 1.5])   # punct de start (x0, y0)
tol = 1e-6
max_iter = 20

# --- Jacobianul numeric inițial (aproximare prin diferențe finite) ---
# Curs: "Jacobianul numeric – diferențe finite"
def jacobian_numeric(F, x, h=1e-6):
    """Calculăm ∂F_i/∂x_j ≈ [F(x + h*e_j) - F(x)] / h"""
    n = len(x)
    J = np.zeros((n, n))
    f0 = F(x)
    for j in range(n):
        xh = x.copy()
        xh[j] += h           # perturbăm componenta j
        J[:, j] = (F(xh) - f0) / h
    return J

# Pornim cu B0 = Jacobianul numeric la x0
B = jacobian_numeric(F, x0)
x = x0.copy()

print("Metoda Broyden pentru F1=x²+y²-4=0, F2=eˣ+y-1=0")
print(f"Start: x0 = {x0}\n")
print(f"{'Iter':>5}  {'x':>12}  {'y':>12}  {'||F||':>12}")
print("-" * 50)

for i in range(max_iter):
    f = F(x)
    norma = np.linalg.norm(f)
    print(f"{i:>5}  {x[0]:>12.8f}  {x[1]:>12.8f}  {norma:>12.2e}")

    # Criteriu de oprire: F ≈ 0
    if norma < tol:
        print(f"\nConvergență la iterația {i}")
        break

    # Pasul Broyden: rezolvăm B * Δx = -F(x) (ca la Newton)
    delta_x = np.linalg.solve(B, -f)

    x_nou = x + delta_x      # noul punct
    f_nou = F(x_nou)         # valoarea funcției în noul punct

    # --- Actualizarea Broyden a aproximației Jacobianului ---
    delta_f = f_nou - f      # variația funcției
    # Formula Broyden rang-1:
    # B = B + (Δf - B·Δx) · Δxᵀ / ||Δx||²
    B = B + np.outer((delta_f - B @ delta_x), delta_x) / np.dot(delta_x, delta_x)

    x = x_nou

print(f"\n>>> Soluție: x = {x[0]:.8f}, y = {x[1]:.8f}")
print(f">>> Verificare F(x,y) = {F(x)}")