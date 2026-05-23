"""
PROBLEMA 36 - Regula lui Simpson 1/3
CERINTA: Aproximați ∫01 ex dx prin regula Simpson 1/3 cu n = 4 (n par).
=====================================
TEORIE (Curs - Capitol: Integrare Numerica):
  Simpson 1/3 aproximeaza functia cu un polinom de grad 2 pe fiecare pereche
  de subintervale (de aceea n trebuie sa fie PARE):

      ∫_a^b f(x)dx ≈ (h/3) * [f(x0) + 4*f(x1) + 2*f(x2) + 4*f(x3) + ... + 4*f(xn-1) + f(xn)]

  Sablonul coeficientilor: 1, 4, 2, 4, 2, ..., 4, 1
  (termenii pare (interiori) au coef=2, termenii impare au coef=4)

  EROAREA: E ≈ -(b-a)*h^4/180 * f^(4)(ξ)  => MULT mai precis decat Trapezul!

Se cere: ∫_0^1 e^x dx cu n=4 (n par!)
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
n = 4       # numarul de subintervale (TREBUIE SA FIE PAR!)

# Verificam ca n e par (conditie obligatorie pentru Simpson 1/3)
if n % 2 != 0:
    print("EROARE: n trebuie sa fie par pentru Simpson 1/3!")
    exit()

# -------------------------------------------------------
# PASUL 2: Calculam pasul si nodurile
# -------------------------------------------------------
h = (b - a) / n   # h = 0.25

noduri = [a + i * h for i in range(n + 1)]   # 5 noduri: 0, 0.25, 0.5, 0.75, 1

print("=== PROBLEMA 36 - Regula Simpson 1/3 ===")
print(f"Interval: [{a}, {b}], n={n}, h={h}")
print(f"Coeficienti: 1, 4, 2, 4, 1  (sablon: 1, [4,2,...], 4, 1)")
print()

# -------------------------------------------------------
# PASUL 3: Aplicam formula Simpson 1/3
# Coeficienti: primul=1, ultimul=1, impare=4, pare=2
# -------------------------------------------------------
suma = f(noduri[0]) + f(noduri[n])   # capetele au coeficientul 1

print("Calculul sumei:")
print(f"  f(x0=0.00) = {f(noduri[0]):.6f}  (coef=1)")

for i in range(1, n):
    if i % 2 == 1:
        # Indici impari (1, 3, 5, ...) => coeficient 4
        coef = 4
    else:
        # Indici pari (2, 4, 6, ...) => coeficient 2
        coef = 2
    print(f"  f(x{i}={noduri[i]:.2f}) = {f(noduri[i]):.6f}  (coef={coef}, contributie={coef*f(noduri[i]):.6f})")
    suma += coef * f(noduri[i])

print(f"  f(xn=1.00) = {f(noduri[n]):.6f}  (coef=1)")

# Inmultim cu h/3
rezultat = (h / 3) * suma

# -------------------------------------------------------
# PASUL 4: Comparatie
# -------------------------------------------------------
exacta = math.exp(1) - 1
eroare = abs(rezultat - exacta)

print()
print(f"Rezultat Simpson 1/3 (n={n}): {rezultat:.8f}")
print(f"Valoarea exacta:              {exacta:.8f}")
print(f"Eroarea absoluta:             {eroare:.2e}")
print()
print("Comparatie cu Trapezul (eroare ~0.000040):")
print("  Simpson 1/3 este MULT mai precis (eroare de ordinul h^4 vs h^2)")