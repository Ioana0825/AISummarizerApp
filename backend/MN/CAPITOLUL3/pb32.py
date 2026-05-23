"""
PROBLEMA 32 – Factorizarea Cholesky – matrice simetrica pozitiv definita
CERINTA: Verificati ca A = [[6,2,1],[2,5,2],[1,2,4]] este simetrica pozitiv
definita si aplicati factorizarea Cholesky.
=========================================================================
TEORIE (Curs: Capitol "Sisteme de Ecuatii Liniare – Factorizarea Cholesky"):

Factorizarea Cholesky se aplica NUMAI matricelor:
  (1) SIMETRICE:        A = A^T
  (2) POZITIV DEFINITE: toate valorile proprii sunt STRICT POZITIVE

DESCOMPUNEREA: A = L * L^T
  unde L este matrice inferior triunghiulara cu elemente POZITIVE pe diagonala.

FORMULELE DIN CURS:
  Diagonala:  l_ii = sqrt( a_ii - sum_{k=1}^{i-1} l_ik^2 )
  Sub diag.:  l_ij = (1/l_jj) * ( a_ij - sum_{k=1}^{j-1} l_ik * l_jk ),  i > j

  Nota: in Python indexarea incepe de la 0, deci:
    - "sum de la k=1 la i-1" devine "sum de la k=0 la i-1" (range(i))
    - "sum de la k=1 la j-1" devine "sum de la k=0 la j-1" (range(j))

REZOLVAREA Ax=b: A = L*L^T =>
  1. L  * y = b   (substitutie directa   – forward)
  2. L^T * x = y  (retrosubstitutie      – backward)
"""

import numpy as np

# -----------------------------------------------------------------------
# Datele problemei
# -----------------------------------------------------------------------
A = np.array([
    [6, 2, 1],
    [2, 5, 2],
    [1, 2, 4]
], dtype=float)

b = np.array([9, 9, 7], dtype=float)

print("=== Factorizarea Cholesky ===\n")

# -----------------------------------------------------------------------
# VERIFICARE: A este simetrica si pozitiv definita?
# -----------------------------------------------------------------------
print("Verificare A simetrica:")
print(f"  A == A^T: {np.allclose(A, A.T)}\n")        # True daca A = A transpusa

print("Verificare A pozitiv definita (valori proprii > 0):")
valori_proprii = np.linalg.eigvals(A)                 # calculam valorile proprii
print(f"  Valori proprii: {np.round(valori_proprii, 4)}")
print(f"  Toate > 0? {all(valori_proprii > 0)}\n")

# -----------------------------------------------------------------------
# FACTORIZAREA CHOLESKY: A = L * L^T
# Formulele din curs (indexare Python de la 0):
#   l_ii = sqrt( a_ii - sum_{k=0}^{i-1} l_ik^2 )
#   l_ij = (a_ij - sum_{k=0}^{j-1} l_ik * l_jk) / l_jj,   i > j
# -----------------------------------------------------------------------
def cholesky(A):
    """Factorizarea Cholesky: A = L * L^T"""
    n = len(A)
    L = np.zeros((n, n))    # initializam L cu zerouri

    for i in range(n):      # i = randul curent (parcurgem fiecare rand)

        # --- Formula 1: elementul DIAGONAL l_ii ---
        # l_ii = sqrt( a_ii - sum_{k=0}^{i-1} l_ik^2 )
        # Scadem suma patratelor elementelor deja calculate pe randul i
        suma_diag = sum(L[i, k]**2 for k in range(i))   # sum l_ik^2, k=0..i-1
        L[i, i] = np.sqrt(A[i, i] - suma_diag)
        print(f"  l_{i+1}{i+1} = sqrt({A[i,i]:.4f} - {suma_diag:.4f}) = {L[i,i]:.6f}")

        # --- Formula 2: elementele SUB DIAGONALA l_ij, cu i > j ---
        # l_ij = (a_ij - sum_{k=0}^{j-1} l_ik * l_jk) / l_jj
        # Parcurgem coloanele j de la 0 pana la i-1 (sub diagonala)
        for j in range(i + 1, n):
            # Scadem suma produselor elementelor deja calculate
            suma_subdiag = sum(L[j, k] * L[i, k] for k in range(i))  # sum l_jk*l_ik, k=0..i-1
            L[j, i] = (A[j, i] - suma_subdiag) / L[i, i]
            print(f"  l_{j+1}{i+1} = ({A[j,i]:.4f} - {suma_subdiag:.4f}) / {L[i,i]:.4f} = {L[j,i]:.6f}")

    return L

L = cholesky(A)

print(f"\nMatricea L:\n{np.round(L, 6)}")
print(f"\nVerificare L * L^T:\n{np.round(L @ L.T, 6)}")
print(f"\nL * L^T == A? {np.allclose(L @ L.T, A)}")

# -----------------------------------------------------------------------
# Rezolvam A*x = b prin L*y=b si L^T*x=y
# -----------------------------------------------------------------------
print(f"\n--- Rezolvam A*x = b cu b = {b} ---\n")

n = len(b)

# Pasul 1: Substitutie directa L * y = b (forward substitution)
# y[i] = (b[i] - sum_{k=0}^{i-1} L[i,k]*y[k]) / L[i,i]
y = np.zeros(n)
for i in range(n):
    suma = np.dot(L[i, :i], y[:i])      # sum L[i,k]*y[k], k=0..i-1
    y[i] = (b[i] - suma) / L[i, i]

print(f"  y (din L*y=b):    {np.round(y, 6)}")

# Pasul 2: Retrosubstitutie L^T * x = y (back substitution)
# x[i] = (y[i] - sum_{k=i+1}^{n-1} L^T[i,k]*x[k]) / L^T[i,i]
LT = L.T                                # L^T = transpusa lui L (superior triunghiulara)
x = np.zeros(n)
for i in range(n - 1, -1, -1):
    suma = np.dot(LT[i, i+1:], x[i+1:])    # sum LT[i,k]*x[k], k=i+1..n-1
    x[i] = (y[i] - suma) / LT[i, i]

print(f"  x (din L^T*x=y):  {np.round(x, 6)}")

# -----------------------------------------------------------------------
# Rezultat si verificare
# -----------------------------------------------------------------------
print(f"\nSolutia: x = {np.round(x, 6)}")
print(f"Solutia exacta (numpy): {np.round(np.linalg.solve(A, b), 6)}")
print(f"Reziduu ||Ax - b|| = {np.linalg.norm(A @ x - b):.2e}")