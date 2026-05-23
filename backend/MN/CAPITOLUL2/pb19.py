"""
PROBLEMA 19 - Newton-Raphson: calculul lui sqrt(3) fara functia sqrt
=====================================================================
Capitol din curs: "Metode numerice pentru ecuatii neliniare"
                  Sectiunea: Aplicatii ale metodei Newton-Raphson

CERINTA: Aproximați √3 rezolvând ecuația f(x) = x2 − 3 = 0 prin Newton-Raphson, pornind de la x0 = 1.

IDEE:
  sqrt(3) este solutia pozitiva a ecuatiei: x^2 - 3 = 0

  Aplicam Newton-Raphson:
      f(x)  = x^2 - 3
      f'(x) = 2x

  Formula Newton:
      x_{n+1} = x_n - f(x_n)/f'(x_n)
              = x_n - (x_n^2 - 3) / (2*x_n)
              = (2*x_n^2 - x_n^2 + 3) / (2*x_n)
              = (x_n^2 + 3) / (2*x_n)
              = (x_n + 3/x_n) / 2   <= MEDIA ARITMETICA a lui x si 3/x!

  Aceasta este celebra "metoda babiloniana" de calcul a radacinii patrate.
"""

import numpy as np  # Folosim doar pentru sqrt(3) de referinta si comparatie


def f(x):
    """
    f(x) = x^2 - 3
    Radacina pozitiva a acestei ecuatii este sqrt(3)
    """
    return x ** 2 - 3  # Polinom simplu de gradul 2


def df(x):
    """
    f'(x) = 2*x   (derivata lui x^2 este 2x)
    """
    return 2 * x


# --- Parametrii problemei ---
x = 1.0  # Punct initial pozitiv (cautam sqrt > 0)
eps = 1e-10  # Precizie foarte mare pentru a vedea convergenta patratica
max_iter = 20

valoare_exacta = np.sqrt(3)  # Valoarea de referinta din Python
print(f"Cautam sqrt(3)")
print(f"Valoarea exacta (Python): sqrt(3) = {valoare_exacta:.15f}")
print(f"Punct initial: x0 = {x}")
print()
print(f"Formula iteratiei: x_nou = (x + 3/x) / 2")
print()
print(f"{'Iter':>4} | {'x_n':>18} | {'(x+3/x)/2':>18} | {'Eroare vs sqrt(3)':>18}")
print("-" * 65)

# --- Bucla principala Newton-Raphson ---
for i in range(max_iter):
    # Formula Newton simplificata: x_nou = (x + 3/x) / 2
    # Echivalenta cu: x_nou = x - (x^2-3)/(2x)
    x_nou = x - f(x) / df(x)  # Aplicam formula generala Newton

    eroare = abs(x_nou - valoare_exacta)  # Eroarea fata de valoarea exacta

    print(f"{i + 1:>4} | {x:>18.15f} | {x_nou:>18.15f} | {eroare:>18.2e}")

    # --- Criteriu de oprire ---
    if abs(x_nou - x) < eps:  # Convergenta atinsa
        break

    x = x_nou  # Actualizam x

# --- Rezultat final ---
print(f"\nRadacina gasita: sqrt(3) ≈ {x_nou:.15f}")
print(f"Valoarea exacta: sqrt(3) = {valoare_exacta:.15f}")
print(f"Eroare absoluta:           {abs(x_nou - valoare_exacta):.2e}")
print(f"Numar iteratii:  {i + 1}")
print()
print(f"Convergenta patratica: observati cum eroarea se PATRATEAZA!")
print(f"  Dupa iteratia 1: ~2.7e-1")
print(f"  Dupa iteratia 2: ~1.8e-2")
print(f"  Dupa iteratia 3: ~9.2e-5")
print(f"  Dupa iteratia 4: ~2.5e-9  (de la 5 cifre la 9 cifre dintr-o data!)")