"""
PROBLEMA 21 - Newton-Raphson pentru sistem 2x2 neliniar
========================================================
Capitol din curs: "Metode numerice pentru ecuatii neliniare"
                  Sectiunea: Metoda Newton-Raphson pentru sisteme

CERINTA: Rezolvați sistemul: F1 = x2 + y2 − 4 = 0 și F2 = ex + y − 1 = 0, pornind de la (x0,y0) = (1, 1.5).

Sistemul de rezolvat:
  F1(x, y) = x^2 + y^2 - 4 = 0   (ecuatia unui cerc de raza 2)
  F2(x, y) = e^x + y - 1 = 0

TEORIE:
  La ecuatii scalare: x_{n+1} = x_n - f(x_n) / f'(x_n)
  La SISTEME generalizam: impartirea devine rezolvarea unui sistem linear!

  Jacobianul (matricea derivatelor partiale):
      J = | dF1/dx  dF1/dy |   =   | 2x   2y |
          | dF2/dx  dF2/dy |       | e^x   1  |

  Algoritmul la fiecare pas:
    1. Calculam F(x_n, y_n) = [F1, F2]
    2. Calculam J(x_n, y_n) = matricea 2x2
    3. Rezolvam sistemul linear: J * delta = -F
    4. Actualizam: [x, y] = [x, y] + delta

  Convergenta: tot patratica ca la scalara!
"""

import numpy as np  # Necesara pentru exp, array, linalg.solve


def F(xy):
    """
    Vectorul functiilor [F1, F2] evaluat in punctul (x, y).
    Returneaza un vector numpy de 2 elemente.
    """
    x, y = xy[0], xy[1]  # Extragem x si y din vectorul xy
    F1 = x ** 2 + y ** 2 - 4  # Ecuatia cercului de raza 2
    F2 = np.exp(x) + y - 1  # Ecuatia transcendenta
    return np.array([F1, F2])  # Returnam ca vector (array) numpy


def J(xy):
    """
    Jacobianul J(x, y) = matricea 2x2 a derivatelor partiale.

    J = | dF1/dx  dF1/dy |   =   | 2x   2y |
        | dF2/dx  dF2/dy |       | e^x   1  |

    Derivatele:
      dF1/dx = 2x,    dF1/dy = 2y
      dF2/dx = e^x,   dF2/dy = 1
    """
    x, y = xy[0], xy[1]
    return np.array([
        [2 * x, 2 * y],  # Primul rand: derivatele lui F1
        [np.exp(x), 1.0]  # Al doilea rand: derivatele lui F2
    ])


# --- Parametrii problemei ---
xy = np.array([1.0, 1.5])  # Punct initial (x0, y0) = (1, 1.5)
eps = 1e-6  # Precizia dorita
max_iter = 20  # Protectie la bucle infinite

print(f"Sistemul neliniar 2x2:")
print(f"  F1 = x^2 + y^2 - 4 = 0  (cerc de raza 2)")
print(f"  F2 = e^x + y - 1 = 0")
print(f"\nPunct initial: (x0, y0) = ({xy[0]}, {xy[1]})")
print(f"F(x0, y0) = {F(xy)}")
print()
print(f"{'Iter':>4} | {'x':>12} | {'y':>12} | {'||F||':>12} | {'||delta||':>12}")
print("-" * 60)

# --- Bucla principala Newton pentru sisteme ---
for i in range(max_iter):
    Fval = F(xy)  # Vectorul functiilor in punctul curent
    Jval = J(xy)  # Jacobianul in punctul curent
    norma_F = np.linalg.norm(Fval)  # Norma euclidiana a vectorului F: sqrt(F1^2+F2^2)

    # Rezolvam sistemul linear: J * delta = -F
    # np.linalg.solve rezolva Ax = b => gaseste delta astfel incat J*delta = -F
    delta = np.linalg.solve(Jval, -Fval)

    norma_delta = np.linalg.norm(delta)  # Marimea pasului

    print(f"{i + 1:>4} | {xy[0]:>12.8f} | {xy[1]:>12.8f} | {norma_F:>12.2e} | {norma_delta:>12.2e}")

    # Actualizam solutia: x_nou = x_vechi + delta
    xy = xy + delta

    # --- Criteriu de oprire: pasul e suficient de mic ---
    if norma_delta < eps:
        break

# --- Rezultat final ---
print(f"\nSolutia gasita:")
print(f"  x = {xy[0]:.8f}")
print(f"  y = {xy[1]:.8f}")
print(f"  Numar iteratii: {i + 1}")
print()
print(f"Verificare:")
print(f"  F1(x,y) = x^2 + y^2 - 4 = {xy[0] ** 2 + xy[1] ** 2 - 4:.2e}  (≈ 0 ✓)")
print(f"  F2(x,y) = e^x + y - 1   = {np.exp(xy[0]) + xy[1] - 1:.2e}  (≈ 0 ✓)")