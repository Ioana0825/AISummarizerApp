"""
PROBLEMA 41 - Metoda Euler pentru ecuatii diferentiale ordinare (EDO)
CERINTA: Rezolvați y' = y − t2 + 1, y(0) = 0.5 pe [0, 2] cu metoda Euler, h = 0.5. Soluția exactă: y = (t+1)2
− 0.5et.
======================================================================
TEORIE (Curs - Capitol: Rezolvarea Numerica a EDO):
  Problema Cauchy (Cauchy Initial Value Problem):
      y' = f(t, y),   y(t0) = y0

  Metoda Euler (ordinul 1) - cea mai simpla metoda:
  Pornind din (t0, y0), facem pasi mici de marime h:

      y_{n+1} = y_n + h * f(t_n, y_n)

  Intuitie: aproximam panta cu derivata curenta, mergem in directia tangentei.

  EROAREA locala: O(h^2)  => eroarea globala: O(h)  (ordin 1)
  => Euler e simplu dar nu foarte precis; pentru precizie mai buna: RK4!

Problema: y' = y - t^2 + 1,  y(0) = 0.5,  pe [0, 2],  h = 0.5
Solutia exacta: y(t) = (t+1)^2 - 0.5*e^t
"""

import math

# -------------------------------------------------------
# PASUL 1: Definim functia EDO si solutia exacta
# -------------------------------------------------------
# Ecuatia diferentiala: y' = f(t, y)
def f(t, y):
    return y - t**2 + 1    # f(t, y) = y - t^2 + 1

# Solutia analitica exacta (pentru verificare)
def y_exact(t):
    return (t + 1)**2 - 0.5 * math.exp(t)   # (t+1)^2 - 0.5*e^t

# -------------------------------------------------------
# PASUL 2: Parametrii problemei
# -------------------------------------------------------
t0 = 0.0    # momentul initial
y0 = 0.5    # conditia initiala: y(0) = 0.5
h  = 0.5    # pasul de integrare
t_final = 2.0   # momentul final

# Calculam numarul de pasi
n_pasi = int((t_final - t0) / h)    # = (2-0)/0.5 = 4 pasi

print("=== PROBLEMA 41 - Metoda Euler ===")
print(f"EDO: y' = y - t^2 + 1,  y(0) = {y0}")
print(f"Interval: [{t0}, {t_final}],  h = {h},  {n_pasi} pasi")
print()
print(f"{'Pasul':>5} {'t':>8} {'y_Euler':>12} {'y_exact':>12} {'Eroare':>12}")
print("-" * 55)

# -------------------------------------------------------
# PASUL 3: Aplicam metoda Euler pas cu pas
# Formula: y_{n+1} = y_n + h * f(t_n, y_n)
# -------------------------------------------------------
t = t0    # momentul curent, incepem de la t0
y = y0    # valoarea curenta, incepem de la y0

# Afisam conditia initiala
print(f"{'0':>5} {t:>8.4f} {y:>12.6f} {y_exact(t):>12.6f} {abs(y - y_exact(t)):>12.2e}")

for i in range(n_pasi):
    # Panta curenta (derivata la momentul t cu valoarea y)
    panta = f(t, y)

    # Pasul Euler: mergem in directia pantei cu lungimea h
    y = y + h * panta    # y_{n+1} = y_n + h * f(t_n, y_n)
    t = t + h            # avansam in timp

    # Calculam si afisam eroarea
    err = abs(y - y_exact(t))
    print(f"{i+1:>5} {t:>8.4f} {y:>12.6f} {y_exact(t):>12.6f} {err:>12.2e}")

print()
print("OBSERVATIE: Eroarea creste in timp (acumulare de erori la fiecare pas).")
print("Cu h mai mic, eroarea ar fi mai mica. Metoda RK4 (Prob. 42) e mult mai precisa!")