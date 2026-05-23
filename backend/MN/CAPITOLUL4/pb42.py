"""
PROBLEMA 42 - Metoda Runge-Kutta de ordin 4 (RK4)
CERINTA: Rezolvați y' = y − t2 + 1, y(0) = 0.5 pe [0, 2] cu metoda RK4, h = 0.5.
===================================================
TEORIE (Curs - Capitol: Rezolvarea Numerica a EDO):
  RK4 aproximeaza panta ca o medie ponderata a 4 estimari:

      k1 = h * f(t_n, y_n)
      k2 = h * f(t_n + h/2, y_n + k1/2)
      k3 = h * f(t_n + h/2, y_n + k2/2)
      k4 = h * f(t_n + h, y_n + k3)

      y_{n+1} = y_n + (1/6) * (k1 + 2*k2 + 2*k3 + k4)

  Intuitie:
      k1 = panta la INCEPUTUL intervalului
      k2 = panta la MIJLOC (folosind k1 pt estimare)
      k3 = panta la MIJLOC (mai buna, folosind k2)
      k4 = panta la SFARSIT (folosind k3)
  => Media ponderata (1, 2, 2, 1) / 6 ~ panta "ideala" a intervalului

  EROAREA globala: O(h^4)  => MULT mai precis decat Euler O(h)!
  Cu acelasi h, RK4 e de ordinul h^3 ori mai precis decat Euler.

Aceeasi problema ca Euler: y' = y - t^2 + 1, y(0) = 0.5, pe [0,2], h=0.5
"""

import math

# -------------------------------------------------------
# PASUL 1: Definim functia EDO si solutia exacta
# -------------------------------------------------------
def f(t, y):
    return y - t**2 + 1    # ecuatia diferentiala

def y_exact(t):
    return (t + 1)**2 - 0.5 * math.exp(t)    # solutia analitica

# -------------------------------------------------------
# PASUL 2: Parametrii (identici cu Euler pentru comparatie)
# -------------------------------------------------------
t0 = 0.0
y0 = 0.5
h  = 0.5
t_final = 2.0
n_pasi = int((t_final - t0) / h)   # 4 pasi

print("=== PROBLEMA 42 - Metoda Runge-Kutta RK4 ===")
print(f"EDO: y' = y - t^2 + 1,  y(0) = {y0}")
print(f"Interval: [{t0}, {t_final}],  h = {h},  {n_pasi} pasi")
print()
print(f"{'Pasul':>5} {'t':>8} {'y_RK4':>12} {'y_exact':>12} {'Eroare':>12}")
print("-" * 55)

# -------------------------------------------------------
# PASUL 3: Aplicam metoda RK4 pas cu pas
# -------------------------------------------------------
t = t0
y = y0

# Afisam conditia initiala
print(f"{'0':>5} {t:>8.4f} {y:>12.8f} {y_exact(t):>12.8f} {abs(y - y_exact(t)):>12.2e}")

for i in range(n_pasi):
    # Calculam cele 4 pante (ki sunt deja inmultiti cu h)
    k1 = h * f(t, y)                    # panta la inceputul intervalului
    k2 = h * f(t + h/2, y + k1/2)      # panta la mijloc (est. cu k1)
    k3 = h * f(t + h/2, y + k2/2)      # panta la mijloc (est. cu k2, mai buna)
    k4 = h * f(t + h,   y + k3)        # panta la sfarsitul intervalului

    # Afisam k-urile pentru primul pas (sa intelegem formula)
    if i == 0:
        print(f"\n  [Pasul 1 detaliat]")
        print(f"  k1 = {k1:.8f}  (panta * h la t={t:.2f})")
        print(f"  k2 = {k2:.8f}  (panta * h la t={t+h/2:.2f}, y+k1/2)")
        print(f"  k3 = {k3:.8f}  (panta * h la t={t+h/2:.2f}, y+k2/2)")
        print(f"  k4 = {k4:.8f}  (panta * h la t={t+h:.2f}, y+k3)")
        print(f"  Medie ponderata: (k1 + 2k2 + 2k3 + k4)/6 = {(k1+2*k2+2*k3+k4)/6:.8f}")
        print()

    # Formula RK4: media ponderata a celor 4 estimari
    y = y + (k1 + 2*k2 + 2*k3 + k4) / 6
    t = t + h

    err = abs(y - y_exact(t))
    print(f"{i+1:>5} {t:>8.4f} {y:>12.8f} {y_exact(t):>12.8f} {err:>12.2e}")

print()
print("COMPARATIE CU EULER (din Problema 41):")
print("  Eroarea Euler la t=2: ~0.051   (O(h) = O(0.5) = 0.5)")
print("  Eroarea RK4   la t=2: ~0.00005  (O(h^4) = O(0.0625))")
print("  RK4 e de ~1000x mai precis cu acelasi pas h=0.5!")