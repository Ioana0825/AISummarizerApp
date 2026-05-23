"""
PROBLEMA 37 - Regula 3/8 a lui Simpson
CERINTA: Aproximați ∫01 ex dx prin regula Simpson 3/8 cu n = 3 subintervale.
=======================================
TEORIE (Curs - Capitol: Integrare Numerica):
  Simpson 3/8 foloseste un polinom de grad 3 pe fiecare grup de 3 subintervale.
  n trebuie sa fie MULTIPLU DE 3.

      ∫_a^b f(x)dx ≈ (3h/8) * [f(x0) + 3*f(x1) + 3*f(x2) + 2*f(x3) + 3*f(x4) + ... + f(xn)]

  Sablonul coeficientilor: 1, 3, 3, 2, 3, 3, 2, ..., 3, 3, 1

  EROAREA: E ≈ -(b-a)*h^4/80 * f^(4)(ξ)
  Precizie similara cu Simpson 1/3, utila cand n e multiplu de 3 dar nu de 2.

Se cere: ∫_0^1 e^x dx cu n=3 subintervale
Valoarea exacta: e - 1 ≈ 1.71828
"""

import math

# -------------------------------------------------------
# PASUL 1: Definim functia si parametrii
# -------------------------------------------------------
def f(x):
    return math.exp(x)   # f(x) = e^x

a = 0       # limita inferioara
b = 1       # limita superioara
n = 3       # numarul de subintervale (MULTIPLU DE 3!)

# Verificam conditia
if n % 3 != 0:
    print("EROARE: n trebuie sa fie multiplu de 3 pentru Simpson 3/8!")
    exit()

# -------------------------------------------------------
# PASUL 2: Calculam pasul si nodurile
# -------------------------------------------------------
h = (b - a) / n     # h = 1/3 ≈ 0.3333

noduri = [a + i * h for i in range(n + 1)]   # 4 noduri: 0, 1/3, 2/3, 1

print("=== PROBLEMA 37 - Regula Simpson 3/8 ===")
print(f"Interval: [{a}, {b}], n={n}, h={h:.6f}")
print(f"Noduri: {[f'{xi:.4f}' for xi in noduri]}")
print()

# -------------------------------------------------------
# PASUL 3: Aplicam formula Simpson 3/8
# Coeficienti: 1, 3, 3, 2, 3, 3, ..., 1
# -------------------------------------------------------
suma = f(noduri[0]) + f(noduri[n])    # capetele: coeficient 1

print("Calculul sumei:")
print(f"  f(x0={noduri[0]:.4f}) = {f(noduri[0]):.6f}  (coef=1)")

for i in range(1, n):
    if i % 3 == 0:
        # Multiplii de 3 (la granita grupurilor): coeficient 2
        coef = 2
    else:
        # Restul (pozitia 1,2 in fiecare grup de 3): coeficient 3
        coef = 3
    print(f"  f(x{i}={noduri[i]:.4f}) = {f(noduri[i]):.6f}  (coef={coef})")
    suma += coef * f(noduri[i])

print(f"  f(xn={noduri[n]:.4f}) = {f(noduri[n]):.6f}  (coef=1)")

# Formula 3/8: inmultim cu 3h/8
rezultat = (3 * h / 8) * suma

# -------------------------------------------------------
# PASUL 4: Comparatie cu valoarea exacta
# -------------------------------------------------------
exacta = math.exp(1) - 1
eroare = abs(rezultat - exacta)

print()
print(f"Rezultat Simpson 3/8 (n={n}): {rezultat:.8f}")
print(f"Valoarea exacta:              {exacta:.8f}")
print(f"Eroarea absoluta:             {eroare:.2e}")