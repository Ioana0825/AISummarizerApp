"""
PROBLEMA 16 - Metoda Newton-Raphson: f(x) = x*e^x - 2 = 0
===========================================================
Capitol din curs: "Metode numerice pentru ecuatii neliniare"
                  Sectiunea: Metoda Newton-Raphson
CERINTA: Aplicați metoda Newton-Raphson pentru f(x) = xex − 2, f'(x) = ex(1+x), cu x0 = 1, ε = 10−6.

TEORIE:
  Ideea: aproximam f(x) cu tangenta in punctul curent x_n.
  Din expansiunea Taylor: f(x) ≈ f(x_n) + f'(x_n) * (x - x_n)

  Setam aproximarea egala cu 0 si rezolvam pentru x:
      f(x_n) + f'(x_n) * (x_{n+1} - x_n) = 0
      x_{n+1} = x_n - f(x_n) / f'(x_n)

  Convergenta PATRATICA: daca x_n are k cifre corecte,
  x_{n+1} are aproximativ 2k cifre corecte!

  Pentru f(x) = x*e^x - 2:
      f'(x) = e^x + x*e^x = e^x*(1+x)   [regula produsului]
"""

import math

# Functia de rezolvat: f(x) = x*e^x - 2 = 0
def f(x):  return x * math.exp(x) - 2

# Derivata: f'(x) = e^x*(1+x)
# Regula produsului: (x * e^x)' = 1*e^x + x*e^x = e^x*(1+x)
def fp(x): return math.exp(x) * (1 + x)


def newton(x0, eps=1e-6):
    xn = x0                        # Pornim iteratia din punctul initial x0
    for n in range(1, 20):         # Maxim 20 de iteratii (convergenta e rapida)
        xn1 = xn - f(xn) / fp(xn) # Formula Newton: x_nou = x - f(x)/f'(x)
        err = abs(xn1 - xn)        # Eroarea = distanta dintre doua iteratii consecutive
        print(f"  pas {n}: x = {xn1:.10f}  err = {err:.2e}")
        if err < eps:              # Daca eroarea < epsilon, am atins precizia dorita
            return xn1             # Returnam radacina gasita
        xn = xn1                   # Actualizam x pentru urmatoarea iteratie


# Convergenta patratica vizibila in output:
#   pas 1: err ≈ 1e-1
#   pas 2: err ≈ 1e-2
#   pas 3: err ≈ 1e-4   (eroarea se PATRATEAZA la fiecare pas!)
#   pas 4: err ≈ 1e-8
newton(1.0)  # Apelam cu x0 = 1.0 (punct initial, ales aproape de radacina)