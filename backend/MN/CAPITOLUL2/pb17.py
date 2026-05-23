"""
PROBLEMA 17 - Metoda Punctului Fix: cos(x) - x = 0
====================================================
Capitol din curs: "Metode numerice pentru ecuatii neliniare"
                  Sectiunea: Metoda Punctului Fix (Iteratii Succesive)
CERINTA: Rezolvați cos(x) − x = 0 prin metoda punctului fix g(x) = cos(x), pornind de la x0 = 0.5.

TEORIE:
  Rescrierea ecuatiei f(x) = 0 sub forma x = g(x)

  Ecuatia: cos(x) - x = 0
  Rescriem: x = cos(x)  =>  g(x) = cos(x)

  Iteratia: x_{n+1} = g(x_n) = cos(x_n)

  CONDITIA DE CONVERGENTA (Teorema contractiei):
      |g'(x)| < 1  in vecinatatea radacinii

  Pentru g(x) = cos(x):
      g'(x) = -sin(x)
      |g'(x*)| = |sin(x*)| ≈ |sin(0.739)| ≈ 0.674 < 1  => CONVERGE ✓

  Radacina x* ≈ 0.7390851332 se numeste "punctul Dottie"
"""

import math

# Functia de iteratie: g(x) = cos(x)
# Obtinuta din rescrierea ecuatiei: cos(x) - x = 0 => x = cos(x)
def g(x): return math.cos(x)


def punct_fix(x0, eps=1e-6):
    xn = x0                          # Pornim iteratia din punctul initial x0
    for n in range(1, 80):           # Maxim 80 iteratii (converge mai lent decat Newton)
        xn1 = g(xn)                  # Aplicam iteratia: x_nou = cos(x_vechi)
        err = abs(xn1 - xn)          # Eroarea = distanta dintre doua iteratii consecutive
        if n <= 5 or n % 10 == 0 or err < eps:  # Afisam primele 5, apoi din 10 in 10
            print(f"  pas {n:2d}: x = {xn1:.10f}  err = {err:.2e}")
        if err < eps:                # Eroarea suficient de mica => am atins precizia dorita
            return xn1               # Returnam radacina gasita
        xn = xn1                     # Actualizam x pentru urmatoarea iteratie

# Convergenta LINIARA vizibila in output (eroarea scade incet, ~0.67x la fiecare pas)
# Comparatie: Newton-Raphson gaseste radacina in ~5 iteratii, punctul fix in ~35!
punct_fix(0.0)  # Apelam cu x0 = 0.0 (punct initial, ca in curs)