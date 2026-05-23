"""
PROBLEMA 29 – Factorizarea LU (Crout) – sistem 3x3
CERINTA: Aplicați factorizarea LU (Crout) matricei A = [[3,1,1],[1,4,1],[1,1,5]] cu b = [1,2,3].
====================================================
TEORIE (Curs: Capitol "Sisteme de Ecuatii Liniare – Factorizarea LU"):

Acelasi algoritm ca la Problema 24, aplicat pe un sistem mai simplu 3x3.
Util pentru a verifica calculul manual.

A = [[3,1,1],[1,4,1],[1,1,5]], b = [1,2,3]

Calculul LU Crout pas cu pas:
  Coloana k=0:
    U[0][0] = A[0][0] = 3
    U[0][1] = A[0][1] = 1
    U[0][2] = A[0][2] = 1
    L[0][0] = 1  (diagonala lui L = 1 in Doolittle)
    L[1][0] = A[1][0] / U[0][0] = 1/3
    L[2][0] = A[2][0] / U[0][0] = 1/3

  Coloana k=1:
    U[1][1] = A[1][1] - L[1][0]*U[0][1] = 4 - (1/3)*1 = 11/3
    U[1][2] = A[1][2] - L[1][0]*U[0][2] = 1 - (1/3)*1 = 2/3
    L[1][1] = 1
    L[2][1] = (A[2][1] - L[2][0]*U[0][1]) / U[1][1] = (1 - 1/3) / (11/3) = (2/3)/(11/3) = 2/11

  Coloana k=2:
    U[2][2] = A[2][2] - L[2][0]*U[0][2] - L[2][1]*U[1][2]
            = 5 - (1/3)*1 - (2/11)*(2/3)
    L[2][2] = 1
"""

import numpy as np

# -----------------------------------------------------------------------
# Datele problemei
# -----------------------------------------------------------------------
A = np.array([
    [3, 1, 1],
    [1, 4, 1],
    [1, 1, 5]
], dtype=float)

b = np.array([1, 2, 3], dtype=float)

print("=" * 55)
print("PROBLEMA 29 – Factorizarea LU (Crout) 3x3")
print("=" * 55)
print("\nMatricea A:\n", A)
print("Vectorul b:", b)

# -----------------------------------------------------------------------
# PASUL 1: Factorizare LU Crout cu afisare pas cu pas
# -----------------------------------------------------------------------
n = len(A)
L = np.zeros((n, n))    # L = matrice inferior triunghiulara (initializam cu 0)
U = np.zeros((n, n))    # U = matrice superior triunghiulara (initializam cu 0)

print("\n--- Factorizare LU Crout ---")
for k in range(n):
    print(f"\n  Coloana k={k}:")

    # Calculam elementele din U pe randul k (partea superior triunghiulara)
    for j in range(k, n):
        # U[k][j] = A[k][j] - suma_{s=0}^{k-1} L[k][s] * U[s][j]
        suma = sum(L[k][s] * U[s][j] for s in range(k))
        U[k][j] = A[k][j] - suma
        print(f"    U[{k}][{j}] = A[{k}][{j}] - suma = {A[k][j]} - {suma:.4f} = {U[k][j]:.4f}")

    # Diagonala lui L = 1 (conventie Doolittle)
    L[k][k] = 1.0
    print(f"    L[{k}][{k}] = 1.0  (diagonala)")

    # Calculam elementele din L sub diagonala pe coloana k
    for i in range(k + 1, n):
        # L[i][k] = (A[i][k] - suma_{s=0}^{k-1} L[i][s] * U[s][k]) / U[k][k]
        suma = sum(L[i][s] * U[s][k] for s in range(k))
        L[i][k] = (A[i][k] - suma) / U[k][k]
        print(f"    L[{i}][{k}] = ({A[i][k]} - {suma:.4f}) / {U[k][k]:.4f} = {L[i][k]:.4f}")

print("\nMatricea L:\n", np.round(L, 6))
print("Matricea U:\n", np.round(U, 6))
print("\nVerificare L*U:\n", np.round(L @ U, 6))
print("Matricea A originala:\n", A)

# -----------------------------------------------------------------------
# PASUL 2: Substitutie directa – L*y = b
# -----------------------------------------------------------------------
# x[i] = (b[i] - sum_{j<i} L[i][j]*y[j]) / L[i][i]
y = np.zeros(n)
print("\n--- Substitutie directa: L*y = b ---")
for i in range(n):
    suma = np.dot(L[i, :i], y[:i])       # suma termenilor deja calculati
    y[i] = (b[i] - suma) / L[i][i]       # formula forward substitution
    print(f"  y[{i}] = ({b[i]} - {suma:.4f}) / {L[i][i]:.4f} = {y[i]:.6f}")

# -----------------------------------------------------------------------
# PASUL 3: Retrosubstitutie – U*x = y
# -----------------------------------------------------------------------
# x[i] = (y[i] - sum_{j>i} U[i][j]*x[j]) / U[i][i]
x = np.zeros(n)
print("\n--- Retrosubstitutie: U*x = y ---")
for i in range(n - 1, -1, -1):
    suma = np.dot(U[i, i+1:], x[i+1:])   # suma termenilor deja calculati
    x[i] = (y[i] - suma) / U[i][i]        # formula back substitution
    print(f"  x[{i}] = ({y[i]:.4f} - {suma:.4f}) / {U[i][i]:.4f} = {x[i]:.6f}")

# -----------------------------------------------------------------------
# Rezultat si verificare
# -----------------------------------------------------------------------
print("\n" + "=" * 55)
print("SOLUTIA sistemului:")
for i, xi in enumerate(x):
    print(f"  x{i+1} = {xi:.6f}")

print("\nVerificare ||A*x - b|| =", np.linalg.norm(A @ x - b))
print("Solutia numpy (referinta):", np.round(np.linalg.solve(A, b), 6))