import numpy as np

# ============================================================
# PROBLEMA 45 – Conducere termică 1D prin Diferențe Finite (FDM)
# Scop: rezolvăm ecuația -T''(x) = q(x) cu T(0)=T(1)=0
# Curs: Cap. "Aplicații inginerești – Diferențe finite"
# CERINTA: O bară de lungime L=1m are temperatura 0°C la capete. Există sursă de căldură
# q(x)=100·sin(πx). Găsiți distribuția staționară T(x) prin diferențe finite cu n=4 noduri interioare.x
#
# Discretizare:
#   Împărțim bara în n+1 intervale egale cu pasul h = L/(n+1)
#   Noduri interioare: x1, x2, ..., xn
#   Aproximăm T''(xi) ≈ [T(i-1) - 2T(i) + T(i+1)] / h²
#   Ecuația devine: -T(i-1) + 2T(i) - T(i+1) = h² * q(xi)
#   → sistem tridiagonal A * T = b
# ============================================================

L = 1.0        # lungimea barei [m]
n = 4          # număr noduri interioare
h = L / (n + 1)  # pasul de discretizare

print(f"Bară L={L}m, {n} noduri interioare, h={h}")

# Pozițiile nodurilor interioare (de la x1 la x4)
x = np.array([(i + 1) * h for i in range(n)])
print(f"Noduri x = {x}\n")

# --- Sursa de căldură la fiecare nod ---
# q(x) = 100 * sin(π*x)
q = 100 * np.sin(np.pi * x)

# --- Construim matricea tridiagonală A ---
# Diagonala principală: 2/h², diagonalele secundare: -1/h²
# Echivalent: -T(i-1) + 2T(i) - T(i+1) = h² * q(xi)
A = np.zeros((n, n))
for i in range(n):
    A[i, i] = 2           # termenul principal
    if i > 0:
        A[i, i-1] = -1    # termenul din stânga
    if i < n - 1:
        A[i, i+1] = -1    # termenul din dreapta

print("Matricea A (tridiagonală):")
print(A)

# --- Vectorul b = h² * q(xi) ---
# Condiții la limită T(0)=0 și T(L)=0 sunt automat incluse
# (nu adăugăm nimic la capete deoarece T_0=T_{n+1}=0)
b = h**2 * q

print(f"\nVectorul b = h²·q(xi):")
print(b)

# --- Rezolvăm sistemul A * T = b ---
T = np.linalg.solve(A, b)

print(f"\nTemperaturile la nodurile interioare:")
for i in range(n):
    print(f"  T(x={x[i]:.2f}) = {T[i]:.6f} °C")

# --- Soluția exactă (pentru comparație) ---
# -T''=100sin(πx) → T(x) = 100/π² * sin(πx)
T_exact = (100 / np.pi**2) * np.sin(np.pi * x)
print(f"\nSoluția exactă T(x) = 100/π²·sin(πx):")
for i in range(n):
    eroare = abs(T[i] - T_exact[i])
    print(f"  T_exact(x={x[i]:.2f}) = {T_exact[i]:.6f}, eroare = {eroare:.2e}")