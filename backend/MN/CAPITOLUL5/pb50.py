import numpy as np

# ============================================================
# PROBLEMA 50 – Jacobianul numeric prin diferențe finite
# Scop: aproximăm ∂F_i/∂x_j fără formule analitice
# Curs: Cap. "Diferențe finite – aproximarea derivatelor"
#       Cap. "Newton-Raphson pentru sisteme neliniare – Jacobian"
# CERINTA: Aproximați Jacobianul sistemului F1=x2+y2−4, F2=ex+y−1 la punctul (1, 1.5) prin diferențe finite
# cu h=10−8.
#
# Formula diferențelor finite înainte (forward):
#   ∂F_i/∂x_j ≈ [F_i(x + h*e_j) - F_i(x)] / h
#
# Formula diferențelor finite centrate (mai precisă):
#   ∂F_i/∂x_j ≈ [F_i(x + h*e_j) - F_i(x - h*e_j)] / (2h)
# ============================================================

def F(v):
    """Sistemul neliniar:
    F1(x, y) = x² + y² - 4
    F2(x, y) = e^x + y - 1
    """
    x, y = v
    return np.array([x**2 + y**2 - 4,
                     np.exp(x) + y - 1])

# Punctul în care calculăm Jacobianul
p = np.array([1.0, 1.5])
h = 1e-8   # pasul mic pentru diferențe finite

print("Jacobianul numeric al sistemului F1=x²+y²-4, F2=eˣ+y-1")
print(f"La punctul (x, y) = ({p[0]}, {p[1]}), h = {h}\n")

# --- Metoda 1: Diferențe finite ÎNAINTE (forward differences) ---
# Curs: "eroare de trunchere O(h)" – mai puțin precisă
def jacobian_forward(F, x, h):
    """∂F_i/∂x_j ≈ [F(x + h*ej) - F(x)] / h"""
    n = len(x)
    J = np.zeros((n, n))
    f0 = F(x)             # F(x) calculat o singură dată
    for j in range(n):
        xh = x.copy()
        xh[j] += h        # perturbăm componenta j cu +h
        J[:, j] = (F(xh) - f0) / h
    return J

# --- Metoda 2: Diferențe finite CENTRATE (central differences) ---
# Curs: "eroare de trunchiere O(h²)" – mai precisă
def jacobian_central(F, x, h):
    """∂F_i/∂x_j ≈ [F(x + h*ej) - F(x - h*ej)] / (2h)"""
    n = len(x)
    J = np.zeros((n, n))
    for j in range(n):
        xp = x.copy(); xp[j] += h   # x + h*ej
        xm = x.copy(); xm[j] -= h   # x - h*ej
        J[:, j] = (F(xp) - F(xm)) / (2 * h)
    return J

J_fwd = jacobian_forward(F, p, h)
J_ctr = jacobian_central(F, p, h)

print("Jacobian (diferențe ÎNAINTE, forward):")
print(J_fwd)

print("\nJacobian (diferențe CENTRATE, central):")
print(J_ctr)

# --- Jacobianul analitic (pentru comparație) ---
# ∂F1/∂x = 2x,   ∂F1/∂y = 2y
# ∂F2/∂x = e^x,  ∂F2/∂y = 1
x, y = p
J_analitic = np.array([[2*x,        2*y],
                        [np.exp(x),  1.0]])

print("\nJacobian ANALITIC (exact):")
print(J_analitic)

# --- Comparație erori ---
eroare_fwd = np.max(np.abs(J_fwd - J_analitic))
eroare_ctr = np.max(np.abs(J_ctr - J_analitic))

print(f"\nEroarea max față de analitic:")
print(f"  Diferențe înainte (O(h)):   {eroare_fwd:.2e}")
print(f"  Diferențe centrate (O(h²)): {eroare_ctr:.2e}")
print(f"\nConcluzie: diferențele centrate sunt mult mai precise pentru același h!")

# --- Tabel element cu element ---
print(f"\n{'Element':>10}  {'Analitic':>14}  {'Fwd':>14}  {'Central':>14}")
print("-" * 58)
etichete = [("∂F1/∂x", 0,0), ("∂F1/∂y", 0,1), ("∂F2/∂x", 1,0), ("∂F2/∂y", 1,1)]
for label, i, j in etichete:
    print(f"{label:>10}  {J_analitic[i,j]:>14.10f}  {J_fwd[i,j]:>14.10f}  {J_ctr[i,j]:>14.10f}")