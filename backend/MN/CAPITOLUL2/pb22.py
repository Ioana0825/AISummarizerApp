"""
PROBLEMA 22 - Newton-Raphson pentru sistem 3x3 neliniar
========================================================
Capitol din curs: "Metode numerice pentru ecuatii neliniare"
                  Sectiunea: Metoda Newton-Raphson pentru sisteme

CERINTA: Rezolvați sistemul neliniar 3×3 (cu ecuații de tip polynomial și exponențial) pornind de la (1.0,
3.0, 1.0).

Sistemul de rezolvat (3 ecuatii, 3 necunoscute x, y, z):
  F1(x,y,z) = x^2 + y + z - 6 = 0
  F2(x,y,z) = x + y^2 - z - 4 = 0
  F3(x,y,z) = x + y + z^2 - 5 = 0

TEORIE (aceeasi ca la Problema 21, extinsa la 3 dimensiuni):
  Jacobianul 3x3:
      J = | dF1/dx  dF1/dy  dF1/dz |   =   | 2x  1   1  |
          | dF2/dx  dF2/dy  dF2/dz |       | 1   2y -1  |
          | dF3/dx  dF3/dy  dF3/dz |       | 1   1  2z  |

  La fiecare iteratie:
    1. Calculam F(x, y, z)    => vector de 3 elemente
    2. Calculam J(x, y, z)    => matrice 3x3
    3. Rezolvam J * delta = -F => vector delta de 3 elemente
    4. [x, y, z] = [x, y, z] + delta
"""

import numpy as np  # Necesara pentru array, linalg.solve, linalg.norm


def F(xyz):
    """
    Vectorul functiilor [F1, F2, F3] evaluat in punctul (x, y, z).
    """
    x, y, z = xyz[0], xyz[1], xyz[2]  # Extragem cele 3 necunoscute
    F1 = x ** 2 + y + z - 6  # Prima ecuatie
    F2 = x + y ** 2 - z - 4  # A doua ecuatie
    F3 = x + y + z ** 2 - 5  # A treia ecuatie
    return np.array([F1, F2, F3])  # Returnam ca vector numpy de 3 elemente


def J(xyz):
    """
    Jacobianul 3x3 evaluat in punctul (x, y, z).

    Derivate partiale:
      dF1/dx = 2x,  dF1/dy = 1,   dF1/dz = 1
      dF2/dx = 1,   dF2/dy = 2y,  dF2/dz = -1
      dF3/dx = 1,   dF3/dy = 1,   dF3/dz = 2z
    """
    x, y, z = xyz[0], xyz[1], xyz[2]
    return np.array([
        [2 * x, 1.0, 1.0],  # Randul 1: gradientul lui F1
        [1.0, 2 * y, -1.0],  # Randul 2: gradientul lui F2
        [1.0, 1.0, 2 * z]  # Randul 3: gradientul lui F3
    ])


# --- Parametrii problemei ---
xyz = np.array([1.0, 3.0, 1.0])  # Punct initial (x0, y0, z0) = (1, 3, 1)
eps = 1e-8  # Precizia dorita
max_iter = 50  # Protectie la bucle infinite

print(f"Sistemul neliniar 3x3:")
print(f"  F1 = x^2 + y + z - 6 = 0")
print(f"  F2 = x + y^2 - z - 4 = 0")
print(f"  F3 = x + y + z^2 - 5 = 0")
print(f"\nPunct initial: (x0, y0, z0) = ({xyz[0]}, {xyz[1]}, {xyz[2]})")
print(f"F(x0,y0,z0) = {F(xyz)}")
print()
print(f"{'Iter':>4} | {'x':>10} | {'y':>10} | {'z':>10} | {'||F||':>12} | {'||delta||':>12}")
print("-" * 65)

# --- Bucla principala Newton pentru sisteme 3x3 ---
for i in range(max_iter):
    Fval = F(xyz)  # Vectorul functiilor [F1, F2, F3]
    Jval = J(xyz)  # Jacobianul 3x3
    norma_F = np.linalg.norm(Fval)  # Norma: sqrt(F1^2 + F2^2 + F3^2)

    # Rezolvam sistemul linear 3x3: J * delta = -F
    # np.linalg.solve este echivalentul calcularii delta = J^(-1) * (-F)
    # (dar mai stabil numeric decat inversarea matricei!)
    delta = np.linalg.solve(Jval, -Fval)

    norma_delta = np.linalg.norm(delta)  # Marimea pasului

    print(f"{i + 1:>4} | {xyz[0]:>10.6f} | {xyz[1]:>10.6f} | {xyz[2]:>10.6f} | {norma_F:>12.2e} | {norma_delta:>12.2e}")

    # Actualizam solutia vectoriala
    xyz = xyz + delta

    # --- Criteriu de oprire ---
    if norma_delta < eps:
        break

# --- Rezultat final ---
print(f"\nSolutia gasita:")
print(f"  x = {xyz[0]:.8f}")
print(f"  y = {xyz[1]:.8f}")
print(f"  z = {xyz[2]:.8f}")
print(f"  Numar iteratii: {i + 1}")
print()
print(f"Verificare (valorile trebuie sa fie ~0):")
Ffinal = F(xyz)
print(f"  F1(x,y,z) = {Ffinal[0]:.2e}")
print(f"  F2(x,y,z) = {Ffinal[1]:.2e}")
print(f"  F3(x,y,z) = {Ffinal[2]:.2e}")
print()
print(f"Observatie: Aceeasi structura ca la sistemul 2x2 (Problema 21),")
print(f"  dar cu Jacobian 3x3 si vector F de 3 componente.")
print(f"  Codul este aproape identic - doar F() si J() se schimba!")