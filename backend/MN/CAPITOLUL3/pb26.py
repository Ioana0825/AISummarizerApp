"""
PROBLEMA 26 – Retrosubstitutie – sistem superior triunghiular U*x = y
CERINTA: Rezolvați sistemul superior triunghiular: U·x = y cu U = [[2,3,−1],[0,4,2],[0,0,5]], y = [5, 10, 15].
=======================================================================
TEORIE (Curs: Capitol "Sisteme de Ecuatii Liniare – Retrosubstitutie"):

Un sistem superior triunghiular are forma:
  U[0][0]*x[0] + U[0][1]*x[1] + U[0][2]*x[2] = y[0]
              U[1][1]*x[1] + U[1][2]*x[2]     = y[1]
                             U[2][2]*x[2]      = y[2]

Se rezolva de JOS in SUS (back substitution):
  x[n-1] = y[n-1] / U[n-1][n-1]
  x[i]   = (y[i] - sum_{j=i+1}^{n-1} U[i][j] * x[j]) / U[i][i]

Aceasta este COMPONENTA ESENTIALA in:
  - Eliminarea Gauss (pasul final dupa triangularizare)
  - Factorizarea LU (pasul Ux=y dupa ce y e cunoscut)

ATENTIE: Rezolvam de la ultima ecuatie spre prima!
"""

import numpy as np

# -----------------------------------------------------------------------
# Datele problemei
# -----------------------------------------------------------------------
# Matricea superior triunghiulara U
U = np.array([
    [2, 3, -1],   # prima linie: toate trei elementele
    [0, 4,  2],   # a doua linie: U[1][1] si U[1][2]
    [0, 0,  5]    # a treia linie: doar U[2][2] != 0
], dtype=float)

y = np.array([5, 10, 15], dtype=float)   # vectorul termenilor liberi (de obicei numit y)

print("=" * 55)
print("PROBLEMA 26 – Retrosubstitutie (Back Substitution)")
print("=" * 55)
print("\nMatricea U (superior triunghiulara):\n", U)
print("Vectorul y:", y)

# -----------------------------------------------------------------------
# Retrosubstitutia pas cu pas (ca sa vedem ce se intampla)
# -----------------------------------------------------------------------
print("\n--- Rezolvare pas cu pas (de jos in sus) ---")
n = len(y)          # numarul de ecuatii
x = np.zeros(n)     # initializam solutia cu zerouri

for i in range(n - 1, -1, -1):         # parcurgem de la n-1 PANA LA 0 (invers!)
    suma = 0.0
    for j in range(i + 1, n):          # suma termenilor deja calculati (j > i)
        suma += U[i][j] * x[j]         # U[i][j] * x[j] deja cunoscut
    # Formula: x[i] = (y[i] - suma) / U[i][i]
    x[i] = (y[i] - suma) / U[i][i]

    # Afisam calculul pentru fiecare pas
    if i == n - 1:
        print(f"  x[{i}] = y[{i}] / U[{i}][{i}] = {y[i]} / {U[i][i]} = {x[i]:.6f}")
    else:
        detalii = " - ".join([f"U[{i}][{j}]*x[{j}]={U[i][j]*x[j]:.4f}" for j in range(i+1, n)])
        print(f"  x[{i}] = (y[{i}] - ({detalii})) / U[{i}][{i}]")
        print(f"       = ({y[i]} - {suma:.4f}) / {U[i][i]} = {x[i]:.6f}")

# -----------------------------------------------------------------------
# Rezultat si verificare
# -----------------------------------------------------------------------
print("\n" + "=" * 55)
print("SOLUTIA sistemului U*x = y:")
for i, xi in enumerate(x):
    print(f"  x{i+1} = {xi:.6f}")

# Verificare: U*x trebuie sa fie egal cu y
print("\nVerificare U*x =", np.round(U @ x, 6))
print("y original   =", y)
print("Reziduu ||U*x - y|| =", np.linalg.norm(U @ x - y))