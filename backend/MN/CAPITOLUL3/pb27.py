"""
PROBLEMA 27 – Metoda Jacobi – sistem 4x4 diagonal dominant
CERINTA: Rezolvati prin metoda Jacobi sistemul:
  10x1 - x2  + 2x3        =  6
  -x1  + 11x2 - x3 + 3x4  = 25
  2x1  - x2  + 10x3 - x4  = -11
         3x2  - x3  + 8x4 = 15
============================================================
TEORIE (Curs: Capitol "Metode Iterative – Python", pagina 72):

Metoda Jacobi este o metoda ITERATIVA: porneste dintr-o aproximatie initiala
x(0) si calculeaza iteratii x(1), x(2), ... pana la convergenta.

IDEEA: Din ecuatia i: sum_j A[i][j]*x[j] = b[i]
       izolam x[i]:
       x[i]^(k+1) = (b[i] - sum_{j != i} A[i][j] * x[j]^(k)) / A[i][i]

Adica: la iteratia k+1, calculam TOATE componentele noi x[i]^(k+1)
       folosind DOAR valorile VECHI x[j]^(k).

CONVERGENTA: Garantata daca A este DIAGONAL DOMINANTA:
       |A[i][i]| > sum_{j != i} |A[i][j]|  pentru orice i
"""

import numpy as np

# -----------------------------------------------------------------------
# Functia Jacobi – dupa modelul din curs (pagina 72)
# -----------------------------------------------------------------------
def jacobi(A, b, eps=1e-6, max_iter=200):
    """Metoda iterativa Jacobi."""

    n = len(b)
    x = np.zeros(n)     # x(0) = aproximatia initiala = vectorul zero
    errors = []         # lista in care salvam eroarea la fiecare iteratie

    for k in range(1, max_iter + 1):
        x_new = np.zeros(n)         # alocam vectorul pentru iteratia k+1

        for i in range(n):
            # np.dot(A[i,:], x) calculeaza intregul produs scalar A[i]*x
            # din care scadem A[i,i]*x[i] ca sa excludem termenul diagonal
            # => obtinem suma A[i][j]*x[j] pentru j != i (valorile VECHI)
            s = b[i] - np.dot(A[i, :], x) + A[i, i] * x[i]
            # Formula Jacobi: x_new[i] = s / A[i][i]
            x_new[i] = s / A[i, i]

        # Eroarea = norma infinit: max|x_new[i] - x[i]| pentru orice i
        err = np.max(np.abs(x_new - x))
        errors.append(err)          # salvam eroarea pentru aceasta iteratie
        x = x_new.copy()            # actualizam x cu noile valori

        # Criteriu de oprire: daca eroarea e mai mica decat toleranta, am converge
        if err < eps:
            return x, errors, k     # returnam solutia, erorile si numarul de iteratii

    return x, errors, max_iter      # am epuizat iteratiile fara convergenta

# -----------------------------------------------------------------------
# Datele problemei
# b = termenul drept din fiecare ecuatie:
#   10x1 - x2 + 2x3 = 6, ... = 25, ... = -11, ... = 15
# -----------------------------------------------------------------------
A = np.array([[10, -1,  2,  0],
              [-1, 11, -1,  3],
              [ 2, -1, 10, -1],
              [ 0,  3, -1,  8]], dtype=float)

b = np.array([6, 25, -11, 15], dtype=float)

print("=== Metoda Jacobi ===\n")

# Verificare dominanta diagonala (conditie suficienta de convergenta)
print("Verificare diag. dominanta:")
for i in range(len(b)):
    diag = abs(A[i, i])                                          # elementul diagonal
    off  = sum(abs(A[i, j]) for j in range(len(b)) if j != i)   # suma restului
    print(f"  |a_{{{i+1}{i+1}}}| = {diag:.0f} > "
          f"{off:.0f} = suma_{{j!={i+1}}}|? {diag > off}")
print()

# Rezolvam cu Jacobi
x, errors, it = jacobi(A, b)

print(f"Jacobi: x = {np.round(x, 6)},  iteratii: {it}")
print(f"\nSolutia exacta (numpy): {np.round(np.linalg.solve(A, b), 6)}")
print(f"Reziduu ||Ax - b|| = {np.linalg.norm(A @ x - b):.2e}")