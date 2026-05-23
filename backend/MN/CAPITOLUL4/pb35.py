"""
PROBLEMA 35 - Regula Trapezului (integrare numerica)
CERINTA: Aproximați ∫01 ex dx prin regula trapezului cu n = 4 subintervale egale.
====================================================
TEORIE (Curs - Capitol: Integrare Numerica):
  Aproximam integrala prin suma ariilor trapezelor:

      ∫_a^b f(x)dx ≈ (h/2) * [f(x0) + 2*f(x1) + 2*f(x2) + ... + 2*f(xn-1) + f(xn)]

  unde h = (b-a)/n  (pasul de discretizare)
       xi = a + i*h  (nodurile)

  EROAREA de trunchiere: E ≈ -(b-a)*h^2/12 * f''(ξ)
  => cu cat h mai mic (n mai mare), cu atat mai precis!

Se cere: ∫_0^1 e^x dx cu n=4 subintervale
Valoarea exacta: e^1 - e^0 = e - 1 ≈ 1.71828
"""

import math  # pentru math.exp

# -------------------------------------------------------
# PASUL 1: Definim functia si parametrii
# -------------------------------------------------------
# Functia de integrat: f(x) = e^x
def f(x):
    return math.exp(x)   # e^x

a = 0       # limita inferioara
b = 1       # limita superioara
n = 4       # numarul de subintervale

# -------------------------------------------------------
# PASUL 2: Calculam pasul si nodurile
# -------------------------------------------------------
h = (b - a) / n   # h = (1-0)/4 = 0.25  (latimea unui interval)

# Nodurile: x0=0, x1=0.25, x2=0.5, x3=0.75, x4=1
# xi = a + i*h
noduri = [a + i * h for i in range(n + 1)]

print("=== PROBLEMA 35 - Regula Trapezului ===")
print(f"Interval: [{a}, {b}], n={n}, h={h}")
print(f"Noduri: {[f'{xi:.2f}' for xi in noduri]}")
print()

# -------------------------------------------------------
# PASUL 3: Aplicam formula trapezului compus
# Formula: (h/2) * [f(x0) + 2*f(x1) + ... + 2*f(xn-1) + f(xn)]
# -------------------------------------------------------
suma = f(noduri[0]) + f(noduri[n])    # primul si ultimul termen (coef = 1)

print("Calculul sumei:")
print(f"  f(x0) = f({noduri[0]:.2f}) = {f(noduri[0]):.6f}  (coef=1)")

for i in range(1, n):
    # Termenii din mijloc au coeficientul 2
    print(f"  f(x{i}) = f({noduri[i]:.2f}) = {f(noduri[i]):.6f}  (coef=2, contributie={2*f(noduri[i]):.6f})")
    suma += 2 * f(noduri[i])          # coeficientul 2 pentru termenii interiori

print(f"  f(xn) = f({noduri[n]:.2f}) = {f(noduri[n]):.6f}  (coef=1)")

# Inmultim suma cu h/2
rezultat = (h / 2) * suma

# -------------------------------------------------------
# PASUL 4: Comparatie cu valoarea exacta
# -------------------------------------------------------
exacta = math.exp(1) - math.exp(0)   # = e - 1 = 1.71828...
eroare = abs(rezultat - exacta)

print()
print(f"Rezultat Trapez (n={n}): {rezultat:.8f}")
print(f"Valoarea exacta:         {exacta:.8f}")
print(f"Eroarea absoluta:        {eroare:.2e}")