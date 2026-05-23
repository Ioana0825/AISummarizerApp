import numpy as np

# ============================================================
# PROBLEMA 49 – Analiza circuitelor rezistive (Legile lui Kirchhoff)
# Scop: rezolvăm sistemul Ax = b obținut din legile Kirchhoff
# Curs: Cap. "Aplicații inginerești – Sisteme liniare"
# CERINTA: Prin legile lui Kirchhoff, circuitul rezistiv produce sistemul: [[3,−1,0],[−1,4,−1],[0,−1,2]]·I = [10,
# 0, 5]. Găsiți curenții.
#
# Legile lui Kirchhoff:
#   KCL (curenți): suma curenților într-un nod = 0
#   KVL (tensiuni): suma tensiunilor într-o buclă = 0
#
# Sistemul obținut:
#   3*I1 -   I2        = 10
#    -I1 + 4*I2 -   I3 = 0
#          -I2 + 2*I3  = 5
# ============================================================

# Matricea sistemului (rezistențele nodurilor)
A = np.array([[ 3, -1,  0],
              [-1,  4, -1],
              [ 0, -1,  2]], dtype=float)

# Vectorul termenilor liberi (sursele de tensiune/curent)
b = np.array([10, 0, 5], dtype=float)

print("Sistemul rezistiv (Kirchhoff):")
print("  3*I1 -   I2         = 10")
print("   -I1 + 4*I2 -   I3  = 0")
print("         -I2 + 2*I3   = 5")
print()
print("Matricea A =")
print(A)
print(f"\nVectorul b = {b}")

# --- Metoda 1: Eliminare Gauss (np.linalg.solve) ---
# Curs: Cap. "Eliminarea Gauss" – rezolvare directă
I = np.linalg.solve(A, b)

print(f"\n>>> Curenții găsiți (np.linalg.solve):")
print(f"  I1 = {I[0]:.6f} A")
print(f"  I2 = {I[1]:.6f} A")
print(f"  I3 = {I[2]:.6f} A")

# --- Verificare: A @ I trebuie să fie egal cu b ---
verificare = A @ I
print(f"\n[Verificare] A @ I = {verificare}")
print(f"[Verificare] b     = {b}")
print(f"[Verificare] Eroare = {np.max(np.abs(verificare - b)):.2e}")

# --- Metoda 2: Factorizare LU manuală (pentru ilustrare) ---
# Curs: Cap. "Factorizarea LU"
print("\n--- Rezolvare prin Factorizare LU (scipy) ---")
from scipy.linalg import lu_factor, lu_solve

lu, piv = lu_factor(A)    # factorizăm A = P*L*U
I_lu = lu_solve((lu, piv), b)   # rezolvăm Ly=Pb, Ux=y

print(f"  I1 = {I_lu[0]:.6f} A")
print(f"  I2 = {I_lu[1]:.6f} A")
print(f"  I3 = {I_lu[2]:.6f} A")

# --- Analiza circuitului ---
print(f"\n--- Analiza circuitului ---")
R = np.array([1/3, 1/4, 1/2])   # conductanțe echivalente (simplificat)
print(f"Curentul maxim este I1 = {I[0]:.4f} A (intrare din sursa de 10V)")
print(f"Curentul I3 = {I[2]:.4f} A (ieșire spre sursa de 5V)")
print(f"Puterea disipată (simplificat): P = b·I = {np.dot(b, I):.4f} W")