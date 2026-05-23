"""
PROBLEMA 25 – Substitutie directa – sistem inferior triunghiular L*x = b
CERINTA: Rezolvați sistemul inferior triunghiular: L·x = b cu L = [[2,0,0],[3,4,0],[1,2,5]], b = [4, 11, 20].
=========================================================================
TEORIE (Curs: Capitol "Sisteme de Ecuatii Liniare – Substitutie directa"):

Un sistem inferior triunghiular are forma:
  L[0][0]*x[0]                                        = b[0]
  L[1][0]*x[0] + L[1][1]*x[1]                        = b[1]
  L[2][0]*x[0] + L[2][1]*x[1] + L[2][2]*x[2]        = b[2]
  ...

Se rezolva de SUS in JOS (forward substitution):
  x[0] = b[0] / L[0][0]
  x[1] = (b[1] - L[1][0]*x[0]) / L[1][1]
  x[2] = (b[2] - L[2][0]*x[0] - L[2][1]*x[1]) / L[2][2]

Formula generala:
  x[i] = (b[i] - sum_{j=0}^{i-1} L[i][j] * x[j]) / L[i][i]

Aceasta este COMPONENTA ESENTIALA in factorizarea LU (pasul Ly=b).
"""

import numpy as np

# -----------------------------------------------------------------------
# Datele problemei
# -----------------------------------------------------------------------
# Matricea inferior triunghiulara L
L = np.array([
    [2, 0, 0],   # prima linie: doar L[0][0] != 0
    [3, 4, 0],   # a doua linie: L[1][0] si L[1][1]
    [1, 2, 5]    # a treia linie: toate trei elementele
], dtype=float)

b = np.array([4, 11, 20], dtype=float)   # vectorul termenilor liberi

print("=" * 55)
print("PROBLEMA 25 – Substitutie directa (Forward Substitution)")
print("=" * 55)
print("\nMatricea L (inferior triunghiulara):\n", L)
print("Vectorul b:", b)

# -----------------------------------------------------------------------
# Substitutia directa pas cu pas (ca sa vedem ce se intampla)
# -----------------------------------------------------------------------
print("\n--- Rezolvare pas cu pas ---")
n = len(b)          # numarul de ecuatii
x = np.zeros(n)     # initializam solutia cu zerouri

for i in range(n):                          # parcurgem fiecare ecuatie de sus in jos
    suma = 0.0
    for j in range(i):                      # suma termenilor deja calculati (j < i)
        suma += L[i][j] * x[j]             # L[i][j] * x[j] deja cunoscut
    # Formula: x[i] = (b[i] - suma) / L[i][i]
    x[i] = (b[i] - suma) / L[i][i]

    # Afisam calculul pentru fiecare pas
    if i == 0:
        print(f"  x[0] = b[0] / L[0][0] = {b[0]} / {L[0][0]} = {x[0]:.6f}")
    else:
        detalii = " - ".join([f"L[{i}][{j}]*x[{j}]={L[i][j]*x[j]:.4f}" for j in range(i)])
        print(f"  x[{i}] = (b[{i}] - ({detalii})) / L[{i}][{i}]")
        print(f"       = ({b[i]} - {suma:.4f}) / {L[i][i]} = {x[i]:.6f}")

# -----------------------------------------------------------------------
# Rezultat si verificare
# -----------------------------------------------------------------------
print("\n" + "=" * 55)
print("SOLUTIA sistemului L*x = b:")
for i, xi in enumerate(x):
    print(f"  x{i+1} = {xi:.6f}")

# Verificare: L*x trebuie sa fie egal cu b
print("\nVerificare L*x =", np.round(L @ x, 6))
print("b original   =", b)
print("Reziduu ||L*x - b|| =", np.linalg.norm(L @ x - b))