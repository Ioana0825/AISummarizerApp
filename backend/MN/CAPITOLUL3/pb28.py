"""
PROBLEMA 28 – Eliminarea Gauss cu pivotare – sistem 3x3 clasic
CERINTA: Rezolvați prin eliminare Gauss cu pivotare: 2x1 + x2 − x3 = 8, −3x1 − x2 + 2x3 = −11, −2x1 + x2
+ 2x3 = −3.
===============================================================
TEORIE (Curs: Capitol "Sisteme de Ecuatii Liniare – Metode Directe"):

Acelasi algoritm ca la Problema 23, dar pe un sistem 3x3 mai simplu,
ideal pentru a intelege mecanismul pas cu pas.

SISTEMUL:
   2*x1 +  x2 -  x3 =   8
  -3*x1 -  x2 + 2*x3 = -11
  -2*x1 +  x2 + 2*x3 =  -3

PASII ELIMINARII GAUSS:
  Pasul 1 (k=0): eliminam x1 din ecuatiile 2 si 3
    m21 = A[1][0]/A[0][0], R2 = R2 - m21*R1
    m31 = A[2][0]/A[0][0], R3 = R3 - m31*R1
  Pasul 2 (k=1): eliminam x2 din ecuatia 3
    m32 = A[2][1]/A[1][1], R3 = R3 - m32*R2
  => Obtinem sistem superior triunghiular => retrosubstitutie
"""

import numpy as np

# -----------------------------------------------------------------------
# Datele problemei
# -----------------------------------------------------------------------
A = np.array([
    [ 2,  1, -1],
    [-3, -1,  2],
    [-2,  1,  2]
], dtype=float)

b = np.array([8, -11, -3], dtype=float)

print("=" * 55)
print("PROBLEMA 28 – Eliminare Gauss cu pivotare (3x3)")
print("=" * 55)
print("\nSistemul initial:")
print("  2*x1 +  x2 -  x3 =  8")
print(" -3*x1 -  x2 + 2*x3 = -11")
print(" -2*x1 +  x2 + 2*x3 = -3")
print("\nMatricea A:\n", A)
print("Vectorul b:", b)

# -----------------------------------------------------------------------
# Eliminarea Gauss cu pivotare partiala – varianta detaliata pas cu pas
# -----------------------------------------------------------------------
n = len(b)
A = A.copy()     # lucram pe copii
b = b.copy()

for k in range(n):      # k = pasul curent (coloana de eliminat)

    # --- Pivotare partiala ---
    # Gasim randul cu cel mai mare element (in modul) in coloana k, de la randul k in jos
    max_idx = np.argmax(abs(A[k:, k])) + k
    if max_idx != k:
        # Facem swap intre randul k si randul max_idx
        A[[k, max_idx]] = A[[max_idx, k]]
        b[[k, max_idx]] = b[[max_idx, k]]
        print(f"\n  Pivotare: schimbam randul {k} cu randul {max_idx}")

    print(f"\n  === Pasul k={k} (pivot = A[{k},{k}] = {A[k,k]:.4f}) ===")

    # --- Eliminare: zeroul elementele de sub pivot ---
    for i in range(k + 1, n):
        if A[k, k] == 0:
            raise ValueError("Pivot zero – sistem singular!")
        # Factorul de eliminare: m = A[i][k] / A[k][k]
        m = A[i, k] / A[k, k]
        print(f"  m[{i},{k}] = A[{i},{k}]/A[{k},{k}] = {A[i,k]:.4f}/{A[k,k]:.4f} = {m:.4f}")

        # Actualizam randul i: R_i = R_i - m * R_k
        A[i, :] = A[i, :] - m * A[k, :]   # actualizam randul i din A
        b[i]    = b[i]    - m * b[k]       # actualizam termenul liber corespunzator
        print(f"  Dupa eliminare: A[{i}] = {A[i]}, b[{i}] = {b[i]:.4f}")

print("\nMatricea superior triunghiulara U:\n", np.round(A, 6))
print("Vectorul transformat y:", np.round(b, 6))

# -----------------------------------------------------------------------
# Retrosubstitutie (back substitution)
# -----------------------------------------------------------------------
print("\n--- Retrosubstitutie (de jos in sus) ---")
x = np.zeros(n)
for i in range(n - 1, -1, -1):               # de la ultima ecuatie la prima
    suma = np.dot(A[i, i+1:], x[i+1:])       # suma termenilor deja calculati
    x[i] = (b[i] - suma) / A[i, i]           # formula retrosubstitutiei
    print(f"  x[{i}] = ({b[i]:.4f} - {suma:.4f}) / {A[i,i]:.4f} = {x[i]:.6f}")

# -----------------------------------------------------------------------
# Rezultat si verificare
# -----------------------------------------------------------------------
print("\n" + "=" * 55)
print("SOLUTIA sistemului:")
print(f"  x1 = {x[0]:.6f}")
print(f"  x2 = {x[1]:.6f}")
print(f"  x3 = {x[2]:.6f}")

# Verificare cu matricea originala
A_orig = np.array([[2,1,-1],[-3,-1,2],[-2,1,2]], dtype=float)
b_orig = np.array([8,-11,-3], dtype=float)
print("\nVerificare A*x:", np.round(A_orig @ x, 6))
print("b original:    ", b_orig)
print("Reziduu ||Ax-b|| =", np.linalg.norm(A_orig @ x - b_orig))