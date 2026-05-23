"""
PROBLEMA 24 – Factorizarea LU (Crout) – sistem 4x4
CERINTA: Aplicați factorizarea LU (Crout) matricei A = [[4,1,−1,1],[1,5,2,0],[−1,2,6,1],[1,0,1,4]], și
rezolvați Ax = b prin Ly = b și Ux = y.
====================================================
TEORIE (Curs: Capitol "Sisteme de Ecuatii Liniare – Factorizarea LU"):

Factorizarea LU descompune matricea A = L * U unde:
  - L = matrice inferior triunghiulara (lower) cu 1 pe diagonala (Doolittle)
        sau elemente arbitrare pe diagonala (Crout)
  - U = matrice superior triunghiulara (upper)

ALGORITMUL CROUT:
  Elementele lui L si U se calculeaza coloana cu coloana:

  U[k][j] = A[k][j] - sum(L[k][s] * U[s][j], s=0..k-1)   pentru j >= k
  L[i][k] = (A[i][k] - sum(L[i][s] * U[s][k], s=0..k-1)) / U[k][k]  pentru i > k

REZOLVAREA sistemului Ax = b devine doua sisteme triunghiulare:
  1. L * y = b  => y prin substitutie directa (forward substitution)
  2. U * x = y  => x prin retrosubstitutie (back substitution)

AVANTAJ: Daca avem mai multi vectori b, factorizarea LU se face o singura data!
"""

import numpy as np

# -----------------------------------------------------------------------
# Datele problemei
# -----------------------------------------------------------------------
A = np.array([
    [ 4,  1, -1,  1],
    [ 1,  5,  2,  0],
    [-1,  2,  6,  1],
    [ 1,  0,  1,  4]
], dtype=float)

b = np.array([12, 8, 19, 11], dtype=float)

print("=" * 55)
print("PROBLEMA 24 – Factorizarea LU (Crout)")
print("=" * 55)
print("\nMatricea A:\n", A)
print("Vectorul b:", b)

# -----------------------------------------------------------------------
# PASUL 1: Factorizarea LU (Crout)
# -----------------------------------------------------------------------
def factorizare_lu_crout(A):
    """
    Realizeaza factorizarea LU (Crout) a matricei A.
    Returneaza matricele L si U astfel incat A = L * U.
    """
    n = len(A)
    L = np.zeros((n, n))    # initializam L cu zerouri
    U = np.zeros((n, n))    # initializam U cu zerouri

    for k in range(n):      # parcurgem fiecare coloana k

        # --- Calculam elementele din U pe randul k ---
        # Formula: U[k][j] = A[k][j] - sum_{s=0}^{k-1} L[k][s] * U[s][j]
        for j in range(k, n):
            suma = sum(L[k][s] * U[s][j] for s in range(k))  # suma produselor anterioare
            U[k][j] = A[k][j] - suma   # elementul din U

        # --- Calculam elementele din L pe coloana k ---
        # Diagonala lui L: L[k][k] = 1 (conventie Doolittle)
        L[k][k] = 1.0

        # Formula: L[i][k] = (A[i][k] - sum_{s=0}^{k-1} L[i][s] * U[s][k]) / U[k][k]
        for i in range(k + 1, n):
            suma = sum(L[i][s] * U[s][k] for s in range(k))  # suma produselor anterioare
            L[i][k] = (A[i][k] - suma) / U[k][k]  # impartim la elementul pivot U[k][k]

    return L, U

L, U = factorizare_lu_crout(A)

print("\nMatricea L (inferior triunghiulara):\n", np.round(L, 6))
print("\nMatricea U (superior triunghiulara):\n", np.round(U, 6))
print("\nVerificare L * U = A:\n", np.round(L @ U, 6))

# -----------------------------------------------------------------------
# PASUL 2: Substitutie directa – rezolvam L * y = b
# -----------------------------------------------------------------------
# Formula forward: y[i] = (b[i] - sum_{j=0}^{i-1} L[i][j] * y[j]) / L[i][i]
def substitutie_directa(L, b):
    """Rezolva L * y = b prin substitutie directa (forward substitution)."""
    n = len(b)
    y = np.zeros(n)             # initializam y cu zerouri
    for i in range(n):          # parcurgem de sus in jos
        suma = np.dot(L[i, :i], y[:i])         # suma termenilor deja calculati
        y[i] = (b[i] - suma) / L[i, i]         # formula substitutiei directe
    return y

# -----------------------------------------------------------------------
# PASUL 3: Retrosubstitutie – rezolvam U * x = y
# -----------------------------------------------------------------------
# Formula back: x[i] = (y[i] - sum_{j=i+1}^{n-1} U[i][j] * x[j]) / U[i][i]
def retrosubstitutie(U, y):
    """Rezolva U * x = y prin retrosubstitutie (back substitution)."""
    n = len(y)
    x = np.zeros(n)                    # initializam x cu zerouri
    for i in range(n - 1, -1, -1):    # parcurgem de jos in sus
        suma = np.dot(U[i, i+1:], x[i+1:])     # suma termenilor deja calculati
        x[i] = (y[i] - suma) / U[i, i]         # formula retrosubstitutiei
    return x

y = substitutie_directa(L, b)
x = retrosubstitutie(U, y)

print("\n" + "=" * 55)
print("Vectorul intermediar y (din L*y=b):", np.round(y, 6))
print("\nSOLUTIA sistemului (din U*x=y):")
for i, xi in enumerate(x):
    print(f"  x{i+1} = {xi:.6f}")

# Verificare finala
print("\nVerificare ||A*x - b|| =", np.linalg.norm(A @ x - b))