"""
PROBLEMA 20 - Metoda Bisectiei: f(x) = ln(x) + x - 2 = 0 pe [1, 2]
======================================================================
Capitol din curs: "Metode numerice pentru ecuatii neliniare"
                  Sectiunea: Metoda Bisectiei - aplicatii

CERINTA: Găsiți rădăcina ecuației f(x) = ln(x) + x − 2 = 0 pe [1, 2] cu ε = 10−5.

Ecuatie TRANSCENDENTA (contine atat logaritm cat si x => nu se poate
rezolva analitic, necesita metode numerice).

TEORIE (aceeasi ca la Problema 13):
  1. Verificam Teorema Bolzano: f(a)*f(b) < 0
  2. Calculam numarul de iteratii: n >= log2((b-a)/eps)
  3. Aplicam bisectia: c = (a+b)/2, injumatatim intervalul

  f(x) = ln(x) + x - 2
  f(1) = 0 + 1 - 2 = -1 < 0
  f(2) = ln(2) + 2 - 2 = 0.693 > 0
  => Radacina in [1, 2] ✓
"""

import numpy as np  # Biblioteca pentru log (logaritm natural) si log2


def f(x):
    """
    Functia transcendenta: f(x) = ln(x) + x - 2
    np.log = logaritm natural (baza e), nu baza 10!
    """
    return np.log(x) + x - 2  # np.log(x) = ln(x)


# --- Parametrii problemei ---
a = 1.0     # Capatul stang
b = 2.0     # Capatul drept
eps = 1e-5  # Precizia dorita (mai mica decat la P13, deci mai putine iteratii)

# --- Verificare Teorema Bolzano ---
print(f"f(a=1) = ln(1) + 1 - 2 = {f(1.0):.4f}  (negativ)")
print(f"f(b=2) = ln(2) + 2 - 2 = {f(2.0):.4f}  (pozitiv)")
print(f"f(a)*f(b) = {f(a)*f(b):.4f} < 0  => radacina garantata in [1, 2] ✓")
print()

# --- Numarul teoretic de iteratii ---
# n >= log2((b - a) / eps)
n_teoretic = np.ceil(np.log2((b - a) / eps))  # np.ceil = rotunjire in sus (plafon)
print(f"Numar teoretic de iteratii: n >= log2({b-a}/{eps}) = {n_teoretic:.0f}")
print()

# --- Tabel de iteratii ---
print(f"{'Iter':>4} | {'a':>10} | {'b':>10} | {'c=(a+b)/2':>10} | {'f(c)':>12} | {'b-a':>10}")
print("-" * 65)

iteratie = 0  # Contorul de iteratii

# --- Bucla bisectiei ---
while (b - a) / 2 > eps:      # Continuam cat timp jumatatea intervalului > eps
    c = (a + b) / 2            # Mijlocul intervalului
    iteratie += 1

    print(f"{iteratie:>4} | {a:>10.6f} | {b:>10.6f} | {c:>10.6f} | {f(c):>12.2e} | {b-a:>10.2e}")

    if f(a) * f(c) < 0:        # Radacina in [a, c] => mutam capatul drept
        b = c
    else:                        # Radacina in [c, b] => mutam capatul stang
        a = c

# --- Rezultat final ---
print(f"\nRadacina gasita: x = {c:.7f}")
print(f"Numar iteratii:  {iteratie}  (teoretic: {n_teoretic:.0f})")
print(f"Verificare:      f({c:.5f}) = {f(c):.2e}  ✓")
print()
print(f"Verificare alternativa (Newton ar gasi in ~4 iteratii):")
print(f"  f'(x) = 1/x + 1  =>  f'(1.5) = {1/1.5 + 1:.4f}")