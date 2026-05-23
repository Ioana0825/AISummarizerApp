"""
PROBLEMA 15 - Metoda Secantei: f(x) = x*e^x - 2 = 0
=====================================================
Capitol din curs: "Metode numerice pentru ecuatii neliniare"
                  Sectiunea: Metoda Secantei

CERINTA: Aplicați metoda secantei pentru f(x) = xe^x − 2 = 0 cu x0 = 0, x1 = 1, ε = 10−6.

TEORIE:
  La metoda Newton avem nevoie de derivata f'(x).
  La metoda SECANTEI aproximam derivata cu diferenta finita:

      f'(x_n) ≈ [f(x_n) - f(x_{n-1})] / (x_n - x_{n-1})

  Inlocuind in formula Newton => formula secantei:

      x_{n+1} = x_n - f(x_n) * (x_n - x_{n-1}) / (f(x_n) - f(x_{n-1}))

  Avantaj:    Nu necesita calculul derivatei f'(x)
  Dezavantaj: Necesita DOUA puncte initiale x0 si x1
  Convergenta: Supraliniara (ordin ≈ 1.618, numarul de aur)
"""

import numpy as np  # Biblioteca pentru calcule matematice


def f(x):
    """
    Functia de rezolvat: f(x) = x * e^x - 2
    """
    return x * np.exp(x) - 2  # np.exp(x) = e^x


# --- Parametrii problemei ---
x0 = 0.0   # Primul punct initial
x1 = 1.0   # Al doilea punct initial (NU trebuie sa incadreze radacina!)
eps = 1e-6  # Precizia dorita
max_iter = 50  # Protectie: maxim 50 de iteratii

print(f"Metoda Secantei pentru f(x) = x*e^x - 2 = 0")
print(f"Puncte initiale: x0 = {x0}, x1 = {x1}")
print(f"f(x0) = {f(x0):.4f},  f(x1) = {f(x1):.4f}")
print()
print(f"{'Iter':>4} | {'x0':>10} | {'x1':>10} | {'x2 (nou)':>10} | {'f(x2)':>12} | {'|x2-x1|':>10}")
print("-" * 65)

# --- Bucla principala a metodei secantei ---
for i in range(max_iter):
    f0 = f(x0)   # Valoarea functiei in x0
    f1 = f(x1)   # Valoarea functiei in x1

    # Formula secantei:
    # x2 = x1 - f(x1) * (x1 - x0) / (f(x1) - f(x0))
    # Aceasta este dreapta (secanta) care trece prin (x0,f(x0)) si (x1,f(x1))
    x2 = x1 - f1 * (x1 - x0) / (f1 - f0)

    diferenta = abs(x2 - x1)  # Cat de mult s-a schimbat x

    print(f"{i+1:>4} | {x0:>10.6f} | {x1:>10.6f} | {x2:>10.6f} | {f(x2):>12.2e} | {diferenta:>10.2e}")

    # --- Criteriu de oprire ---
    if diferenta < eps:  # Daca x nu s-a mai schimbat semnificativ => am converges
        break

    # --- Actualizam punctele pentru urmatoarea iteratie ---
    x0 = x1   # Vechiul x1 devine noul x0
    x1 = x2   # Noul x2 devine noul x1

# --- Rezultat final ---
print(f"\nRadacina gasita: x = {x2:.8f}")
print(f"Numar iteratii:  {i+1}")
print(f"Verificare:      f({x2:.6f}) = {f(x2):.2e}  (aproape de 0 ✓)")
print()
print(f"Comparatie: Bisectia necesita ~19 iteratii, Secanta doar {i+1}!")