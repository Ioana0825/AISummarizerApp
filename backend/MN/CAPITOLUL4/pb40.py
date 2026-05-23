"""
PROBLEMA 40 - Regula compozita a Trapezului cu n=8 si n=16
CERINTA: Aproximați ∫0^π sin(x) dx prin regula compozită a trapezului cu n = 8 și n = 16. Comparați.
===========================================================
TEORIE (Curs - Capitol: Integrare Numerica):
  Aceeasi formula ca la Problema 35, dar acum comparam doua valori ale lui n
  pentru a vedea cum scade eroarea:

      ∫_a^b f(x)dx ≈ (h/2) * [f(x0) + 2*f(x1) + ... + 2*f(xn-1) + f(xn)]

  Eroarea metodei trapezului: E ≈ -(b-a)*h^2/12 * f''(ξ)
  => Daca dublam n (jumatam h), eroarea scade de 4 ori (factor h^2)!

  Aceasta se numeste "convergenta de ordin 2" => O(h^2)

Se cere: ∫_0^π sin(x) dx cu n=8 si n=16
Valoarea exacta: [-cos(x)]_0^π = -cos(π) - (-cos(0)) = 1 + 1 = 2
"""

import math

# -------------------------------------------------------
# PASUL 1: Definim functia si limitele de integrare
# -------------------------------------------------------
def f(x):
    return math.sin(x)    # f(x) = sin(x)

a = 0           # limita inferioara
b = math.pi     # limita superioara: π

# -------------------------------------------------------
# PASUL 2: Functia generala pentru regula trapezului
# (reutilizabila pentru orice n)
# -------------------------------------------------------
def trapez(f, a, b, n):
    """
    Aproximeaza integrala ∫_a^b f(x)dx cu regula trapezului compus.
    Parametri:
        f - functia de integrat
        a, b - limitele de integrare
        n - numarul de subintervale
    Formula: (h/2) * [f(x0) + 2*sum_interior + f(xn)]
    """
    h = (b - a) / n                    # pasul de discretizare
    suma = f(a) + f(b)                 # capetele: coeficient 1

    for i in range(1, n):
        xi = a + i * h                 # nodul interior i
        suma += 2 * f(xi)              # coeficientul 2 pentru termenii interiori

    return (h / 2) * suma             # inmultim cu h/2

# -------------------------------------------------------
# PASUL 3: Calculam pentru n=8 si n=16
# -------------------------------------------------------
exacta = 2.0    # -cos(π) + cos(0) = 1 + 1 = 2

print("=== PROBLEMA 40 - Regula Compozita a Trapezului ===")
print(f"Integrala: ∫_0^π sin(x) dx")
print(f"Valoarea exacta: {exacta:.8f}")
print()

for n in [8, 16]:
    h = (b - a) / n
    rezultat = trapez(f, a, b, n)
    eroare = abs(rezultat - exacta)
    print(f"n={n:2d}: h={h:.6f},  Trapez={rezultat:.8f},  Eroare={eroare:.2e}")

print()
# -------------------------------------------------------
# PASUL 4: Verificam convergenta O(h^2)
# -------------------------------------------------------
# Daca dublam n => h se injumatateste => eroarea ar trebui sa scada de 4 ori
rez_8  = trapez(f, a, b, 8)
rez_16 = trapez(f, a, b, 16)
err_8  = abs(rez_8 - exacta)
err_16 = abs(rez_16 - exacta)

raport = err_8 / err_16
print(f"Eroare n=8:  {err_8:.6e}")
print(f"Eroare n=16: {err_16:.6e}")
print(f"Raport erori (E8/E16): {raport:.2f}  (teoretic ≈ 4 pentru ordin 2)")