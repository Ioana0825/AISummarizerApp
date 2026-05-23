"""
PROBLEMA 14 - Numarul de iteratii necesar la bisectie
======================================================
Capitol din curs: "Metode numerice pentru ecuatii neliniare"
                  Sectiunea: Analiza convergentei bisectiei
CERINTA: Câte iterații sunt necesare pentru a găsi rădăcina lui f(x) = x3 − x − 2 = 0 pe [1, 2] cu ε = 10−6?
Ecuatie: f(x) = x^3 - x - 2 = 0  pe [1, 2],  epsilon = 10^-6

TEORIE:
  Dupa n iteratii de bisectie, eroarea maxima este:
      e_n = (b - a) / 2^n

  Vrem e_n <= epsilon, adica:
      (b - a) / 2^n <= eps
      2^n >= (b - a) / eps
      n >= log2((b - a) / eps)

  Deci: n_minim = ceil( log2((b - a) / eps) )
"""

import numpy as np  # Necesara pentru log2 si ceil


def f(x):
    """
    Functia de rezolvat: f(x) = x^3 - x - 2
    Radacina se afla in [1, 2] deoarece f(1)=-2 < 0 si f(2)=4 > 0
    """
    return x**3 - x - 2  # Polinom de gradul 3


# --- Parametrii problemei ---
a = 1.0    # Capatul stang
b = 2.0    # Capatul drept
eps = 1e-6  # Precizia dorita

# --- Verificare Bolzano ---
print(f"f(a=1) = {f(1.0):.4f}  (negativ)")
print(f"f(b=2) = {f(2.0):.4f}  (pozitiv)")
print(f"Semne opuse => exista radacina in [1, 2] (Teorema Bolzano) ✓")
print()

# --- Calculul teoretic al numarului de iteratii ---
# n >= log2((b - a) / eps)
raport = (b - a) / eps            # Raportul dintre lungimea intervalului si precizie
n_teoretic = np.ceil(np.log2(raport))  # Rotunjim in sus pentru a asigura precizia

print(f"Formula: n >= log2((b-a)/eps)")
print(f"       = log2({b-a} / {eps})")
print(f"       = log2({raport})")
print(f"       = {np.log2(raport):.4f}")
print(f"       => n_minim = {n_teoretic:.0f} iteratii")
print()

# --- Verificare prin bisectie efectiva ---
a_v, b_v = a, b   # Copiem intervalul pentru a nu modifica originalul
n_real = 0         # Numarul real de iteratii

while (b_v - a_v) / 2 > eps:      # Conditia de oprire
    c_v = (a_v + b_v) / 2         # Mijlocul intervalului
    n_real += 1
    if f(a_v) * f(c_v) < 0:       # Radacina e in [a, c]
        b_v = c_v
    else:                           # Radacina e in [c, b]
        a_v = c_v

# --- Rezultate ---
print(f"Verificare practica:")
print(f"  Numar teoretic de iteratii: {n_teoretic:.0f}")
print(f"  Numar real de iteratii:     {n_real}")
print(f"  Radacina gasita:            x = {c_v:.8f}")
print(f"  Verificare:                 f({c_v:.6f}) = {f(c_v):.2e}")
print()
print(f"Observatie: n_real <= n_teoretic intotdeauna ({n_real} <= {n_teoretic:.0f}) ✓")