"""
PROBLEMA 31 – Metoda Gauss-Seidel – sistem 3x3
CERINTA: Rezolvati prin Gauss-Seidel:
  5x1 + x2  + x3  = 10
  x1  + 7x2 - x3  = 12
  x1  - x2  + 6x3 =  8
  Start: x0 = (0, 0, 0)
================================================
TEORIE (Curs: Capitol "Metode Iterative – Python", pagina 72):

Metoda Gauss-Seidel este similara cu Jacobi, dar IMBUNATATITA:
  - La calculul lui x[i]^(k+1), folosim IMEDIAT valorile NOI deja calculate
    la acelasi pas k+1 (nu asteptam sa fie gata toate).

FORMULA:
  x[i]^(k+1) = (b[i] - sum_{j<i} A[i][j]*x[j]^(k+1)   <- valorile NOI
                       - sum_{j>i} A[i][j]*x[j]^(k) ) / A[i][i]
                                                          <- valorile VECHI

DIFERENTA FATA DE JACOBI:
  Jacobi:       x_nou[i] foloseste TOATE valorile VECHI din iteratia k
  Gauss-Seidel: x[i] foloseste imediat valorile NOI (j<i) + VECHI (j>i)
  => Gauss-Seidel converge mai rapid!

CONVERGENTA: Garantata daca A este DIAGONAL DOMINANTA:
       |A[i][i]| > sum_{j != i} |A[i][j]|  pentru orice i
"""

import numpy as np

# -----------------------------------------------------------------------
# Functia Gauss-Seidel – dupa modelul din curs (pagina 72)
# -----------------------------------------------------------------------
def gauss_seidel(A, b, eps=1e-6, max_iter=200):
    """Metoda iterativa Gauss-Seidel."""

    n = len(b)
    x = np.zeros(n)     # x(0) = aproximatia initiala = vectorul zero
    errors = []         # lista in care salvam eroarea la fiecare iteratie

    for k in range(1, max_iter + 1):
        x_old = x.copy()            # salvam valorile VECHI (pentru calculul erorii)

        for i in range(n):
            s = b[i]                # pornim suma cu termenul liber b[i]
            for j in range(n):
                if j != i:
                    # Diferenta cheie fata de Jacobi:
                    # pentru j < i: x[j] deja actualizat => folosim valoarea NOUA
                    # pentru j > i: x[j] inca neactualizat => folosim valoarea VECHE
                    # In ambele cazuri folosim x[j] curent (Python actualizeaza pe loc)
                    s -= A[i, j] * x[j]
            # Formula Gauss-Seidel: x[i] = s / A[i][i]
            x[i] = s / A[i, i]

        # Eroarea = norma infinit: max|x[i] - x_old[i]| pentru orice i
        err = np.max(np.abs(x - x_old))
        errors.append(err)          # salvam eroarea pentru aceasta iteratie

        # Criteriu de oprire: daca eroarea e mai mica decat toleranta, am converge
        if err < eps:
            return x, errors, k     # returnam solutia, erorile si numarul de iteratii

    return x, errors, max_iter      # am epuizat iteratiile fara convergenta

# -----------------------------------------------------------------------
# Datele problemei
# b = termenul drept din fiecare ecuatie:
#   5x1 + x2 + x3 = 10, ... = 12, ... = 8
# -----------------------------------------------------------------------
A = np.array([[5,  1,  1],
              [1,  7, -1],
              [1, -1,  6]], dtype=float)

b = np.array([10, 12, 8], dtype=float)

print("=== Metoda Gauss-Seidel ===\n")

# Verificare dominanta diagonala (conditie suficienta de convergenta)
print("Verificare diag. dominanta:")
for i in range(len(b)):
    diag = abs(A[i, i])                                          # elementul diagonal
    off  = sum(abs(A[i, j]) for j in range(len(b)) if j != i)   # suma restului
    print(f"  |a_{{{i+1}{i+1}}}| = {diag:.0f} > "
          f"{off:.0f} = suma_{{j!={i+1}}}|? {diag > off}")
print()

# Rezolvam cu Gauss-Seidel
x, errors, it = gauss_seidel(A, b)

print(f"Gauss-Seidel: x = {np.round(x, 6)},  iteratii: {it}")
print(f"\nSolutia exacta (numpy): {np.round(np.linalg.solve(A, b), 6)}")
print(f"Reziduu ||Ax - b|| = {np.linalg.norm(A @ x - b):.2e}")